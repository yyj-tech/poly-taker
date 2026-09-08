import { WATCHLIST, isDotaOrLol } from "../lib/match.js";

const GAMMA = "https://gamma-api.polymarket.com";
const CLOB = "https://clob.polymarket.com";

const SEARCHES = [
  "Iron Wing vs Team Spirit",
  "Gen.G vs KT Rolster",
  "TEAM VISION vs BoomBoys",
  "DRX Challengers vs Hanwha",
  "Team Liquid vs Team Yandex",
  "Nigma Galaxy vs Team Falcons",
  "T1 vs DN SOOPers",
  "Dplus KIA Challengers vs KT Rolster Challengers",
  "GIANTX vs Karmine",
  "NAVI vs Heretics",
  "Natus Vincere vs Heretics",
  "Team Heretics vs Natus Vincere",
  "The International Playoffs",
  "LCK Challengers",
  "LEC Summer",
  "KeSPA Cup",
];

async function getJson(url, timeoutMs = 20000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      headers: { accept: "application/json", "user-agent": "arb-radar-web/1.0" },
      signal: ctrl.signal,
    });
    const text = await res.text();
    let body = null;
    try { body = text ? JSON.parse(text) : null; } catch { body = null; }
    if (!res.ok) {
      const err = new Error("HTTP " + res.status);
      err.status = res.status;
      throw err;
    }
    return body;
  } finally {
    clearTimeout(t);
  }
}

function parseMaybeJson(v) {
  if (Array.isArray(v)) return v;
  if (typeof v === "string") {
    try { return JSON.parse(v); } catch { return []; }
  }
  return [];
}

function isMatchWinnerMarket(m) {
  if (!m || m.closed) return false;
  const group = String(m.groupItemTitle || "").toLowerCase();
  const q = String(m.question || "").toLowerCase();
  if (group.includes("game 1") || group.includes("game 2") || group.includes("game 3") || group.includes("game 4") || group.includes("game 5")) return false;
  if (group.includes("o/u") || group.includes("total") || group.includes("spread") || group.includes("map")) return false;
  if (group.includes("match winner") || group === "winner") return true;
  const outcomes = parseMaybeJson(m.outcomes).map((x) => String(x).toLowerCase());
  if (outcomes.includes("over") || outcomes.includes("under")) return false;
  if (outcomes.length === 2 && !outcomes.includes("yes") && !outcomes.includes("no")) {
    if (q.includes("game 1") || q.includes("game 2")) return false;
    return true;
  }
  return false;
}

function eventLooksUseful(ev) {
  if (!ev || ev.closed) return false;
  const title = String(ev.title || "");
  if (title.toLowerCase().indexOf(" vs") < 0) return false;
  return isDotaOrLol(title + " " + (ev.slug || ""));
}

async function searchEvents(q) {
  const data = await getJson(GAMMA + "/public-search?q=" + encodeURIComponent(q));
  const evs = data && Array.isArray(data.events) ? data.events : [];
  return evs.filter(eventLooksUseful);
}

async function tagEvents(slug) {
  const data = await getJson(GAMMA + "/events?tag_slug=" + encodeURIComponent(slug) + "&closed=false&limit=80");
  const evs = Array.isArray(data) ? data : [];
  return evs.filter(eventLooksUseful);
}

function bestAsk(book) {
  const asks = (book && book.asks) || [];
  let best = null;
  for (const a of asks) {
    const price = Number(a && a.price);
    const size = Number(a && a.size);
    if (!Number.isFinite(price) || !Number.isFinite(size) || price <= 0 || size <= 0) continue;
    if (!best || price < best.price) best = { price, size };
  }
  return best;
}

async function loadBook(tokenId) {
  if (!tokenId) return null;
  const book = await getJson(CLOB + "/book?token_id=" + encodeURIComponent(tokenId));
  const ask = bestAsk(book);
  return {
    ask: ask ? ask.price : null,
    size: ask ? ask.size : 0,
    ts: book && book.timestamp ? Number(book.timestamp) : Date.now(),
  };
}

function parseTeamsFromTitle(title) {
  const m = String(title || "").match(/^(?:Dota 2|LoL|League of Legends)?:?\s*(.+?)\s+vs\.?\s+(.+?)\s*(?:\(|-|$)/i);
  if (!m) return null;
  return { home: m[1].trim(), away: m[2].trim() };
}

export async function pullPolymarket() {
  const fetchedAt = Date.now();
  try {
    const byId = new Map();
    const queries = SEARCHES.concat(WATCHLIST.map((w) => w.teamA + " vs " + w.teamB));
    for (const q of queries) {
      try {
        for (const ev of await searchEvents(q)) {
          if (ev && ev.id != null) byId.set(String(ev.id), ev);
        }
      } catch {
        // one query failed
      }
    }
    for (const slug of ["dota-2", "league-of-legends"]) {
      try {
        for (const ev of await tagEvents(slug)) {
          if (ev && ev.id != null) byId.set(String(ev.id), ev);
        }
      } catch {
        // tag list failed
      }
    }

    const events = [];
    const jobs = [];
    for (const ev of byId.values()) {
      const markets = ev.markets || [];
      const mw = markets.find(isMatchWinnerMarket);
      if (!mw) continue;
      const outcomes = parseMaybeJson(mw.outcomes);
      const tokens = parseMaybeJson(mw.clobTokenIds);
      if (outcomes.length < 2 || tokens.length < 2) continue;
      const parsed = parseTeamsFromTitle(ev.title) || { home: outcomes[0], away: outcomes[1] };
      const rec = {
        id: ev.id,
        slug: ev.slug,
        title: ev.title,
        home: parsed.home,
        away: parsed.away,
        teamA: parsed.home,
        teamB: parsed.away,
        startTime: ev.startTime || ev.startDate || mw.endDate || ev.endDate || null,
        live: Boolean(ev.live),
        league: ev.title,
        pmHomeAsk: null,
        pmAwayAsk: null,
        pmHomeSize: 0,
        pmAwaySize: 0,
        pmHomeTs: null,
        pmAwayTs: null,
        source: "polymarket",
      };
      events.push(rec);
      jobs.push({ rec, tokenA: tokens[0], tokenB: tokens[1], outA: outcomes[0], outB: outcomes[1] });
    }

    const concurrency = 8;
    let i = 0;
    async function worker() {
      while (i < jobs.length) {
        const idx = i++;
        const job = jobs[idx];
        try {
          const [ba, bb] = await Promise.all([loadBook(job.tokenA), loadBook(job.tokenB)]);
          job.rec.pmHomeAsk = ba && ba.ask;
          job.rec.pmHomeSize = ba && ba.size || 0;
          job.rec.pmHomeTs = ba && ba.ts;
          job.rec.pmAwayAsk = bb && bb.ask;
          job.rec.pmAwaySize = bb && bb.size || 0;
          job.rec.pmAwayTs = bb && bb.ts;
        } catch {
          // leave nulls
        }
      }
    }
    await Promise.all(Array.from({ length: Math.min(concurrency, jobs.length || 1) }, () => worker()));

    return {
      ok: true,
      status: "OK",
      fetchedAt,
      nEvents: events.length,
      nPriced: events.filter((e) => e.pmHomeAsk || e.pmAwayAsk).length,
      events,
    };
  } catch (err) {
    return {
      ok: false,
      status: "失败",
      error: err && err.message ? err.message : String(err),
      fetchedAt,
      events: [],
    };
  }
}
