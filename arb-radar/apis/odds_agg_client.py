#!/usr/bin/env python3
"""Third-party odds aggregator client. Read-only. No scraping, no bets.

Primary: odds-api.io (public /v3/bookmakers, events/odds need ODDS_API_IO_KEY)
Secondary: OddsPapi (all calls need ODDSPAPI_KEY)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

OAI = "https://api.odds-api.io/v3"
PAPI = "https://api.oddspapi.io/v4"

WANTED = ("Stake", "Duel", "Duelbits", "Pinnacle", "Polymarket", "GG.bet")


def get(url: str, params: dict[str, Any] | None = None, timeout: int = 25) -> dict[str, Any]:
    if params:
        url = url + "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={"accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"ok": True, "status": resp.status, "json": json.loads(resp.read().decode())}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw[:400]
        return {"ok": False, "status": e.code, "json": parsed}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "status": None, "json": str(e)}


def oai_bookmakers() -> list[str]:
    r = get(f"{OAI}/bookmakers")
    if not r["ok"] or not isinstance(r["json"], list):
        raise SystemExit(f"odds-api.io /bookmakers failed: {r}")
    return [b["name"] for b in r["json"] if isinstance(b, dict) and b.get("name")]


def print_catalog() -> None:
    names = oai_bookmakers()
    print(f"odds-api.io bookmakers: {len(names)} (no key)")
    low = {n.lower(): n for n in names}
    for q in WANTED:
        hits = [n for n in names if q.lower() in n.lower()]
        print(f"  {q}: {hits or '—'}")
    sports = get(f"{OAI}/sports")
    if sports["ok"] and isinstance(sports["json"], list):
        slugs = [s.get("slug") for s in sports["json"] if isinstance(s, dict)]
        print(f"  sports has esports: {'esports' in slugs}  slugs={slugs}")


def oai_esports(key: str, bookmakers: str = "Stake,Duel") -> None:
    ev = get(f"{OAI}/events", {"sport": "esports", "apiKey": key})
    print("odds-api.io /events?sport=esports:", ev["status"])
    if not ev["ok"]:
        print(json.dumps(ev["json"], ensure_ascii=False)[:500])
        return
    events = ev["json"] if isinstance(ev["json"], list) else ev["json"].get("events") or ev["json"]
    if not isinstance(events, list):
        print(json.dumps(ev["json"], ensure_ascii=False)[:800])
        return
    print(f"  events: {len(events)}")
    dota = [e for e in events if "dota" in json.dumps(e).lower()]
    lol = [e for e in events if "league of legends" in json.dumps(e).lower() or '"lol"' in json.dumps(e).lower()]
    print(f"  dota-ish: {len(dota)}  lol-ish: {len(lol)}")
    sample = (dota or lol or events)[:3]
    for e in sample:
        eid = e.get("id") or e.get("eventId")
        name = e.get("home") or e.get("name") or e
        print(f"  event {eid}: {name}")
        if not eid:
            continue
        odds = get(f"{OAI}/odds", {"eventId": eid, "bookmakers": bookmakers, "apiKey": key})
        print(f"    odds {odds['status']}: {json.dumps(odds['json'], ensure_ascii=False)[:400]}")


def papi_probe(key: str) -> None:
    books = get(f"{PAPI}/bookmakers", {"apiKey": key})
    print("OddsPapi /v4/bookmakers:", books["status"])
    if not books["ok"]:
        print(json.dumps(books["json"], ensure_ascii=False)[:500])
        return
    items = books["json"] if isinstance(books["json"], list) else []
    slugs = []
    for b in items:
        if isinstance(b, dict):
            slugs.append(b.get("slug") or b.get("bookmakerName") or "")
    print(f"  bookmakers: {len(slugs)}")
    for q in ("stake", "duel", "duelbits", "pinnacle", "polymarket"):
        hits = [s for s in slugs if q in s.lower()]
        print(f"  {q}: {hits or '—'}")
    for sport_id, label in ((16, "Dota2"), (18, "LoL")):
        fx = get(f"{PAPI}/fixtures", {"apiKey": key, "sportId": sport_id, "hasOdds": "true"})
        n = len(fx["json"]) if fx["ok"] and isinstance(fx["json"], list) else fx
        print(f"  fixtures {label} ({sport_id}): {n if isinstance(n, int) else fx['status']}")


def main() -> int:
    print_catalog()
    oai_key = os.environ.get("ODDS_API_IO_KEY") or os.environ.get("ODDS_API_KEY")
    papi_key = os.environ.get("ODDSPAPI_KEY")
    if oai_key:
        print("\n-- odds-api.io odds --")
        oai_esports(oai_key)
    else:
        print("\nODDS_API_IO_KEY not set; skip events/odds")
    if papi_key:
        print("\n-- OddsPapi --")
        papi_probe(papi_key)
    else:
        print("ODDSPAPI_KEY not set; skip OddsPapi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
