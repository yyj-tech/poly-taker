#!/usr/bin/env python3
"""Stake public odds client. Read-only. No login, no bets, no cookies."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any

HOSTS = [
    "https://stake.com",
    "https://stake.bet",
    "https://stake.ac",
    "https://stake.pet",
    "https://stake.us",
]

SPORT_SLUG = "dota-2"
TOURNAMENT_SLUGS = [
    "the-international-2026",
    "the-international",
    "dota-2-the-international",
]
CATEGORY_SLUGS = ["dota-2", "esports", "international", "world"]

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

SLUG_SPORT = """
query SlugSport($sport: String!) {
  slugSport(sport: $sport) {
    id
    name
    slug
    allCategories {
      id
      name
      slug
      tournamentList {
        id
        name
        slug
      }
    }
    fixtureList {
      id
      name
      slug
      status
    }
  }
}
"""

SLUG_TOURNAMENT = """
query SlugTournament($sport: String!, $category: String!, $tournament: String!) {
  slugTournament(sport: $sport, category: $category, tournament: $tournament) {
    id
    name
    slug
    fixtureList {
      id
      name
      slug
      status
    }
  }
}
"""

SEARCH = """
query Search($query: String!) {
  sportFixtureQuery(query: $query) {
    fixture {
      id
      name
      slug
      status
    }
  }
}
"""

FIXTURE_ODDS = """
query FixtureOdds($id: String!) {
  sportFixture(id: $id) {
    id
    name
    slug
    status
    tournament {
      id
      name
      slug
      category {
        id
        name
        slug
        sport { id name slug }
      }
    }
    data {
      ... on SportFixtureDataOutright { name startTime endTime }
      ... on SportFixtureDataMatch {
        startTime
        competitors { name abbreviation extId }
      }
    }
    groups(groups: ["winner"]) {
      templates {
        markets {
          id
          name
          status
          extId
          specifiers
          outcomes { id name odds active }
        }
      }
    }
  }
}
"""

PUBLIC_FEED = """
query PublicFeed($limit: Int) {
  allSportBets(limit: $limit) {
    bet {
      ... on SportBet {
        amount
        currency
        outcomes {
          odds
          fixtureName
          outcome { name }
        }
      }
    }
  }
  highrollerSportBets(limit: $limit) {
    bet {
      ... on SportBet {
        amount
        currency
        outcomes {
          odds
          fixtureName
          outcome { name }
        }
      }
    }
  }
}
"""


def headers(origin: str) -> dict[str, str]:
    return {
        "content-type": "application/json",
        "accept": "application/json",
        "x-language": "en",
        "origin": origin,
        "referer": origin + "/sports",
        "user-agent": UA,
    }


def gql(host: str, query: str, variables: dict[str, Any] | None = None, timeout: int = 25) -> dict[str, Any]:
    url = host.rstrip("/") + "/_api/graphql"
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=headers(host),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return {
                "ok": True,
                "url": url,
                "status": resp.status,
                "json": json.loads(body.decode() or "{}"),
                "raw": body[:300].decode("utf-8", "replace"),
            }
    except urllib.error.HTTPError as e:
        raw = e.read()[:400]
        return {
            "ok": False,
            "url": url,
            "status": e.code,
            "json": None,
            "raw": raw.decode("utf-8", "replace"),
        }
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "url": url, "status": None, "json": None, "raw": str(e)}


def implied(odds: float | None) -> float | None:
    if not odds or odds <= 1:
        return None
    return 1.0 / float(odds)


def looks_like_ti(name: str) -> bool:
    n = (name or "").lower()
    return any(k in n for k in ("international", " ti ", "ti15", "ti 15", "ti2026", "ti 2026"))


def extract_outcomes(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in fixture.get("groups") or []:
        for tmpl in group.get("templates") or []:
            for market in tmpl.get("markets") or []:
                for oc in market.get("outcomes") or []:
                    odds = oc.get("odds")
                    rows.append(
                        {
                            "team": oc.get("name"),
                            "odds": odds,
                            "implied": implied(odds) if isinstance(odds, (int, float)) else None,
                            "active": oc.get("active"),
                            "market": market.get("name"),
                            "market_status": market.get("status"),
                            "limit": None,
                        }
                    )
    return rows


def pick_working_host(preferred: str | None) -> tuple[str | None, list[dict[str, Any]]]:
    log: list[dict[str, Any]] = []
    hosts = [preferred] + [h for h in HOSTS if h != preferred] if preferred else list(HOSTS)
    for host in hosts:
        if not host:
            continue
        res = gql(host, "query { __typename }")
        log.append({"step": "handshake", **{k: res[k] for k in ("url", "status", "raw")}})
        data = (res.get("json") or {}).get("data")
        if res.get("ok") and data and data.get("__typename"):
            return host, log
    return None, log


def scan(host: str) -> dict[str, Any]:
    log: list[dict[str, Any]] = []
    sport = gql(host, SLUG_SPORT, {"sport": SPORT_SLUG})
    log.append({"step": "slugSport dota-2", "url": sport["url"], "status": sport["status"], "raw": sport["raw"][:240]})
    sport_data = ((sport.get("json") or {}).get("data") or {}).get("slugSport")

    search = gql(host, SEARCH, {"query": "The International"})
    log.append({"step": "sportFixtureQuery", "url": search["url"], "status": search["status"], "raw": search["raw"][:240]})
    search_fix = (((search.get("json") or {}).get("data") or {}).get("sportFixtureQuery") or {}).get("fixture")

    tournaments: list[dict[str, Any]] = []
    if sport_data:
        for cat in sport_data.get("allCategories") or []:
            for t in cat.get("tournamentList") or []:
                tournaments.append({**t, "category": cat.get("slug")})

    ti_candidates = [t for t in tournaments if looks_like_ti(t.get("name", "") + " " + t.get("slug", ""))]
    if not ti_candidates:
        for cat in CATEGORY_SLUGS:
            for tslug in TOURNAMENT_SLUGS:
                res = gql(host, SLUG_TOURNAMENT, {"sport": SPORT_SLUG, "category": cat, "tournament": tslug})
                log.append(
                    {
                        "step": f"slugTournament {cat}/{tslug}",
                        "url": res["url"],
                        "status": res["status"],
                        "raw": res["raw"][:200],
                    }
                )
                node = ((res.get("json") or {}).get("data") or {}).get("slugTournament")
                if node:
                    ti_candidates.append({**node, "category": cat})
                time.sleep(0.35)

    fixtures: list[dict[str, Any]] = []
    if isinstance(search_fix, list):
        fixtures.extend(search_fix)
    elif isinstance(search_fix, dict):
        fixtures.append(search_fix)
    if sport_data:
        fixtures.extend(sport_data.get("fixtureList") or [])
    for t in ti_candidates:
        fixtures.extend(t.get("fixtureList") or [])

    seen: set[str] = set()
    unique = []
    for fx in fixtures:
        if not fx or not fx.get("id") or fx["id"] in seen:
            continue
        seen.add(fx["id"])
        unique.append(fx)

    outright_rows: list[dict[str, Any]] = []
    qf_rows: list[dict[str, Any]] = []
    for fx in unique:
        res = gql(host, FIXTURE_ODDS, {"id": fx["id"]})
        log.append({"step": f"sportFixture {fx.get('name')}", "url": res["url"], "status": res["status"]})
        node = ((res.get("json") or {}).get("data") or {}).get("sportFixture")
        if not node:
            continue
        rows = extract_outcomes(node)
        name = (node.get("name") or "") + " " + ((node.get("data") or {}).get("name") or "")
        if looks_like_ti(name) and len(rows) >= 4:
            outright_rows = rows
            outright_rows = [{**r, "fixture": node.get("name"), "fixture_id": node.get("id")} for r in rows]
        elif looks_like_ti(name) or "quarter" in name.lower() or "playoff" in name.lower():
            qf_rows.append({"fixture": node.get("name"), "id": node.get("id"), "outcomes": rows})
        time.sleep(0.35)

    feed = gql(host, PUBLIC_FEED, {"limit": 5})
    log.append({"step": "public feed", "url": feed["url"], "status": feed["status"], "raw": feed["raw"][:200]})

    return {
        "host": host,
        "sport": sport_data,
        "tournaments": ti_candidates,
        "outright": outright_rows,
        "quarters": qf_rows,
        "log": log,
        "errors": (sport.get("json") or {}).get("errors")
        or (search.get("json") or {}).get("errors"),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Pull Stake TI outright odds (public, no login)")
    p.add_argument("--host", default=None, help="e.g. https://stake.us")
    args = p.parse_args()
    host, handshake_log = pick_working_host(args.host)
    print("=== handshake ===")
    for row in handshake_log:
        print(f"{row['status']} {row['url']} {row['raw'][:120].replace(chr(10), ' ')}")
    if not host:
        print("NO_WORKING_HOST")
        return 2
    print("using", host)
    result = scan(host)
    print("=== sport ===")
    print(json.dumps(result["sport"], ensure_ascii=False)[:800])
    print("=== tournaments ===")
    print(json.dumps(result["tournaments"], ensure_ascii=False)[:800])
    print("=== outright ===")
    if result["outright"]:
        print(f"{'team':24} {'odds':8} {'implied':8} {'active'}")
        for r in result["outright"]:
            impl = f"{r['implied']:.4f}" if r["implied"] else "-"
            print(f"{str(r['team'])[:24]:24} {str(r['odds']):8} {impl:8} {r['active']}")
    else:
        print("NO_OUTRIGHT_PRICES")
        if result.get("errors"):
            print(json.dumps(result["errors"], ensure_ascii=False)[:600])
    print("=== log ===")
    for row in result["log"]:
        print(row.get("step"), row.get("status"), row.get("url", ""))
    return 0 if result["outright"] else 1


if __name__ == "__main__":
    sys.exit(main())
