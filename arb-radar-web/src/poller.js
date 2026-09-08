import { getPollSec } from "./config.js";
import { WATCHLIST, findPair } from "./lib/match.js";
import { bestPosition, formatSettle, isStale } from "./lib/arb.js";
import { pullStakeDuel } from "./sources/oddsApiIo.js";
import { pullPinnacle } from "./sources/pinnacle.js";
import { pullPolymarket } from "./sources/polymarket.js";

const STALE_MS = 30 * 60 * 1000;
const MAX_ROWS = 20;

let snapshot = emptySnapshot();
let timer = null;
const clients = new Set();
let onPollSec = null;
let inflight = null;

function emptySnapshot() {
  return {
    type: "snapshot",
    ts: Date.now(),
    tsShanghai: shanghaiNow(),
    sources: {
      oddsApiIo: { status: "—", error: null, fetchedAt: null },
      pinnacle: { status: "—", error: null, fetchedAt: null },
      polymarket: { status: "—", error: null, fetchedAt: null },
    },
    highValueCount: 0,
    prices: [],
    positions: [],
  };
}

function shanghaiNow(ms) {
  const t = new Date((ms || Date.now()) + 8 * 3600000);
  const y = t.getUTCFullYear();
  const mo = String(t.getUTCMonth() + 1).padStart(2, "0");
  const d = String(t.getUTCDate()).padStart(2, "0");
  const h = String(t.getUTCHours()).padStart(2, "0");
  const mi = String(t.getUTCMinutes()).padStart(2, "0");
  const s = String(t.getUTCSeconds()).padStart(2, "0");
  return y + "-" + mo + "-" + d + " " + h + ":" + mi + ":" + s + " CST";
}

function sideOf(hit, homeKey, awayKey) {
  if (!hit) return { a: null, b: null, extra: {} };
  const item = hit.item;
  if (hit.flipped) return { a: item[awayKey], b: item[homeKey], extra: item };
  return { a: item[homeKey], b: item[awayKey], extra: item };
}

function alreadyListed(rows, teamA, teamB) {
  return rows.some((r) => findPair([{ teamA: r.teamA, teamB: r.teamB }], teamA, teamB));
}

function liveOf(oai, pin, pm, start) {
  if (oai && oai.live) return true;
  if (pin && pin.live) return true;
  if (pm && pm.live) return true;
  if (start && Date.parse(start) < Date.now()) return true;
  return false;
}

function buildRow(label, teamA, teamB, oaiHit, pinHit, pmHit, watch) {
  const oai = oaiHit && oaiHit.item;
  const pin = pinHit && pinHit.item;
  const pm = pmHit && pmHit.item;
  const stake = sideOf(oaiHit, "stakeHome", "stakeAway");
  const duel = sideOf(oaiHit, "duelHome", "duelAway");
  const pinP = sideOf(pinHit, "pinHome", "pinAway");
  const pmP = sideOf(pmHit, "pmHomeAsk", "pmAwayAsk");
  const pmS = sideOf(pmHit, "pmHomeSize", "pmAwaySize");
  const start = (pin && pin.startTime) || (oai && oai.date) || (pm && pm.startTime) || null;
  const live = liveOf(oai, pin, pm, start);
  const stakeTs = oaiHit && oaiHit.flipped ? oai && oai.stakeUpdated : oai && oai.stakeUpdated;
  const duelTs = oai && oai.duelUpdated;
  const pmATs = pmHit && pmHit.flipped ? pm && pm.pmAwayTs : pm && pm.pmHomeTs;
  const pmBTs = pmHit && pmHit.flipped ? pm && pm.pmHomeTs : pm && pm.pmAwayTs;
  const row = {
    watch: Boolean(watch),
    status: live ? "滚球" : "非滚球",
    event: label,
    teamA,
    teamB,
    startTime: start,
    league: (oai && oai.league) || (pin && pin.league) || "",
    pmA: pmP.a,
    pmB: pmP.b,
    pmASize: pmHit && pmHit.flipped ? (pm && pm.pmAwaySize) : (pm && pm.pmHomeSize) || 0,
    pmBSize: pmHit && pmHit.flipped ? (pm && pm.pmHomeSize) : (pm && pm.pmAwaySize) || 0,
    pmAStale: isStale(pmATs, STALE_MS),
    pmBStale: isStale(pmBTs, STALE_MS),
    pinA: pinP.a,
    pinB: pinP.b,
    pinLimit: pin && pin.pinLimit,
    pinStale: false,
    stakeA: stake.a,
    stakeB: stake.b,
    stakeStale: isStale(stakeTs, STALE_MS),
    duelA: duel.a,
    duelB: duel.b,
    duelStale: isStale(duelTs, STALE_MS),
  };
  return row;
}

function align(oai, pin, pm) {
  const oaiE = (oai && oai.events) || [];
  const pinE = (pin && pin.events) || [];
  const pmE = (pm && pm.events) || [];
  const prices = [];

  for (const w of WATCHLIST) {
    prices.push(buildRow(
      w.event,
      w.teamA,
      w.teamB,
      findPair(oaiE, w.teamA, w.teamB),
      findPair(pinE, w.teamA, w.teamB),
      findPair(pmE, w.teamA, w.teamB),
      true,
    ));
  }

  for (const ev of oaiE) {
    if (prices.length >= MAX_ROWS) break;
    const hasBook = ev.stakeHome || ev.stakeAway || ev.duelHome || ev.duelAway;
    if (!hasBook) continue;
    if (alreadyListed(prices, ev.home, ev.away)) continue;
    const pinHit = findPair(pinE, ev.home, ev.away);
    const pmHit = findPair(pmE, ev.home, ev.away);
    if (!pinHit && !pmHit) continue;
    prices.push(buildRow(
      ev.home + " vs " + ev.away,
      ev.home,
      ev.away,
      { item: ev, flipped: false },
      pinHit,
      pmHit,
      false,
    ));
  }

  const positions = [];
  for (const row of prices) {
    const pos = bestPosition(row);
    if (!pos) {
      positions.push({
        status: row.status,
        event: row.event,
        leftBuy: "—",
        rightBuy: "—",
        cost: null,
        fee: null,
        rate: null,
        settle: formatSettle(row.startTime),
        profit: null,
        highValue: false,
        ruleNote: "",
        limitNote: row.pinLimit ? ("PIN限额" + row.pinLimit) : "限额未知",
      });
      continue;
    }
    const noteBits = [pos.limitNote, pos.ruleNote].filter(Boolean);
    positions.push({
      status: row.status,
      event: noteBits.length ? row.event + "（" + noteBits.join("；") + "）" : row.event,
      leftBuy: pos.leftBuy,
      rightBuy: pos.rightBuy,
      cost: pos.cost,
      fee: pos.fee,
      rate: pos.rate,
      settle: formatSettle(row.startTime),
      profit: pos.profit,
      highValue: pos.highValue,
      ruleNote: pos.ruleNote,
      limitNote: pos.limitNote,
    });
  }
  positions.sort((a, b) => (Number(b.profit) || -1e18) - (Number(a.profit) || -1e18));
  return { prices, positions, highValueCount: positions.filter((p) => p.highValue).length };
}

export function getSnapshot() {
  return snapshot;
}

export function addClient(res) {
  clients.add(res);
  res.on("close", () => clients.delete(res));
}

function broadcast(payload) {
  const data = "data: " + JSON.stringify(payload) + String.fromCharCode(10,10);
  for (const res of clients) {
    try { res.write(data); } catch { clients.delete(res); }
  }
}

export function refreshNow() {
  if (inflight) return inflight;
  inflight = (async () => {
    const [oai, pin, pm] = await Promise.all([
      pullStakeDuel(),
      pullPinnacle(),
      pullPolymarket(),
    ]);
    const aligned = align(oai, pin, pm);
    snapshot = {
      type: "snapshot",
      ts: Date.now(),
      tsShanghai: shanghaiNow(),
      sources: {
        oddsApiIo: { status: oai.status, error: oai.error || null, fetchedAt: oai.fetchedAt, nEvents: oai.nEvents || 0 },
        pinnacle: { status: pin.status, error: pin.error || null, fetchedAt: pin.fetchedAt, nEvents: pin.nEvents || 0 },
        polymarket: { status: pm.status, error: pm.error || null, fetchedAt: pm.fetchedAt, nEvents: pm.nEvents || 0 },
      },
      highValueCount: aligned.highValueCount,
      prices: aligned.prices,
      positions: aligned.positions,
    };
    broadcast(snapshot);
    return snapshot;
  })().finally(() => { inflight = null; });
  return inflight;
}

function schedule() {
  if (timer) clearTimeout(timer);
  const sec = getPollSec();
  timer = setTimeout(async () => {
    try { await refreshNow(); } catch (e) { console.error("poll failed", e && e.message ? e.message : e); }
    schedule();
  }, sec * 1000);
}

export function startPoller() {
  refreshNow().catch((e) => console.error("first poll failed", e && e.message ? e.message : e));
  schedule();
  onPollSec = setInterval(() => {
    // interval handle kept so pollSec hot-change is picked up by schedule()
  }, 60000);
}

export function reschedule() {
  schedule();
}

export function heartbeat() {
  setInterval(() => {
    for (const res of clients) {
      try { res.write(": ping" + String.fromCharCode(10,10)); } catch { clients.delete(res); }
    }
  }, 25000);
}
