export const HIGH_VALUE_RATE = 0.015;
export const PIN_PM_RULE_NOTE = "规则不一致（PM 延期窗口/50-50 vs PIN 超时 void）";

export function americanToDecimal(american) {
  const n = Number(american);
  if (!Number.isFinite(n) || n === 0) return null;
  const dec = n > 0 ? n / 100 + 1 : 100 / Math.abs(n) + 1;
  return Math.round(dec * 1000) / 1000;
}

export function toNum(v) {
  if (v === null || v === undefined || v === "") return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

export function pmFee(spend, p) {
  const s = Number(spend);
  const price = Number(p);
  if (!Number.isFinite(s) || !Number.isFinite(price)) return 0;
  return s * 0.05 * price * (1 - price);
}

export function sizePosition({ askSize, odds, ask, pinLimit }) {
  const S0 = toNum(askSize);
  const O = toNum(odds);
  const p = toNum(ask);
  if (!S0 || S0 <= 0 || !O || O <= 1 || !p || p <= 0 || p >= 1) return null;
  let shares = S0;
  let D = shares / O;
  let limitNote = pinLimit ? ("PIN限额" + pinLimit) : "限额未知";
  const L = toNum(pinLimit);
  if (L && L > 0 && D > L) {
    D = L;
    shares = D * O;
  }
  const spend = shares * p;
  const fee = pmFee(spend, p);
  const cost = D + spend + fee;
  const profit = shares - cost;
  const rate = cost > 0 ? profit / cost : 0;
  return { D, S: shares, spend, fee, cost, profit, rate, limitNote, O, p };
}

function fmtU(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return "—";
  return (Math.round(x * 10) / 10).toFixed(1);
}

function fmtOdds(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return "—";
  return x.toFixed(3);
}

function fmtAsk(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return "—";
  return x.toFixed(3);
}

export function formatSettle(iso) {
  if (!iso) return "未知";
  const t = new Date(iso);
  if (Number.isNaN(t.getTime())) return "未知";
  const now = Date.now();
  const ms = t.getTime() - now;
  const abs = Math.abs(ms);
  const hours = abs / 3600000;
  let rel;
  if (hours < 1) rel = Math.round(abs / 60000) + "分钟";
  else if (hours < 48) rel = (Math.round(hours * 10) / 10) + "小时";
  else rel = (Math.round((hours / 24) * 10) / 10) + "天";
  const sh = new Date(t.getTime() + 8 * 3600000);
  const md = (sh.getUTCMonth() + 1) + "/" + sh.getUTCDate();
  const hh = String(sh.getUTCHours()).padStart(2, "0");
  const mm = String(sh.getUTCMinutes()).padStart(2, "0");
  if (ms < 0) return "已开赛（" + md + " " + hh + ":" + mm + "）";
  return "约" + rel + "（" + md + " " + hh + ":" + mm + "）";
}

export function bestPosition(row) {
  const books = [
    { name: "PIN", a: row.pinA, b: row.pinB, limit: row.pinLimit, rulesOk: false },
    { name: "Stake", a: row.stakeA, b: row.stakeB, limit: null, rulesOk: true },
    { name: "Duel", a: row.duelA, b: row.duelB, limit: null, rulesOk: true },
  ];
  const sides = [
    { bookSide: "a", bookTeam: row.teamA, pmAsk: row.pmB, pmSize: row.pmBSize, pmTeam: row.teamB },
    { bookSide: "b", bookTeam: row.teamB, pmAsk: row.pmA, pmSize: row.pmASize, pmTeam: row.teamA },
  ];
  let best = null;
  for (const book of books) {
    for (const side of sides) {
      const odds = side.bookSide === "a" ? book.a : book.b;
      const sized = sizePosition({
        askSize: side.pmSize,
        odds,
        ask: side.pmAsk,
        pinLimit: book.name === "PIN" ? book.limit : null,
      });
      if (!sized) continue;
      const cand = {
        book: book.name,
        rulesOk: book.rulesOk,
        ruleNote: book.rulesOk ? "" : PIN_PM_RULE_NOTE,
        leftBuy: book.name + " 买" + side.bookTeam + " " + fmtU(sized.D) + "U @" + fmtOdds(sized.O),
        rightBuy: "PM 买" + side.pmTeam + " " + fmtU(sized.S) + "份 @" + fmtAsk(sized.p),
        cost: sized.cost,
        fee: sized.fee,
        rate: sized.rate,
        profit: sized.profit,
        limitNote: sized.limitNote,
        highValue: book.rulesOk && sized.rate >= HIGH_VALUE_RATE,
      };
      if (!best || cand.profit > best.profit) best = cand;
    }
  }
  return best;
}

export function isStale(ts, maxMs) {
  if (!ts) return false;
  const t = typeof ts === "number" ? ts : Date.parse(ts);
  if (!Number.isFinite(t)) return false;
  return Date.now() - t > (maxMs || 30 * 60 * 1000);
}
