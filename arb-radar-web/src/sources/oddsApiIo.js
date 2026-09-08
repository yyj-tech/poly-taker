import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { getOddsKey } from "../config.js";
import { isDotaOrLol } from "../lib/match.js";

const BASE = "https://api.odds-api.io/v3";
const BOOKS = "Stake,Duel";
const CACHE_PATH = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../data/oai-cache.json");
const EVENT_TTL_MS = 30 * 60 * 1000;
const ODDS_TTL_MS = 4 * 60 * 1000;
let mem = { at: 0, events: [], rows: [], rowsAt: 0 };

function loadDisk() {
  try {
    const raw = JSON.parse(fs.readFileSync(CACHE_PATH, "utf8"));
    if (raw && Array.isArray(raw.events)) return raw;
  } catch {
    // no cache yet
  }
  return null;
}

function saveDisk(payload) {
  try {
    fs.mkdirSync(path.dirname(CACHE_PATH), { recursive: true });
    fs.writeFileSync(CACHE_PATH, JSON.stringify(payload) + "\n");
  } catch (err) {
    console.error("oai cache write failed", err && err.message ? err.message : err);
  }
}

function dailyLimitNote(err) {
  const body = err && err.body;
  const msg = (body && body.error) || (err && err.message) || "";
  if (err && err.status === 429) {
    if (/daily/i.test(String(msg))) {
      return "HTTP 429 日配额已用尽（免费档 500/天，UTC 0 点重置）";
    }
    return "HTTP 429 限流 " + String(msg).slice(0, 160);
  }
  return err && err.message ? err.message : String(err);
}

function lastGood(fetchedAt, err) {
  const disk = loadDisk();
  const events = (mem.rows && mem.rows.length && mem.rows) || (disk && disk.rows) || [];
  if (!events.length) {
    return {
      ok: false,
      status: "失败",
      error: dailyLimitNote(err),
      fetchedAt,
      events: [],
    };
  }
  return {
    ok: true,
    status: "缓存",
    error: dailyLimitNote(err),
    fetchedAt: (disk && disk.fetchedAt) || mem.rowsAt || fetchedAt,
    nEvents: events.length,
    nStake: events.filter((r) => r.stakeHome || r.stakeAway).length,
    nDuel: events.filter((r) => r.duelHome || r.duelAway).length,
    events,
  };
}

async function getJson(url, timeoutMs = 20000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      headers: { accept: "application/json" },
      signal: ctrl.signal,
    });
    const text = await res.text();
    let body = null;
    try { body = text ? JSON.parse(text) : null; } catch { body = text.slice(0, 240); }
    if (!res.ok) {
      const err = new Error("HTTP " + res.status + " " + url.split("?")[0]);
      err.status = res.status;
      err.body = body;
      throw err;
    }
    return body;
  } finally {
    clearTimeout(t);
  }
}

function withKey(pathName, params, key) {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params || {})) {
    if (v !== undefined && v !== null && v !== "") q.set(k, String(v));
  }
  q.set("apiKey", key);
  return BASE + pathName + "?" + q.toString();
}

export async function listBookmakers() {
  const data = await getJson(BASE + "/bookmakers");
  const names = Array.isArray(data) ? data.map((b) => b && b.name).filter(Boolean) : [];
  return { names, hasStake: names.includes("Stake"), hasDuel: names.includes("Duel") };
}

function extractMl(bookMarkets) {
  if (!Array.isArray(bookMarkets)) return { home: null, away: null, updated: null };
  for (const m of bookMarkets) {
    const name = String((m && m.name) || "").toUpperCase();
    if (!{"ML":1,"MONEYLINE":1,"MATCH WINNER":1,"WINNER":1}[name]) continue;
    const row = (m.odds && m.odds[0]) || null;
    if (!row) continue;
    const home = row.home == null ? null : Number(row.home);
    const away = row.away == null ? null : Number(row.away);
    return {
      home: Number.isFinite(home) ? home : null,
      away: Number.isFinite(away) ? away : null,
      updated: m.updatedAt || null,
    };
  }
  return { home: null, away: null, updated: null };
}

async function fetchEventsOnce(key) {
  const data = await getJson(withKey("/events", {
    sport: "esports",
    status: "pending,live",
    limit: 100,
  }, key));
  const all = Array.isArray(data) ? data : [];
  return all.filter((e) => isDotaOrLol(JSON.stringify(e)));
}

async function fetchOddsMulti(key, ids) {
  const out = [];
  for (let i = 0; i < ids.length; i += 10) {
    const chunk = ids.slice(i, i + 10);
    const data = await getJson(withKey("/odds/multi", {
      eventIds: chunk.join(","),
      bookmakers: BOOKS,
      markets: "ML",
    }, key));
    if (Array.isArray(data)) out.push(...data);
    else if (data && typeof data === "object") out.push(data);
  }
  return out;
}

function mapEvent(e, pack) {
  const books = (pack && pack.bookmakers) || {};
  const stake = extractMl(books.Stake);
  const duel = extractMl(books.Duel);
  const status = (e && e.status) || (pack && pack.status) || "";
  const live = String(status).toLowerCase() === "live";
  const league = (e && e.league) || {};
  return {
    id: e && e.id != null ? Number(e.id) : (pack && pack.id != null ? Number(pack.id) : null),
    home: (e && e.home) || (pack && pack.home) || "",
    away: (e && e.away) || (pack && pack.away) || "",
    date: (e && e.date) || (pack && pack.date) || null,
    status,
    live,
    league: league.name || null,
    leagueSlug: league.slug || null,
    stakeHome: stake.home,
    stakeAway: stake.away,
    stakeUpdated: stake.updated,
    duelHome: duel.home,
    duelAway: duel.away,
    duelUpdated: duel.updated,
    source: "odds-api.io",
  };
}

function mergePack(events, packed) {
  return events.map((e) => mapEvent(e, packed.get(Number(e.id))));
}

export async function pullStakeDuel() {
  const key = getOddsKey();
  const fetchedAt = Date.now();
  if (!key) {
    return {
      ok: false,
      status: "无key",
      error: "未配置 odds-api.io key",
      fetchedAt,
      events: [],
    };
  }
  try {
    const now = Date.now();
    if (!mem.events.length) {
      const disk = loadDisk();
      if (disk && Array.isArray(disk.events) && disk.events.length) {
        mem.events = disk.events;
        mem.at = disk.at || 0;
        mem.rows = disk.rows || [];
        mem.rowsAt = disk.fetchedAt || 0;
      }
    }

    let events = mem.events;
    if (!events.length || now - mem.at > EVENT_TTL_MS) {
      try {
        events = await fetchEventsOnce(key);
        mem.events = events;
        mem.at = now;
      } catch (err) {
        if (!events.length) throw err;
        console.error("oai events fallback to cache", err && err.message ? err.message : err);
      }
    }

    const ids = events.map((e) => Number(e.id)).filter((n) => Number.isFinite(n)).slice(0, 20);
    let rows;
    if (mem.rows.length && now - mem.rowsAt < ODDS_TTL_MS) {
      rows = mem.rows;
    } else if (ids.length) {
      const packed = new Map();
      const odds = await fetchOddsMulti(key, ids);
      for (const o of odds) {
        if (o && o.id != null) packed.set(Number(o.id), o);
      }
      rows = mergePack(events, packed);
      mem.rows = rows;
      mem.rowsAt = now;
      saveDisk({ at: mem.at, fetchedAt: now, events, rows });
    } else {
      rows = mergePack(events, new Map());
    }

    return {
      ok: true,
      status: "OK",
      fetchedAt,
      nEvents: rows.length,
      nStake: rows.filter((r) => r.stakeHome || r.stakeAway).length,
      nDuel: rows.filter((r) => r.duelHome || r.duelAway).length,
      events: rows,
    };
  } catch (err) {
    return lastGood(fetchedAt, err);
  }
}

