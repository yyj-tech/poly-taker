export const WATCHLIST = [
  { event: "Iron Wing vs Spirit", teamA: "Iron Wing", teamB: "Spirit" },
  { event: "GEN vs KT", teamA: "GEN", teamB: "KT" },
  { event: "VISION vs BoomBoys", teamA: "VISION", teamB: "BoomBoys" },
  { event: "DRX.C vs HLE.C", teamA: "DRX.C", teamB: "HLE.C" },
  { event: "Liquid vs Yandex", teamA: "Liquid", teamB: "Yandex" },
  { event: "NGX vs Falcons", teamA: "NGX", teamB: "Falcons" },
  { event: "T1 vs DNS", teamA: "T1", teamB: "DNS" },
  { event: "DK.C vs KT.C", teamA: "DK.C", teamB: "KT.C" },
  { event: "GX vs KC", teamA: "GX", teamB: "KC" },
  { event: "NAVI vs Heretics", teamA: "NAVI", teamB: "Heretics" },
];

const ALIASES = {
  "iron wing": ["iron wing", "1w", "1win", "1w team"],
  spirit: ["spirit", "team spirit"],
  vision: ["vision", "parivision", "team vision", "pvision"],
  boomboys: ["boomboys", "boom boys", "betboom", "betboom team", "bb team"],
  liquid: ["liquid", "team liquid"],
  yandex: ["yandex", "team yandex"],
  ngx: ["ngx", "nigma", "nigma galaxy"],
  falcons: ["falcons", "team falcons"],
  gen: ["gen", "gen g", "geng"],
  kt: ["kt", "kt rolster"],
  "drx.c": ["drx.c", "drx challengers", "kiwoom drx challengers"],
  "hle.c": ["hle.c", "hle challengers", "hanwha", "hanwha life challengers"],
  "dk.c": ["dk.c", "dk challengers", "dplus", "dplus kia challengers"],
  "kt.c": ["kt.c", "kt challengers", "kt rolster challengers"],
  t1: ["t1"],
  dns: ["dns", "dn souls", "dn soopers", "dn souz"],
  gx: ["gx", "giantx", "giant x"],
  kc: ["kc", "karmine", "karmine corp"],
  navi: ["navi", "natus vincere"],
  heretics: ["heretics", "team heretics", "th"],
};

const SPECIFIC_FIRST = [
  "kt.c", "drx.c", "hle.c", "dk.c",
  "iron wing", "boomboys", "heretics", "falcons", "liquid", "yandex",
  "vision", "spirit", "navi", "dns", "ngx", "gx", "kc", "gen", "kt", "t1",
];

const SHORT = new Set(["th", "kt", "gx", "kc", "dk", "t1", "ngx", "gen", "1w"]);

export function normalize(name) {
  return String(name || "")
    .toLowerCase()
    .replace(/[._-]+/g, " ")
    .replace(/[^a-z0-9 ]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function words(n) {
  return n.split(" ").filter(Boolean);
}

function aliasHit(normName, alias) {
  if (normName === alias) return true;
  if (SHORT.has(alias)) return words(normName).includes(alias);
  return normName.includes(alias) || alias.includes(normName);
}

export function teamTokens(name) {
  const n = normalize(name);
  const toks = new Set([n, ...words(n)]);
  const challenger = n.includes("challenger") || n.split(" ").includes("c");
  for (const key of SPECIFIC_FIRST) {
    const alts = ALIASES[key] || [key];
    const isC = key.endsWith(".c");
    if (isC && !challenger && !alts.some((a) => n === a)) continue;
    if (!isC && (key === "kt" || key === "dk" || key === "gen") && challenger) continue;
    const hit = n === key || alts.some((a) => aliasHit(n, a));
    if (hit) {
      toks.add(key);
      for (const a of alts) toks.add(a);
    }
  }
  return toks;
}

export function sameTeam(a, b) {
  if (!a || !b) return false;
  const ta = teamTokens(a);
  const tb = teamTokens(b);
  for (const t of ta) {
    if (tb.has(t)) return true;
  }
  return false;
}

export function pairMatch(a1, b1, a2, b2) {
  if (sameTeam(a1, a2) && sameTeam(b1, b2)) return { matched: true, flipped: false };
  if (sameTeam(a1, b2) && sameTeam(b1, a2)) return { matched: true, flipped: true };
  return null;
}

export function findPair(list, teamA, teamB) {
  for (const item of list || []) {
    const a = item.teamA || item.home || item.a;
    const b = item.teamB || item.away || item.b;
    const hit = pairMatch(teamA, teamB, a, b);
    if (hit) return { item, flipped: hit.flipped };
  }
  return null;
}

export function isDotaOrLol(blob) {
  const s = String(blob || "").toLowerCase();
  return [
    "dota",
    "league of legends",
    "league-of-legends",
    "lck",
    "lpl",
    "lec",
    "lcs",
    "kespa",
    "the international",
    "lol:",
    "lol ",
  ].some((k) => s.includes(k));
}
