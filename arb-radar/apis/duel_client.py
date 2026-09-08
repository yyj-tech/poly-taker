#!/usr/bin/env python3
"""Duel/Betby public odds client. Read-only. No login, no bets, no passwords."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any

BASE = "https://duel.com"
PROXY = "https://sports-proxy.duel.com"
BRAND_ID = "2482975601191952386"
OPERATOR_ID = "2432909813404016640"
THEME = "duel"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)


def headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    h = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": BASE,
        "referer": BASE + "/sports",
        "user-agent": UA,
    }
    if extra:
        h.update(extra)
    return h


def request(method: str, url: str, body: dict[str, Any] | None = None, timeout: int = 25) -> dict[str, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            text = raw.decode("utf-8", "replace")
            parsed = None
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
            return {"ok": True, "url": url, "status": resp.status, "json": parsed, "text": text[:500]}
    except urllib.error.HTTPError as e:
        raw = e.read()
        text = raw.decode("utf-8", "replace")
        parsed = None
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        return {"ok": False, "url": url, "status": e.code, "json": parsed, "text": text[:500]}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "url": url, "status": None, "json": None, "text": str(e)}


def session(lang: str = "en", currency: str = "USD", display_in_fiat: bool = False) -> dict[str, Any]:
    url = (
        f"{BASE}/api/v2/match-betting/betby/user-session/"
        f"{lang}/{currency}/{str(display_in_fiat).lower()}"
    )
    return request("POST", url, {})


def probe() -> list[dict[str, Any]]:
    urls = [
        ("GET", f"{BASE}/api/v2/metadata", None),
        ("GET", f"{BASE}/api/v2/match-betting", None),
        ("GET", f"{PROXY}/", None),
        ("GET", "https://ui.invisiblesport.com/bt-renderer.min.js", None),
    ]
    out = []
    for method, url, body in urls:
        out.append(request(method, url, body))
    return out


def implied(odds: float | None) -> float | None:
    if not odds or odds <= 1:
        return None
    return 1.0 / float(odds)


def main() -> int:
    parser = argparse.ArgumentParser(description="Pull Duel/Betby TI outright odds (public, no login)")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--currency", default="USD")
    args = parser.parse_args()

    print("=== probe ===")
    logs = probe()
    for row in logs:
        msg = ""
        if isinstance(row.get("json"), dict):
            msg = row["json"].get("message") or row["json"].get("error") or ""
        print(f"{row['status']} {row['url']} {msg or row['text'][:120].replace(chr(10), ' ')}")

    print("=== user-session ===")
    sess = session(args.lang, args.currency, False)
    print(sess["status"], sess["url"])
    print((sess.get("text") or "")[:300].replace("\n", " "))

    token = None
    library = None
    if isinstance(sess.get("json"), dict):
        data = sess["json"].get("data") or sess["json"]
        if isinstance(data, dict):
            token = data.get("token")
            library = data.get("libraryUrl") or data.get("library_url")
    print("token", "yes" if token else "no", "libraryUrl", library)

    if not token:
        print("NO_SESSION")
        print("need: match-betting re-enabled + non-blocked IP. not a user password.")
        print(f"brand_id={BRAND_ID} operator_id={OPERATOR_ID} theme={THEME}")
        return 1

    print("=== betby ready ===")
    print("initialize BTRenderer with brand_id / token / themeName=duel")
    print("then open Esports > Dota 2 > The International outright")
    print("NO_OUTRIGHT_PRICES (iframe API not called without a live JWT proxy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
