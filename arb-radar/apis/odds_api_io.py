#!/usr/bin/env python3
"""odds-api.io client for Stake / Duel esports moneyline.

Read-only. No browser, no bets. Key from ODDS_API_IO_KEY / ODDS_API_KEY
or /workspace/arb-radar/apis/.odds_api_io_key
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE = "https://api.odds-api.io/v3"
KEY_FILE = Path(__file__).resolve().parent / ".odds_api_io_key"
BOOKS = ("Stake", "Duel")
SPORT = "esports"

# Team aliases: any token on the left matches any token on the right.
ALIASES = {
    "iron wing": {"iron wing", "1w", "1win", "1w team"},
    "spirit": {"spirit", "team spirit"},
    "vision": {"vision", "parivision", "team vision"},
    "boomboys": {"boomboys", "boom boys", "betboom", "betboom team"},
    "liquid": {"liquid", "team liquid"},
    "yandex": {"yandex", "team yandex"},
    "ngx": {"ngx", "nigma", "nigma galaxy"},
    "falcons": {"falcons", "team falcons"},
    "gen": {"gen", "gen.g", "geng"},
    "kt": {"kt", "kt rolster"},
    "drx.c": {"drx.c", "drx challengers", "drx"},
    "hle.c": {"hle.c", "hle challengers", "hanwha", "hle"},
    "dk.c": {"dk.c", "dk challengers", "dplus", "dk"},
    "kt.c": {"kt.c", "kt challengers"},
    "t1": {"t1"},
    "dns": {"dns", "dn souls", "dn souz"},
    "gx": {"gx", "giantx", "giant x"},
    "kc": {"kc", "karmine", "karmine corp"},
    "navi": {"navi", "natus vincere"},
    "heretics": {"heretics", "team heretics", "th"},
}


def load_key() -> str | None:
    for env in ("ODDS_API_IO_KEY", "ODDS_API_KEY"):
        v = os.environ.get(env)
        if v:
            return v.strip()
    if KEY_FILE.exists():
        return KEY_FILE.read_text().strip() or None
    # connector credential dump, if the user saved via secret-request
    for p in Path("/home/box").glob("**/*odds-api*"):
        if p.is_file() and p.stat().st_size < 4096:
            try:
                txt = p.read_text()
            except OSError:
                continue
            if txt.startswith("{") and "apiKey" in txt:
                try:
                    return json.loads(txt).get("apiKey")
                except json.JSONDecodeError:
                    pass
            if re.fullmatch(r"[A-Za-z0-9_\-]{16,}", txt.strip()):
                return txt.strip()
    return None


def _get(path: str, params: dict[str, Any], key: str, timeout: int = 25) -> Any:
    q = {k: v for k, v in params.items() if v is not None}
    q["apiKey"] = key
    url = f"{BASE}{path}?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(url, headers={"accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            body = raw[:400]
        raise RuntimeError(f"HTTP {e.code} {path}: {body}") from e


def bookmakers() -> list[str]:
    req = urllib.request.Request(f"{BASE}/bookmakers", headers={"accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    return [b["name"] for b in data if isinstance(b, dict) and b.get("name")]


def leagues(key: str, sport: str = SPORT, all_leagues: bool = False) -> list[dict[str, Any]]:
    return _get("/leagues", {"sport": sport, "all": str(all_leagues).lower()}, key)


def events(
    key: str,
    sport: str = SPORT,
    league: str | None = None,
    status: str = "pending,live",
    bookmaker: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    return _get(
        "/events",
        {
            "sport": sport,
            "league": league,
            "status": status,
            "bookmaker": bookmaker,
            "limit": limit,
        },
        key,
    )


def odds_multi(key: str, event_ids: list[int], books: tuple[str, ...] = BOOKS) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for i in range(0, len(event_ids), 10):
        chunk = event_ids[i : i + 10]
        data = _get(
            "/odds/multi",
            {
                "eventIds": ",".join(str(x) for x in chunk),
                "bookmakers": ",".join(books),
                "markets": "ML",
            },
            key,
        )
        if isinstance(data, list):
            out.extend(data)
        elif isinstance(data, dict):
            out.append(data)
        time.sleep(0.15)
    return out


def _norm(s: str) -> str:
    s = s.lower().replace(".", " ").replace("-", " ")
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _tokens(name: str) -> set[str]:
    n = _norm(name)
    toks = {n}
    for canon, alts in ALIASES.items():
        if n == canon or n in alts or any(a in n or n in a for a in alts):
            toks |= alts | {canon}
    return toks


def same_team(a: str, b: str) -> bool:
    return bool(_tokens(a) & _tokens(b))


def extract_ml(book_markets: Any) -> tuple[float | None, float | None, str | None]:
    """Return (home, away, updatedAt) from a bookmaker's market list."""
    if not isinstance(book_markets, list):
        return None, None, None
    for m in book_markets:
        name = str(m.get("name") or "").upper()
        if name not in {"ML", "MONEYLINE", "MATCH WINNER", "WINNER"}:
            continue
        rows = m.get("odds") or []
        if not rows:
            continue
        row = rows[0]
        try:
            home = float(row["home"]) if row.get("home") is not None else None
            away = float(row["away"]) if row.get("away") is not None else None
        except (TypeError, ValueError):
            home = away = None
        return home, away, m.get("updatedAt")
    return None, None, None


def is_dota_or_lol(ev: dict[str, Any]) -> bool:
    blob = json.dumps(ev, ensure_ascii=False).lower()
    return any(
        k in blob
        for k in (
            "dota",
            "league of legends",
            "lck",
            "lpl",
            "lec",
            "lcs",
            "kespa",
            "the international",
        )
    )


def pull_stake_duel(key: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    lg = leagues(key)
    interesting = [
        x
        for x in lg
        if any(
            k in (x.get("name", "") + " " + x.get("slug", "")).lower()
            for k in ("dota", "league-of-legends", "lol", "lck", "lpl", "lec", "international")
        )
    ]
    evs: list[dict[str, Any]] = []
    if interesting:
        for x in interesting:
            try:
                evs.extend(events(key, league=x.get("slug"), limit=100))
            except RuntimeError:
                continue
            time.sleep(0.15)
    if not evs:
        evs = events(key, limit=300)
        evs = [e for e in evs if is_dota_or_lol(e)]

    # de-dupe
    by_id: dict[int, dict[str, Any]] = {}
    for e in evs:
        if isinstance(e, dict) and e.get("id") is not None:
            by_id[int(e["id"])] = e
    evs = list(by_id.values())

    rows = []
    if evs:
        packed = {int(o["id"]): o for o in odds_multi(key, [int(e["id"]) for e in evs]) if o.get("id") is not None}
        for e in evs:
            oid = int(e["id"])
            pack = packed.get(oid, {})
            books = pack.get("bookmakers") or {}
            stake_h, stake_a, stake_ts = extract_ml(books.get("Stake"))
            duel_h, duel_a, duel_ts = extract_ml(books.get("Duel"))
            status = e.get("status") or pack.get("status") or ""
            live = status.lower() == "live"
            rows.append(
                {
                    "id": oid,
                    "home": e.get("home") or pack.get("home"),
                    "away": e.get("away") or pack.get("away"),
                    "date": e.get("date") or pack.get("date"),
                    "status": status,
                    "live": live,
                    "league": (e.get("league") or {}).get("name"),
                    "league_slug": (e.get("league") or {}).get("slug"),
                    "stake_home": stake_h,
                    "stake_away": stake_a,
                    "stake_updated": stake_ts,
                    "duel_home": duel_h,
                    "duel_away": duel_a,
                    "duel_updated": duel_ts,
                    "source": "odds-api.io",
                }
            )

    return {
        "ts_utc": now,
        "source": "odds-api.io",
        "books": list(BOOKS),
        "league_hits": interesting,
        "n_events": len(rows),
        "n_with_stake": sum(1 for r in rows if r["stake_home"] or r["stake_away"]),
        "n_with_duel": sum(1 for r in rows if r["duel_home"] or r["duel_away"]),
        "events": rows,
    }


def match_watch(watch: list[dict[str, str]], pulled: dict[str, Any]) -> list[dict[str, Any]]:
    """Fill Stake/Duel columns for a watchlist of {event, team_a, team_b}."""
    out = []
    for w in watch:
        a, b = w["team_a"], w["team_b"]
        hit = None
        flipped = False
        for ev in pulled.get("events") or []:
            if same_team(a, ev["home"]) and same_team(b, ev["away"]):
                hit, flipped = ev, False
                break
            if same_team(a, ev["away"]) and same_team(b, ev["home"]):
                hit, flipped = ev, True
                break
        if not hit:
            out.append({**w, "stake_a": None, "stake_b": None, "duel_a": None, "duel_b": None, "oai_id": None})
            continue
        if flipped:
            stake_a, stake_b = hit["stake_away"], hit["stake_home"]
            duel_a, duel_b = hit["duel_away"], hit["duel_home"]
        else:
            stake_a, stake_b = hit["stake_home"], hit["stake_away"]
            duel_a, duel_b = hit["duel_home"], hit["duel_away"]
        out.append(
            {
                **w,
                "stake_a": stake_a,
                "stake_b": stake_b,
                "duel_a": duel_a,
                "duel_b": duel_b,
                "oai_id": hit["id"],
                "oai_live": hit["live"],
                "oai_league": hit["league"],
                "stake_updated": hit["stake_updated"],
                "duel_updated": hit["duel_updated"],
            }
        )
    return out


DEFAULT_WATCH = [
    {"event": "Iron Wing vs Spirit", "team_a": "Iron Wing", "team_b": "Spirit"},
    {"event": "GEN vs KT", "team_a": "GEN", "team_b": "KT"},
    {"event": "VISION vs BoomBoys", "team_a": "VISION", "team_b": "BoomBoys"},
    {"event": "DRX.C vs HLE.C", "team_a": "DRX.C", "team_b": "HLE.C"},
    {"event": "Liquid vs Yandex", "team_a": "Liquid", "team_b": "Yandex"},
    {"event": "NGX vs Falcons", "team_a": "NGX", "team_b": "Falcons"},
    {"event": "T1 vs DNS", "team_a": "T1", "team_b": "DNS"},
    {"event": "DK.C vs KT.C", "team_a": "DK.C", "team_b": "KT.C"},
    {"event": "GX vs KC", "team_a": "GX", "team_b": "KC"},
    {"event": "NAVI vs Heretics", "team_a": "NAVI", "team_b": "Heretics"},
]


def main() -> int:
    names = bookmakers()
    print(f"catalog {len(names)} Stake={'Stake' in names} Duel={'Duel' in names}")
    key = load_key()
    if not key:
        print("NO_KEY: set ODDS_API_IO_KEY or write apis/.odds_api_io_key")
        return 2
    pulled = pull_stake_duel(key)
    matched = match_watch(DEFAULT_WATCH, pulled)
    out_dir = Path(__file__).resolve().parents[1] / "scans"
    out_dir.mkdir(exist_ok=True)
    raw_path = out_dir / "odds-api-io-latest.json"
    match_path = out_dir / "odds-api-io-matched.json"
    raw_path.write_text(json.dumps(pulled, ensure_ascii=False, indent=2))
    match_path.write_text(json.dumps(matched, ensure_ascii=False, indent=2))
    print(f"events={pulled['n_events']} stake={pulled['n_with_stake']} duel={pulled['n_with_duel']}")
    print(f"wrote {raw_path}")
    print("| 事件 | Stake_A | Stake_B | Duel_A | Duel_B |")
    print("|---|---:|---:|---:|---:|")
    for r in matched:
        def fmt(x):
            return "—" if x is None else f"{x:.2f}"
        print(f"| {r['event']} | {fmt(r['stake_a'])} | {fmt(r['stake_b'])} | {fmt(r['duel_a'])} | {fmt(r['duel_b'])} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
