import { getPinGuestKey } from "../config.js";
import { americanToDecimal } from "../lib/arb.js";

const BASE = "https://guest.api.arcadia.pinnacle.com/0.1";
const ESPORTS = 12;
const TI_LEAGUE = 5055;
const LOL_NAME_RE = /league of legends|lck|lec|lpl|kespa/i;

async function getJson(url, { key, timeoutMs = 20000 } = {}) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  const headers = { accept: "application/json", "user-agent": "arb-radar-web/1.0" };
  if (key) headers["X-API-Key"] = key;
  try {
    let res = await fetch(url, { headers, signal: ctrl.signal });
    if (res.status === 401 && !key) {
      const guest = getPinGuestKey();
      if (guest) {
        headers["X-API-Key"] = guest;
        res = await fetch(url, { headers, signal: ctrl.signal });
      }
    }
    const text = await res.text();
    let body = null;
    try { body = text ? JSON.parse(text) : null; } catch { body = text.slice(0, 240); }
    if (!res.ok) {
      const err = new Error("HTTP " + res.status + " " + url);
      err.status = res.status;
      throw err;
    }
    return body;
  } finally {
    clearTimeout(t);
  }
}

function pickLeagues(leagues) {
  const out = [];
  const seen = new Set();
  for (const lg of leagues || []) {
    if (!lg || lg.id == null) continue;
    const id = Number(lg.id);
    const name = String(lg.name || "");
    const want = id === TI_LEAGUE || LOL_NAME_RE.test(name);
    if (!want || seen.has(id)) continue;
    seen.add(id);
    out.push({ id, name });
  }
  if (!seen.has(TI_LEAGUE)) out.unshift({ id: TI_LEAGUE, name: "Dota 2 - The International" });
  return out;
}

function rootMatchup(m) {
  if (!m || m.type !== "matchup") return false;
  if (m.parentId) return false;
  if (m.special) return false;
  const parts = m.participants || [];
  return parts.length === 2;
}

function limitFromMarket(mkt) {
  const limits = (mkt && mkt.limits) || [];
  for (const L of limits) {
    if (!L) continue;
    if (L.type === "maxRiskStake" || L.type === "limit" || L.type === "maxStake") {
      const n = Number(L.amount);
      if (Number.isFinite(n) && n > 0) return n;
    }
  }
  return null;
}

function moneylinePair(mkt, matchup) {
  if (!mkt || mkt.type !== "moneyline" || Number(mkt.period) !== 0) return null;
  if (mkt.status && String(mkt.status).toLowerCase() === "closed") return null;
  const prices = mkt.prices || [];
  const parts = matchup.participants || [];
  const home = parts.find((p) => p.alignment === "home") || parts[0];
  const away = parts.find((p) => p.alignment === "away") || parts[1];
  let homeAmer = null;
  let awayAmer = null;
  for (const pr of prices) {
    if (!pr) continue;
    const des = String(pr.designation || "").toLowerCase();
    if (des === "home") homeAmer = pr.price;
    else if (des === "away") awayAmer = pr.price;
    else if (home && pr.participantId != null && home.id != null && Number(pr.participantId) === Number(home.id)) {
      homeAmer = pr.price;
    } else if (away && pr.participantId != null && away.id != null && Number(pr.participantId) === Number(away.id)) {
      awayAmer = pr.price;
    }
  }
  return {
    home: americanToDecimal(homeAmer),
    away: americanToDecimal(awayAmer),
    limit: limitFromMarket(mkt),
  };
}

export async function pullPinnacle() {
  const fetchedAt = Date.now();
  const guest = getPinGuestKey();
  try {
    const leaguesRaw = await getJson(BASE + "/sports/" + ESPORTS + "/leagues?all=false", { key: guest });
    const leagues = pickLeagues(Array.isArray(leaguesRaw) ? leaguesRaw : []);
    const events = [];
    for (const lg of leagues) {
      let matchups = [];
      let markets = [];
      try {
        matchups = await getJson(BASE + "/leagues/" + lg.id + "/matchups", { key: guest });
        markets = await getJson(BASE + "/leagues/" + lg.id + "/markets/straight", { key: guest });
      } catch {
        continue;
      }
      if (!Array.isArray(matchups)) matchups = [];
      if (!Array.isArray(markets)) markets = [];
      const mlById = new Map();
      for (const mk of markets) {
        if (mk && mk.type === "moneyline" && Number(mk.period) === 0 && mk.matchupId != null) {
          mlById.set(Number(mk.matchupId), mk);
        }
      }
      for (const m of matchups) {
        if (!rootMatchup(m)) continue;
        const parts = m.participants || [];
        const home = (parts.find((p) => p.alignment === "home") || parts[0] || {}).name || "";
        const away = (parts.find((p) => p.alignment === "away") || parts[1] || {}).name || "";
        const ml = moneylinePair(mlById.get(Number(m.id)), m);
        const start = m.startTime || null;
        const live = Boolean(m.isLive) || String(m.status || "").toLowerCase() === "live";
        events.push({
          id: m.id,
          home,
          away,
          teamA: home,
          teamB: away,
          startTime: start,
          live,
          status: m.status || "",
          league: lg.name,
          leagueId: lg.id,
          bestOf: m.bestOfX || null,
          pinHome: ml ? ml.home : null,
          pinAway: ml ? ml.away : null,
          pinLimit: ml ? ml.limit : null,
          source: "pinnacle",
        });
      }
    }
    return {
      ok: true,
      status: "OK",
      fetchedAt,
      nEvents: events.length,
      nPriced: events.filter((e) => e.pinHome || e.pinAway).length,
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
