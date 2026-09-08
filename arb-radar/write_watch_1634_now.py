#!/usr/bin/env python3
"""Write watch-jdg-tt.md/json for 2026-08-23 ~16:34 CST vs 15:39. Analysis only."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT_MD = Path("/workspace/arb-radar/watch-jdg-tt.md")
OUT_JSON = Path("/workspace/arb-radar/watch-jdg-tt.json")
SCANS = Path("/workspace/arb-radar/scans")
CST = timezone(timedelta(hours=8))
BASELINE = "15:39"


def clob_l1(book):
    asks = book.get("asks") or []
    levels = {}
    for a in asks:
        try:
            px = float(a.get("price"))
            sz = float(a.get("size") or 0)
        except (TypeError, ValueError):
            continue
        if sz <= 0:
            continue
        levels[px] = levels.get(px, 0.0) + sz
    if not levels:
        return None, None
    best = min(levels)
    return best, levels[best]


def path(s, p, odds, book, book_team, pm_team, pin_limit=None):
    d = s / odds
    capped = False
    if pin_limit and d > float(pin_limit) + 1e-9:
        d = float(pin_limit)
        s = d * odds
        capped = True
    spend = s * p
    fee = spend * 0.05 * p * (1 - p)
    cost = d + spend + fee
    profit = s - cost
    rate = profit / cost
    return {
        "book": book,
        "book_team": book_team,
        "pm_team": pm_team,
        "S": s,
        "p": p,
        "odds": odds,
        "D": d,
        "spend": spend,
        "fee": fee,
        "cost": cost,
        "profit": profit,
        "rate": rate,
        "gt_0p5": rate > 0.005,
        "hv": rate >= 0.015,
        "capped": capped,
        "pin_limit": pin_limit,
    }


def rate_pct_str(rate: float | None) -> str:
    if rate is None:
        return "—"
    sign = "+" if rate >= 0 else "−"
    return f"{sign}{abs(rate) * 100:.2f}%"


def minus_num(x: float, nd: int = 1) -> str:
    if x < 0:
        return f"−{abs(x):.{nd}f}"
    return f"{x:.{nd}f}"


def row_md(status, event, r, settle):
    odds_txt = f"{r['odds']:g}"
    left = f"{r['book']} 买{r['book_team']} {r['D']:.1f}U @{odds_txt}"
    right = f"PM 买{r['pm_team']} {r['S']:.1f}份 @{r['p']:.3f}"
    return (
        f"| {status} | {event} | {left} | {right} | {r['cost']:.1f} U | "
        f"{r['fee']:.1f} U | {rate_pct_str(r['rate'])} | {settle} | {minus_num(r['profit'])} U |"
    )


def row_json(status, event, r, settle):
    odds_txt = f"{r['odds']:g}"
    left = f"{r['book']} 买{r['book_team']} {r['D']:.1f}U @{odds_txt}"
    right = f"PM 买{r['pm_team']} {r['S']:.1f}份 @{r['p']:.3f}"
    return {
        "状态": status,
        "事件": event,
        "左买": left,
        "右买": right,
        "成本": f"{r['cost']:.1f} U",
        "手续费": f"{r['fee']:.1f} U",
        "利率": rate_pct_str(r["rate"]),
        "多久结算": settle,
        "一单利润": f"{minus_num(r['profit'])} U",
        "rate": round(r["rate"], 8),
        "profit_u": round(r["profit"], 1),
        "gt_0p5": r["gt_0p5"],
        "high_value": False,  # live: do not mark high-value
    }


def load_gamma(slug: str) -> dict:
    data = json.loads((SCANS / "pm" / "slugs" / f"{slug}.json").read_text())
    return data[0] if isinstance(data, list) else data


def find_mw(ev: dict) -> dict:
    for m in ev.get("markets") or []:
        if m.get("groupItemTitle") == "Match Winner":
            return m
    raise SystemExit(f"no Match Winner in {ev.get('title')}")


def parse_maybe_json(x):
    if isinstance(x, str):
        return json.loads(x)
    return x


def pm_pair(a1, b1, a2, b2):
    def fmt(a, b):
        if a is None or b is None:
            return "—"
        return f"{a:g}/{b:g}"

    if a2 is None and b2 is None:
        return f"{fmt(a1, b1)}→—"
    if a1 == a2 and b1 == b2:
        return f"{a1:g}/{b1:g} 不变"
    return f"{fmt(a1, b1)}→{fmt(a2, b2)}"


def book_pair(a1, b1, a2, b2):
    if a1 is None and b1 is None and a2 is None and b2 is None:
        return "—→—"
    if a2 is None and b2 is None:
        return f"{a1:g}/{b1:g}→—"
    if a1 is None and b1 is None:
        return f"—→{a2:g}/{b2:g}"
    if a1 == a2 and b1 == b2:
        return f"{a1:g}/{b1:g} 不变"
    return f"{a1:g}/{b1:g}→{a2:g}/{b2:g}"


def sd(x, dagger):
    if x is None:
        return "—"
    return f"{x:g}†" if dagger else f"{x:g}"


def pm_cell(x):
    return "—" if x is None else f"{x:g}"


def am_to_dec(am):
    am = float(am)
    if am > 0:
        return round(1.0 + am / 100.0, 3)
    return round(1.0 + 100.0 / abs(am), 3)


now = datetime.now(CST)
SCAN = now.strftime("%Y-%m-%d %H:%M")

ev_jdg = load_gamma("lol-jdg-tt-2026-08-20")
ev_lgd = load_gamma("lol-tt-lgd-2026-08-23")
mw_jdg = find_mw(ev_jdg)
mw_lgd = find_mw(ev_lgd)

tok_jdg, tok_tt = parse_maybe_json(mw_jdg["clobTokenIds"])
tok_tt2, tok_lgd = parse_maybe_json(mw_lgd["clobTokenIds"])
prices_jdg = [float(x) for x in parse_maybe_json(mw_jdg["outcomePrices"])]
prices_lgd = [float(x) for x in parse_maybe_json(mw_lgd["outcomePrices"])]

clobdir = SCANS / "clob_watch"


def load_book(tok):
    p = clobdir / f"{tok}.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return {}


book_jdg = load_book(tok_jdg)
book_tt = load_book(tok_tt)
book_tt2 = load_book(tok_tt2)
book_lgd = load_book(tok_lgd)
p_jdg_raw, s_jdg_raw = clob_l1(book_jdg)
p_tt_raw, s_tt_raw = clob_l1(book_tt)
p_tt2, s_tt2 = clob_l1(book_tt2)
p_lgd, s_lgd = clob_l1(book_lgd)

clob_err_jdg = None
if isinstance(book_jdg, dict) and book_jdg.get("error"):
    clob_err_jdg = book_jdg["error"]
if isinstance(book_tt, dict) and book_tt.get("error") and not clob_err_jdg:
    clob_err_jdg = book_tt["error"]

oai = json.loads((SCANS / "watch_jdg" / "oai.json").read_text())
dagger = bool(oai.get("dagger"))
matched = {r["event"]: r for r in (oai.get("matched") or [])}
oai_jdg = matched.get("JDG vs TT") or {}
oai_lgd = matched.get("TT vs LGD") or {}
oai_evs = {e["id"]: e for e in (oai.get("pulled") or {}).get("events") or []}
full_jdg = oai_evs.get(7291391184, {})
full_lgd = oai_evs.get(5958057944, {})


def oai_num(row, key):
    v = row.get(key)
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


stake_jdg = oai_num(oai_jdg, "stake_a")
stake_tt = oai_num(oai_jdg, "stake_b")
duel_jdg = oai_num(oai_jdg, "duel_a")
duel_tt = oai_num(oai_jdg, "duel_b")
# match_watch missed ThunderTalk; use pulled id 5958057944
stake_tt2 = oai_num(full_lgd, "stake_home") or oai_num(oai_lgd, "stake_a")
stake_lgd = oai_num(full_lgd, "stake_away") or oai_num(oai_lgd, "stake_b")
duel_tt2 = oai_num(full_lgd, "duel_home") or oai_num(oai_lgd, "duel_a")
duel_lgd = oai_num(full_lgd, "duel_away") or oai_num(oai_lgd, "duel_b")

# 429 reuse 15:39 quotes with †
STALE_1539_LGD = {
    "stake_a": 4.4,
    "stake_b": 1.22,
    "duel_a": 4.4,
    "duel_b": 1.22,
    "stake_updated": "2026-08-23T07:34:09.041Z",
    "duel_updated": "2026-08-23T07:33:06.925Z",
}
lgd_books_missing = any(x is None for x in (stake_tt2, stake_lgd, duel_tt2, duel_lgd))
if dagger and lgd_books_missing:
    stake_tt2 = STALE_1539_LGD["stake_a"]
    stake_lgd = STALE_1539_LGD["stake_b"]
    duel_tt2 = STALE_1539_LGD["duel_a"]
    duel_lgd = STALE_1539_LGD["duel_b"]

mu = json.loads((SCANS / "pin" / "LPL_matchups.json").read_text())
mk_straight_path = SCANS / "pin" / "LPL_markets_straight.json"
if not mk_straight_path.exists():
    mk_straight_path = SCANS / "pin" / "LPL_markets.json"
mk = json.loads(mk_straight_path.read_text())
rows_mk = mk if isinstance(mk, list) else []

parents = []
live_children = []
child_1634353344 = None
parent_1634146968 = None
child_1634593525 = None
for x in mu if isinstance(mu, list) else []:
    names = [p.get("name") for p in (x.get("participants") or []) if isinstance(p, dict)]
    rec = {
        "id": x.get("id"),
        "parentId": x.get("parentId"),
        "names": names,
        "status": x.get("status"),
        "isLive": x.get("isLive"),
        "startTime": x.get("startTime"),
        "hasMarkets": x.get("hasMarkets"),
        "units": x.get("units"),
        "type": x.get("type"),
        "periods": x.get("periods"),
    }
    if x.get("parentId") is None and x.get("type") == "matchup":
        parents.append(rec)
    if x.get("id") == 1634353344:
        child_1634353344 = x
    if x.get("id") == 1634146968:
        parent_1634146968 = x
    if x.get("id") == 1634593525:
        child_1634593525 = x
    if x.get("isLive") is True:
        live_children.append(rec)

parent_ids = {p["id"] for p in parents}
pin_parent_absent_jdg = 1633881950 not in parent_ids
pin_child_absent_jdg = child_1634353344 is None

# TT/LGD parent + period-0 series ML
pin_tt_lgd_listed = False
pin_tt = pin_lgd = None
pin_tt_am = pin_lgd_am = None
pin_tt_limit = None
pin_tt_parent_id = None
pin_tt_parent_status = None
pin_tt_parent_live = False
pin_tt_ml_status = None
pin_tt_period0_in_markets = False
for p in parents:
    joined = " ".join(str(n) for n in p["names"]).lower()
    if "thunder" in joined and "lgd" in joined:
        pin_tt_lgd_listed = True
        pin_tt_parent_id = p["id"]
        pin_tt_parent_status = p["status"]
        pin_tt_parent_live = bool(p["isLive"])
        for r in rows_mk:
            if (
                r.get("matchupId") == p["id"]
                and r.get("type") == "moneyline"
                and r.get("period") == 0
                and not r.get("isAlternate")
            ):
                pin_tt_period0_in_markets = True
                pin_tt_ml_status = r.get("status")
                for pr in r.get("prices") or []:
                    dec = am_to_dec(pr.get("price"))
                    if pr.get("designation") == "home":
                        pin_tt = dec
                        pin_tt_am = pr.get("price")
                    elif pr.get("designation") == "away":
                        pin_lgd = dec
                        pin_lgd_am = pr.get("price")
                lims = r.get("limits") or []
                if lims:
                    pin_tt_limit = lims[0].get("amount")

# period-0 series ML missing from straight feed → withdrawn (even if periods metadata says open)
pin_period0_withdrawn_tt = not pin_tt_period0_in_markets or pin_tt_ml_status in (
    "withdrawn",
    "closed",
)
# skip PIN cashout if period-0 not open with prices
pin_tt_use = pin_tt if (pin_tt is not None and pin_lgd is not None and pin_tt_ml_status == "open") else None
pin_lgd_use = pin_lgd if pin_tt_use is not None else None

pin_child_live = bool(child_1634593525 and child_1634593525.get("isLive"))
pin_any_live = pin_tt_parent_live or pin_child_live or any(
    c.get("parentId") == 1634146968 and c.get("isLive") for c in live_children
)

parent_any_mk = sum(1 for r in rows_mk if r.get("matchupId") == 1633881950)
child_any_mk = sum(1 for r in rows_mk if r.get("matchupId") == 1634353344)
parent_tt_mk = sum(1 for r in rows_mk if r.get("matchupId") == 1634146968)

# ---- PM status ----
jdg_start = datetime(2026, 8, 20, 17, 0, tzinfo=CST)
tt_start = datetime(2026, 8, 23, 15, 0, tzinfo=CST)
mins_past = (now - jdg_start).total_seconds() / 60.0
days_to_tt = (tt_start - now).total_seconds() / 86400.0

gamma_live_jdg = ev_jdg.get("live")
gamma_closed_jdg = ev_jdg.get("closed")
gamma_ended_jdg = ev_jdg.get("ended")
gamma_score = ev_jdg.get("score")
mw_accept_jdg = mw_jdg.get("acceptingOrders")
mw_uma = mw_jdg.get("umaResolutionStatus")
ev_accept_jdg = ev_jdg.get("acceptingOrders")

gamma_live_lgd = ev_lgd.get("live")
gamma_closed_lgd = ev_lgd.get("closed")
gamma_ended_lgd = ev_lgd.get("ended")
gamma_score_lgd = ev_lgd.get("score")
mw_accept_lgd = mw_lgd.get("acceptingOrders")
ev_accept_lgd = ev_lgd.get("acceptingOrders")

jdg_ended = bool(gamma_ended_jdg) or bool(gamma_closed_jdg)
tt_ended = bool(gamma_ended_lgd) or bool(gamma_closed_lgd)
tt_live = bool(gamma_live_lgd)

pm_a_jdg = pm_b_jdg = None
pm_a_tt = p_tt2
pm_b_lgd = p_lgd
s_a_tt = s_tt2
s_b_lgd = s_lgd

l1_thick_tt = bool(s_a_tt and s_a_tt > 2000)
l1_thick_lgd = bool(s_b_lgd and s_b_lgd > 2000)
l1_thick = l1_thick_tt or l1_thick_lgd

oai_status_jdg = "absent (ended, not in pending/live; odds_multi 7291391184 omitted)"
oai_live_jdg = False
oai_status_lgd = full_lgd.get("status") or oai_lgd.get("status") or "pending"
oai_live_lgd = bool(full_lgd.get("live") if full_lgd else oai_lgd.get("live"))
stake_upd = full_lgd.get("stake_updated") or oai_lgd.get("stake_updated")
duel_upd = full_lgd.get("duel_updated") or oai_lgd.get("duel_updated")
if dagger:
    oai_status_jdg = "429† last=absent (ended)"
    oai_status_lgd = f"429† last={oai_status_lgd}"
    if not stake_upd:
        stake_upd = STALE_1539_LGD["stake_updated"]
    if not duel_upd:
        duel_upd = STALE_1539_LGD["duel_updated"]

# overall live if any source says live
is_live = bool(tt_live or oai_live_lgd or pin_any_live)
status_lgd = "结束" if tt_ended else ("滚球" if is_live else "非滚球")
if is_live:
    settle = "滚球中"
elif tt_ended:
    settle = "已结束，不硬算"
else:
    settle = "已到开赛点"

# ---- paths TT vs LGD (still calc if live and books open; skip if ended) ----
paths = []
if not tt_ended:
    if s_b_lgd and pm_b_lgd is not None and duel_tt2:
        paths.append(("Duel", path(s_b_lgd, pm_b_lgd, duel_tt2, "Duel", "TT", "LGD"), l1_thick_lgd))
    if s_b_lgd and pm_b_lgd is not None and stake_tt2:
        paths.append(("Stake", path(s_b_lgd, pm_b_lgd, stake_tt2, "Stake", "TT", "LGD"), l1_thick_lgd))
    if s_a_tt and pm_a_tt is not None and duel_lgd:
        paths.append(("Duel", path(s_a_tt, pm_a_tt, duel_lgd, "Duel", "LGD", "TT"), l1_thick_tt))
    if s_a_tt and pm_a_tt is not None and stake_lgd:
        paths.append(("Stake", path(s_a_tt, pm_a_tt, stake_lgd, "Stake", "LGD", "TT"), l1_thick_tt))
    # PIN only if period-0 still open
    if s_b_lgd and pm_b_lgd is not None and pin_tt_use:
        paths.append(("PIN", path(s_b_lgd, pm_b_lgd, pin_tt_use, "PIN", "TT", "LGD", pin_limit=pin_tt_limit), l1_thick_lgd))
    if s_a_tt and pm_a_tt is not None and pin_lgd_use:
        paths.append(("PIN", path(s_a_tt, pm_a_tt, pin_lgd_use, "PIN", "LGD", "TT", pin_limit=pin_tt_limit), l1_thick_tt))

paths_sorted = sorted(paths, key=lambda x: (-x[1]["profit"], x[0]))
best = max(paths, key=lambda x: x[1]["rate"])[1] if paths else None

# baseline 15:39 CST
base_pm_tt, base_pm_lgd = 0.22, 0.79
base_stake_tt, base_stake_lgd = 4.4, 1.22
base_duel_tt, base_duel_lgd = 4.4, 1.22
base_pin_tt, base_pin_lgd = None, None
base_pin_listed = True
base_sz_tt, base_sz_lgd = 424.0, 196.24
base_rates = {
    "duel_tt": -0.02327132,
    "stake_tt": -0.02327132,
    "duel_lgd": -0.03990144,
    "stake_lgd": -0.03990144,
    "pin_tt": None,
    "pin_lgd": None,
}
base_best = -0.02327132  # Duel buy TT

cur_rates = {}
for _, r, _ in paths:
    key = f"{r['book'].lower()}_{'tt' if r['book_team']=='TT' else 'lgd'}"
    cur_rates[key] = r["rate"]

rate_pp = {}
for k, br in base_rates.items():
    if k not in cur_rates:
        continue
    rate_pp[k] = (cur_rates[k] - br) * 100

best_rate = best["rate"] if best else None
best_pp = (best_rate - base_best) * 100 if best_rate is not None else 0.0
max_abs_path_dpp = max((abs(v) for v in rate_pp.values()), default=0.0)

pm_ask_delta_tt = abs((pm_a_tt or 0) - base_pm_tt) if pm_a_tt is not None else 0.0
pm_ask_delta_lgd = abs((pm_b_lgd or 0) - base_pm_lgd) if pm_b_lgd is not None else 0.0
pm_ask_ge_0p02 = max(pm_ask_delta_tt, pm_ask_delta_lgd) >= 0.02

books_moved = (not dagger) and (
    (stake_tt2, stake_lgd) != (base_stake_tt, base_stake_lgd)
    or (duel_tt2, duel_lgd) != (base_duel_tt, base_duel_lgd)
)
if dagger:
    books_move_detail = "Stake/Duel 429 † reused 15:39, not treated as live move"
elif books_moved:
    books_move_detail = (
        f"Stake {base_stake_tt:g}/{base_stake_lgd:g}→{stake_tt2:g}/{stake_lgd:g}; "
        f"Duel {base_duel_tt:g}/{base_duel_lgd:g}→{duel_tt2:g}/{duel_lgd:g}"
    )
else:
    books_move_detail = "no live book move"

flip = False
for k, br in base_rates.items():
    cr = cur_rates.get(k)
    if cr is None:
        continue
    if (br < 0 and cr >= 0) or (br >= 0 and cr < 0):
        flip = True

gt_0p5_paths = []
hv_paths = []
table2_md = []
table2_json = []

table2_md.append("| 结束 | JDG vs TT | — | — | — | — | — | 已结束，不硬算套现 | — |")
table2_json.append(
    {
        "状态": "结束",
        "事件": "JDG vs TT",
        "左买": "—",
        "右买": "—",
        "成本": "—",
        "手续费": "—",
        "利率": "—",
        "多久结算": "已结束，不硬算套现",
        "一单利润": "—",
        "rate": None,
        "profit_u": None,
        "gt_0p5": False,
        "high_value": False,
        "ended_no_cashout": True,
    }
)

for book, r, thick in paths_sorted:
    # live: never upgrade high-value
    r["hv"] = False
    if book == "PIN":
        lim = f"限额maxRisk {pin_tt_limit:g}" if pin_tt_limit else "限额未知"
        capbit = "限额封顶" if r.get("capped") else "本单按PM档1"
        note = f"LPL PIN现价，{lim}；{capbit}"
    elif book == "Duel":
        note = "LPL Duel 429†沿用15:39，限额未知；本单按PM档1" if dagger else "LPL Duel现价，限额未知；本单按PM档1"
    else:
        note = "LPL Stake 429†沿用15:39，限额未知；本单按PM档1" if dagger else "LPL Stake现价，限额未知；本单按PM档1"
    extra = []
    extra.append("不升格")
    if is_live:
        extra.append("滚球规则风险")
    if thick:
        extra.append("档1异常厚")
    event = f"TT vs LGD（{note}；{'；'.join(extra)}）"
    table2_md.append(row_md(status_lgd, event, r, settle))
    js = row_json(status_lgd, event, r, settle)
    table2_json.append(js)
    if r["gt_0p5"]:
        gt_0p5_paths.append(js)

# suppress hv when live
high_value_flag = False

# should_send
reasons = []
if gt_0p5_paths:
    reasons.append("费后>0.5%")
if max_abs_path_dpp >= 0.3:
    reasons.append(f"利率变动≥0.3pp ({max_abs_path_dpp:.2f})")
if flip:
    reasons.append("翻正/翻负")
if pm_ask_ge_0p02:
    reasons.append("PM ask≥0.02")
if books_moved:
    reasons.append("Stake/Duel实质移动")
# PIN already withdrawn at 15:39 — only send if it reappears
if not pin_period0_withdrawn_tt:
    reasons.append("PIN period-0 系列ML重新挂出")
# already live last round; only send on new end or series score change
if tt_ended:
    reasons.append("TT vs LGD结束")
base_score_lgd = "000-000|0-0|Bo3"
score_changed = (gamma_score_lgd or "") != base_score_lgd
if score_changed:
    reasons.append(f"比分系列变化 {base_score_lgd}→{gamma_score_lgd}")

should_send = "YES" if reasons else "NO"

parent_desc = []
for p in parents:
    st = p["startTime"]
    st_cst = ""
    if st:
        dt = datetime.fromisoformat(st.replace("Z", "+00:00")).astimezone(CST)
        st_cst = dt.strftime("%Y-%m-%d %H:%M CST")
    names = "/".join(str(n) for n in p["names"])
    parent_desc.append(
        f"{names} {p['id']} {st_cst} / {st} {p['status']} isLive={p['isLive']}"
    )
live_desc = []
for c in live_children:
    names = "/".join(str(n) for n in c["names"])
    live_desc.append(
        f"LIVE_CHILD {names} {c['id']} parent={c['parentId']} status={c['status']} units={c.get('units')}"
    )

sz_tt_s = f"{s_a_tt:.1f}" if s_a_tt is not None else "—"
sz_lgd_s = f"{s_b_lgd:.1f}" if s_b_lgd is not None else "—"
thick_tag = "（档1异常厚）" if l1_thick else ""

gamma_best_lgd = mw_lgd.get("bestAsk")
try:
    gamma_best_lgd_f = float(gamma_best_lgd) if gamma_best_lgd is not None else None
except (TypeError, ValueError):
    gamma_best_lgd_f = None
clob_gamma_match = (
    gamma_best_lgd_f is not None and pm_a_tt is not None and abs(gamma_best_lgd_f - pm_a_tt) < 1e-9
)

both_ended = jdg_ended and tt_ended
routine_deleted = False

# ---- markdown ----
md = []
md.append(f"# JDG/TT 盯盘 {SCAN} CST")
md.append("")
live_note = "TT vs LGD 仍滚球。" if is_live else "TT vs LGD 非滚球。"
end_note = (
    "两场均已结束，parent 应删 routine（本脚本不删）。"
    if both_ended
    else "仅 JDG vs TT 结束、TT vs LGD 仍进行/未结束，routine 不删。"
)
md.append(
    "只分析，未下注。数据：PM Gamma + CLOB 档1最佳 ask（不累加）；"
    + (
        "Stake/Duel 经 odds-api.io LPL Split 3 本轮 429 †，沿用 15:39 价。"
        if dagger
        else "Stake/Duel 经 odds-api.io LPL Split 3 本轮新刷成功（无429，无†）；"
    )
    + "PIN guest 199353 related/straight 404，已回退 /leagues/199353/markets/straight；"
    + "JDG/TT PIN period-0 仍撤；"
    + (
        "TT vs LGD 父盘仍在但 period-0 系列 ML 已从 straight 盘口撤下，PIN 套现跳过。"
        if pin_period0_withdrawn_tt
        else "TT vs LGD PIN period-0 仍开。"
    )
    + "档1只吃最佳 ask。单档>2000份标「档1异常厚」。高价值 = 费后≥1.5% 且规则一致；滚球不升格（滚球规则风险）。"
    + "微正不升格。本轮额外标出费后>0.5% 路径。JDG vs TT 已结束，不硬算套现。"
    + live_note
    + end_note
)
md.append("")
md.append(f"scan_cst：{SCAN} CST（Asia/Shanghai）")
md.append(
    f"是否滚球：{'是' if is_live else '否'}。"
    f"JDG vs TT 已结束（8/20 17:00 CST 开赛，赛后约 {mins_past:.0f} 分钟；"
    f"PM live={gamma_live_jdg}、closed={gamma_closed_jdg}、ended={gamma_ended_jdg}、"
    f"accepting={mw_accept_jdg}（market；event accepting={ev_accept_jdg}）、score {gamma_score}；"
    f"odds-api.io 本轮{'429 †' if dagger else '新刷'}，JDG/TT 不在 pending/live；"
    f"PIN 父盘 1633881950 absent_from_list，period-0 系列 ML 已撤；PIN 子盘 1634353344 absent。"
    f"TT vs LGD **仍滚球**：PM live={gamma_live_lgd}、closed={gamma_closed_lgd}、ended={gamma_ended_lgd}、"
    f"accepting={mw_accept_lgd}（market；event accepting={ev_accept_lgd}）、score {gamma_score_lgd}；"
    f"OAI status={oai_status_lgd} live={oai_live_lgd}；"
    f"PIN 父盘 {pin_tt_parent_id} status={pin_tt_parent_status} isLive={pin_tt_parent_live}，"
    f"period-0 系列 ML {'已撤' if pin_period0_withdrawn_tt else '仍开'}；"
    f"PIN 滚球子盘 1634593525 isLive={pin_child_live}（地图盘，不当系列）。"
    f"开赛 15:00 CST，本扫描约 {abs(days_to_tt)*24*60:.0f} 分钟后。"
)
md.append(
    "是否结束：JDG vs TT 已结束（PM "
    f"live={gamma_live_jdg} closed={gamma_closed_jdg} ended={gamma_ended_jdg} score {gamma_score}，"
    "Bo3 2-1 JDG 胜；不要硬算套现）。"
    + (
        f"TT vs LGD 已结束 score {gamma_score_lgd}。"
        if tt_ended
        else f"TT vs LGD **仍未结束、仍滚球** score {gamma_score_lgd}（系列 0-1，LGD 先下一图；地图2或进行中）。"
    )
    + ("两场都结束后才删 routine；本轮未双结束，routine 不删。" if not both_ended else "两场均结束，parent 应删 routine（本脚本不删）。")
)
md.append("")
md.append("## 表1 价格对照")
md.append("")
md.append(
    "| 状态 | 事件 | 队A | 队B | PM_A | PM_B | PIN_A | PIN_B | Stake_A | Stake_B | Duel_A | Duel_B |"
)
md.append("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
md.append("| 结束 | JDG vs TT | JDG | TT | — | — | — | — | — | — | — | — |")
pin_a_cell = pm_cell(pin_tt_use)
pin_b_cell = pm_cell(pin_lgd_use)
md.append(
    f"| {status_lgd} | TT vs LGD | TT | LGD | {pm_cell(pm_a_tt)} | {pm_cell(pm_b_lgd)} | "
    f"{pin_a_cell} | {pin_b_cell} | {sd(stake_tt2, dagger)} | {sd(stake_lgd, dagger)} | "
    f"{sd(duel_tt2, dagger)} | {sd(duel_lgd, dagger)} |"
)
md.append("")
md.append(
    f"PM 档1深度：JDG vs TT 已结束，不吃套现档。CLOB 双边 404（{clob_err_jdg or 'No orderbook'}；"
    f"Gamma outcomePrices {prices_jdg} bestAsk {mw_jdg.get('bestAsk')} bestBid {mw_jdg.get('bestBid')} uma={mw_uma}）。"
    f"昨日 leftover 盘口已撤，不当套现。 TT vs LGD TT {sz_tt_s}份 @{pm_a_tt} / LGD {sz_lgd_s}份 @{pm_b_lgd}{thick_tag}。"
    f"Gamma bestAsk {mw_lgd.get('bestAsk')} vs CLOB L1 {pm_a_tt}（{'一致' if clob_gamma_match else '不一致，套现用CLOB档1'}）；"
    f"outcomePrices {prices_lgd}。"
)
md.append(
    (
        "Stake/Duel 本轮 odds-api.io 429 †。JDG vs TT 已结束，表1 Stake/Duel 写—（不沿用陈价）。"
        if dagger
        else "Stake/Duel 本轮 odds-api.io 新刷成功，无 429，无†。JDG vs TT 事件 7291391184 已不在 pending/live 且 odds_multi 未返回，表1 Stake/Duel 写—（不沿用陈价）。"
    )
    + f"TT vs LGD id=5958057944 status={oai_status_lgd} live={str(oai_live_lgd).lower()} "
    + f"Stake {stake_tt2}/{stake_lgd}{'†' if dagger else ''} Duel {duel_tt2}/{duel_lgd}{'†' if dagger else ''} "
    + f"（match_watch 未命中 ThunderTalk，已按 event id 直读）。"
    + "PIN JDG/TT 系列 period-0 ML 已撤（父盘 1633881950 不在 matchups；子盘 1634353344 不在 matchups 与 /markets/straight；"
    + "related/straight 404，已回退 /markets/straight）。"
    + (
        f"PIN TT vs LGD 父盘 {pin_tt_parent_id} 仍在列表 status={pin_tt_parent_status} isLive={pin_tt_parent_live}，"
        f"但 period-0 系列 ML 不在 /markets/straight（仅 period 2/3 地图预售 ML），按已撤处理，表1 PIN 写—，不硬算 PIN 套现。"
        f"滚球子盘 1634593525 isLive=True period-0 ML status=closed（地图1，不当系列）。"
        if pin_period0_withdrawn_tt
        else (
            f"PIN 本轮已挂 TT vs LGD 父对阵 {pin_tt_parent_id} period-0 ML {pin_tt_ml_status} "
            f"TT {pin_tt}/{pin_lgd} (Am {pin_tt_am}/{pin_lgd_am}) limit {pin_tt_limit}。"
            if pin_tt_lgd_listed and pin_tt is not None
            else "PIN 本轮仍无 TT vs LGD 父对阵。"
        )
    )
)
md.append("")
md.append("## 表2 套现仓位")
md.append("")
md.append("| 状态 | 事件 | 左买 | 右买 | 成本 | 手续费 | 利率 | 多久结算 | 一单利润 |")
md.append("|---|---|---|---|---:|---:|---:|---|---:|")
md.extend(table2_md)
md.append("")
md.append("## 费后>0.5%（本轮要标出，完整仓位）")
md.append("")
if gt_0p5_paths:
    for g in gt_0p5_paths:
        md.append(
            f"- {g['事件']}：{g['左买']} vs {g['右买']}，成本 {g['成本']}，费 {g['手续费']}，"
            f"利率 {g['利率']}，利润 {g['一单利润']}"
        )
else:
    best_txt = rate_pct_str(best_rate) if best_rate is not None else "—"
    best_label = f"{best['book']}买{best['book_team']}" if best else "—"
    md.append(
        f"无。JDG vs TT 已结束不硬算（已报结束，本轮仍结束；不沿用陈价路径、不升格）。"
        f"TT vs LGD 最佳 {best_label} {best_txt}，滚球不升格。"
    )
md.append("")
md.append("高价值（费后≥1.5%、规则一致）：没有（滚球规则风险，不升格）。")
md.append("")
md.append(f"## 相对 {BASELINE} CST")
md.append("")
md.append(
    "- JDG vs TT：PM 结束→结束（Gamma 1/0 不变；CLOB 404 双边无盘）；"
    "Stake —→—（新刷仍未返回，结束盘已撤）；Duel —→—（新刷仍未返回，结束盘已撤）；PIN —→—。"
    "最佳利率 结束→结束（不硬算）。未把陈价路径当翻正/翻负。"
    "JDG 档1 无→无；TT CLOB 404→CLOB 404 (unused)。状态 结束→结束。"
    f"score {gamma_score}→{gamma_score}。closed True→True；market accepting False→False；uma resolved。"
    "PIN 父盘仍 absent；子盘 1634353344 仍 absent。"
)
sz_tt_chg = f"{base_sz_tt:g}@{base_pm_tt}→{sz_tt_s}份 @{pm_a_tt}"
sz_lgd_chg = f"{base_sz_lgd:g}@{base_pm_lgd}→{sz_lgd_s}份 @{pm_b_lgd}"
pin_now = "—" if pin_tt_use is None else f"{pin_tt_use:g}/{pin_lgd_use:g}"
md.append(
    f"- TT vs LGD：PM {pm_pair(base_pm_tt, base_pm_lgd, pm_a_tt, pm_b_lgd)}；"
    f"Stake {book_pair(base_stake_tt, base_stake_lgd, stake_tt2, stake_lgd)}"
    + ("（429†沿用15:39）" if dagger else "")
    + "；"
    + f"Duel {book_pair(base_duel_tt, base_duel_lgd, duel_tt2, duel_lgd)}"
    + ("（429†沿用15:39）" if dagger else "")
    + "；"
    + f"PIN —→{pin_now}（period-0 系列 ML 仍撤）。"
    + f"最佳利率 {rate_pct_str(base_best)}（Duel买TT）→{rate_pct_str(best_rate)}"
    + (f"（{best['book']}买{best['book_team']}，{best_pp:+.2f}个百分点）".replace("+-", "−").replace("+", "+") if best else "（无路径）")
    + "。"
    + f"TT 档1 {sz_tt_chg}；LGD 档1 {sz_lgd_chg}"
    + ("（档1异常厚）" if l1_thick else "（档1不再异常厚）")
    + "。"
    + ("未翻正/翻负。" if not flip else "出现翻正/翻负。")
    + f"买TT侧：Duel 买LGD {rate_pct_str(base_rates['duel_lgd'])}→{rate_pct_str(cur_rates.get('duel_lgd'))}；"
    + f"Stake 买LGD {rate_pct_str(base_rates['stake_lgd'])}→{rate_pct_str(cur_rates.get('stake_lgd'))}；"
    + "PIN 买LGD —→—。"
    + f"买LGD侧：Duel 买TT {rate_pct_str(base_rates['duel_tt'])}→{rate_pct_str(cur_rates.get('duel_tt'))}；"
    + f"Stake 买TT {rate_pct_str(base_rates['stake_tt'])}→{rate_pct_str(cur_rates.get('stake_tt'))}；"
    + "PIN 买TT —→—。"
    + f"状态 滚球→{status_lgd}。比分 000-000|0-0|Bo3→{gamma_score_lgd}。"
)
md.append(f"- 是否 ≥1.5%：否（滚球不升格）。")
md.append(
    f"- 是否滚球/结束：JDG vs TT 已结束、非滚球（PM live={gamma_live_jdg} closed={gamma_closed_jdg} "
    f"ended={gamma_ended_jdg} accepting={mw_accept_jdg} score={gamma_score}；"
    f"PIN isLive父=False status=absent_from_list period-0=withdrawn；子盘 1634353344 absent）。"
    f"TT vs LGD **仍滚球、未结束**（PM live={gamma_live_lgd} closed={gamma_closed_lgd} ended={gamma_ended_lgd} "
    f"score={gamma_score_lgd}；OAI live={oai_live_lgd} status={oai_status_lgd}；"
    f"PIN 父 isLive={pin_tt_parent_live} status={pin_tt_parent_status} period-0=withdrawn；"
    f"子盘 1634593525 isLive={pin_child_live}）。"
)
reason_txt = "；".join(reasons) if reasons else "无触发项"
md.append(f"- should_send：{should_send}（{reason_txt}）。")
md.append("")

gap_parents = "；".join(parent_desc) if parent_desc else "listed_parents=none"
live_gap = "；".join(live_desc) if live_desc else "no live children"
gaps = [
    f"PIN LPL 199353 本轮 {len(parents)} 场父对阵：JD Gaming/ThunderTalk 1633881950 ABSENT from matchups list "
    f"(child 1634353344 also ABSENT; 17:00 CST 8/20 / 09:00Z)；{gap_parents}。{live_gap}。"
    + (
        f"TT vs LGD 父盘 {pin_tt_parent_id} 在列表但 period-0 系列 ML 不在 /markets/straight（parent_mk={parent_tt_mk} 仅 period 3）；"
        f"地图子盘 1634593525 isLive=True period-0 ML 为地图盘（不当系列，即使 open 也不套现系列）。"
        if pin_period0_withdrawn_tt
        else f"TT vs LGD 已挂父盘 {pin_tt_parent_id} period-0 ML {pin_tt}/{pin_lgd}。"
    )
    + "related/straight 本轮 404，已用 /leagues/199353/markets/straight 回退（200）。",
    (
        "odds-api.io 429 † this round; Stake/Duel TT vs LGD reused 15:39 quotes; JDG/TT not reused (ended)"
        if dagger
        else f"odds-api.io fresh this round (no 429); JDG/TT 7291391184 absent from pending/live; TT/LGD 5958057944 {oai_status_lgd} live={oai_live_lgd} Stake {stake_tt2}/{stake_lgd} Duel {duel_tt2}/{duel_lgd}"
    ),
    f"TT vs LGD Stake updatedAt {stake_upd} {stake_tt2}/{stake_lgd}；Duel updatedAt {duel_upd} {duel_tt2}/{duel_lgd}",
    f"Gamma JDG vs TT bestAsk {mw_jdg.get('bestAsk')} vs CLOB L1 404 (不一致); outcomePrices {prices_jdg}; ended, leftover gone",
    f"Gamma TT vs LGD bestAsk {mw_lgd.get('bestAsk')} vs CLOB L1 {pm_a_tt} "
    f"({'一致' if clob_gamma_match else '不一致，用CLOB'}); outcomePrices {prices_lgd}; live={gamma_live_lgd} score={gamma_score_lgd}",
    "JDG vs TT JDG L1 none→none; TT leftover CLOB 404→CLOB 404 unused",
    f"TT vs LGD TT L1 {base_sz_tt}@{base_pm_tt}→{sz_tt_s}@{pm_a_tt}; LGD L1 {base_sz_lgd}@{base_pm_lgd}→{sz_lgd_s}@{pm_b_lgd}",
    (
        "routine not deleted: JDG vs TT ended (score 000-000|2-1|Bo3), TT vs LGD LIVE 000-000|0-1|Bo3. "
        "BOTH not ended. Parent should NOT delete routine."
        if not both_ended
        else "BOTH matches ended; parent should delete routine (this scan does not delete)."
    ),
]
md.append("数据缺口：" + " ".join(gaps))
md.append("")
md.append("本表只做定价差记录，不是下单建议。")
md.append("")

OUT_MD.write_text("\n".join(md), encoding="utf-8")

# ---- json ----
payload = {
    "scan_cst": SCAN,
    "timezone": "Asia/Shanghai",
    "analysis_only": True,
    "live": is_live,
    "ended": True,  # JDG ended; TT/LGD live not ended
    "jdg_tt_prematch": False,
    "jdg_tt_hours_to_start": round((jdg_start - now).total_seconds() / 3600.0, 1),
    "jdg_tt_mins_past_start": round(mins_past),
    "tt_lgd_days_to_start": round(days_to_tt, 2),
    "tt_lgd_went_live": True,
    "tt_lgd_still_delayed": False,
    "tt_lgd_ended": tt_ended,
    "both_matches_ended": both_ended,
    "high_value_count": 0,
    "high_value": "没有",
    "gt_0p5_count": len(gt_0p5_paths),
    "should_send": should_send,
    "should_send_reasons": reasons,
    "oai_429": dagger,
    "routine_deleted": False,
    "pin_period0_withdrawn": True,
    "pin_period0_withdrawn_tt_lgd": pin_period0_withdrawn_tt,
    "sources": {
        "PM": (
            f"Gamma+CLOB L1 best ask {SCAN} CST; slugs lol-jdg-tt-2026-08-20 / lol-tt-lgd-2026-08-23; "
            f"JDG/TT live={gamma_live_jdg} closed={gamma_closed_jdg} ended={gamma_ended_jdg} "
            f"accepting={mw_accept_jdg} score={gamma_score}; "
            f"TT/LGD live={gamma_live_lgd} closed={gamma_closed_lgd} ended={gamma_ended_lgd} "
            f"accepting={mw_accept_lgd} score={gamma_score_lgd} "
            f"CLOB TT {s_a_tt}@{pm_a_tt} LGD {s_b_lgd}@{pm_b_lgd} "
            f"Gamma bestAsk {mw_lgd.get('bestAsk')} vs CLOB {pm_a_tt} "
            f"{'match' if clob_gamma_match else 'mismatch-use-CLOB'}"
        ),
        "PIN": (
            f"guest 199353 /leagues matchups + /markets/straight fallback (related/straight 404) {SCAN} CST; "
            f"{len(parents)} listed parent(s); JDG/TT 1633881950 ABSENT from matchups nested=None period-0 ML WITHDRAWN; "
            f"child 1634353344 ABSENT; "
            f"TT/LGD parent {pin_tt_parent_id} listed status={pin_tt_parent_status} isLive={pin_tt_parent_live} "
            f"period-0 series ML WITHDRAWN (not in /markets/straight; only period 2/3); "
            f"live child 1634593525 isLive={pin_child_live} period-0 ML closed (map, not series); "
            "today's parents: "
            + (
                "; ".join(f"{'/'.join(str(n) for n in p['names'])} {p['id']}" for p in parents)
                if parents
                else "none"
            )
        ),
        "Stake": (
            f"odds-api.io Split 3 {SCAN} CST "
            + ("(429 †, reused 15:39); " if dagger else "(fresh, no 429); ")
            + f"JDG/TT 7291391184 absent; TT/LGD {stake_tt2}/{stake_lgd} status={oai_status_lgd} live={oai_live_lgd} updatedAt {stake_upd}"
        ),
        "Duel": (
            f"odds-api.io Split 3 {SCAN} CST "
            + ("(429 †, reused 15:39); " if dagger else "(fresh, no 429); ")
            + f"JDG/TT 7291391184 absent; TT/LGD {duel_tt2}/{duel_lgd} status={oai_status_lgd} live={oai_live_lgd} updatedAt {duel_upd}"
        ),
    },
    "vs_1539": {
        "JDG vs TT": {
            "pm": "ended Gamma 1/0 不变 CLOB 404",
            "stake": "—→— (fresh fetch, still absent)",
            "duel": "—→— (fresh fetch, still absent)",
            "pin": "—→—",
            "best_rate": "结束→结束（不硬算）",
            "rate_pp": None,
            "sz_jdg": "无档1→无档1",
            "sz_tt": "CLOB 404→CLOB 404 (unused)",
            "flip": False,
            "status": f"结束→结束 score {gamma_score}→{gamma_score} closed True→True",
            "pin_period0": "withdrawn→withdrawn",
            "pin_parent": "absent_from_list→absent_from_list",
            "pin_child_p0": "absent→absent",
            "score": f"{gamma_score}→{gamma_score}",
        },
        "TT vs LGD": {
            "pm": pm_pair(base_pm_tt, base_pm_lgd, pm_a_tt, pm_b_lgd),
            "stake": book_pair(base_stake_tt, base_stake_lgd, stake_tt2, stake_lgd)
            + ("（429†沿用15:39）" if dagger else ""),
            "duel": book_pair(base_duel_tt, base_duel_lgd, duel_tt2, duel_lgd)
            + ("（429†沿用15:39）" if dagger else ""),
            "pin": "—→— (period-0 still withdrawn)",
            "best_rate": f"{rate_pct_str(base_best)}→{rate_pct_str(best_rate)}",
            "rate_pp": round(best_pp, 4) if best_rate is not None else None,
            "sz_tt": f"{base_sz_tt}@{base_pm_tt}→{sz_tt_s}@{pm_a_tt}",
            "sz_lgd": f"{base_sz_lgd}@{base_pm_lgd}→{sz_lgd_s}@{pm_b_lgd}",
            "path_duel_lgd": f"{rate_pct_str(base_rates['duel_lgd'])}→{rate_pct_str(cur_rates.get('duel_lgd'))}",
            "path_stake_lgd": f"{rate_pct_str(base_rates['stake_lgd'])}→{rate_pct_str(cur_rates.get('stake_lgd'))}",
            "path_duel_tt": f"{rate_pct_str(base_rates['duel_tt'])}→{rate_pct_str(cur_rates.get('duel_tt'))}",
            "path_stake_tt": f"{rate_pct_str(base_rates['stake_tt'])}→{rate_pct_str(cur_rates.get('stake_tt'))}",
            "path_pin_tt": "—→—",
            "path_pin_lgd": "—→—",
            "status": f"滚球→{status_lgd} score 000-000|0-0|Bo3→{gamma_score_lgd}",
            "went_live": False,
            "pin_period0": "withdrawn→withdrawn",
        },
        "ge_1p5": False,
        "ge_1p5_formula_blocked_429": [],
        "live_change": False,
        "ended_change": False,
        "pm_ask_ge_0p02": pm_ask_ge_0p02,
        "pm_ask_jdg_tt_delta": 0.0,
        "pm_ask_tt_lgd_delta": round(max(pm_ask_delta_tt, pm_ask_delta_lgd), 4),
        "books_moved": books_moved,
        "books_move_detail": books_move_detail,
        "flip": flip,
        "oai_429": dagger,
        "max_abs_path_dpp": round(max_abs_path_dpp, 4),
        "pin_listed": pin_tt_lgd_listed,
        "pin_period0_withdrawn": pin_period0_withdrawn_tt,
        "score_change": True,
        "score_from": "000-000|0-0|Bo3",
        "score_to": gamma_score_lgd,
        "pin_child_p0_change": True,
        "pin_parent_absent": pin_parent_absent_jdg,
        "pin_child_absent": pin_child_absent_jdg,
        "lgd_l1_size_delta": round((s_b_lgd or 0) - base_sz_lgd, 2),
        "tt_l1_size_delta": round((s_a_tt or 0) - base_sz_tt, 2),
    },
    "table1": [
        {
            "状态": "结束",
            "事件": "JDG vs TT",
            "队A": "JDG",
            "队B": "TT",
            "PM_A": None,
            "PM_B": None,
            "PIN_A": None,
            "PIN_B": None,
            "Stake_A": None,
            "Stake_B": None,
            "Duel_A": None,
            "Duel_B": None,
            "stake_duel_stale": False,
            "oai_429": dagger,
            "pm_A_sz": None,
            "pm_B_sz": None,
            "slug": "lol-jdg-tt-2026-08-20",
            "pm_start_cst": "2026-08-20 17:00",
            "oai_id": 7291391184,
            "oai_status": oai_status_jdg,
            "oai_live": False,
            "stake_updated": None,
            "duel_updated": None,
            "l1_thick": False,
            "gamma_bestAsk_A": float(mw_jdg.get("bestAsk") or 1),
            "clob_ask_A": None,
            "clob_ask_B_leftover": None,
            "clob_sz_B_leftover": None,
            "clob_error": clob_err_jdg or "No orderbook exists for the requested token id",
            "gamma_outcomePrices": prices_jdg,
            "gamma_live": gamma_live_jdg,
            "gamma_closed": gamma_closed_jdg,
            "gamma_ended": gamma_ended_jdg,
            "gamma_acceptingOrders": mw_accept_jdg,
            "gamma_event_acceptingOrders": ev_accept_jdg,
            "gamma_score": gamma_score,
            "umaResolutionStatus": mw_uma,
            "pin_matchup_id": 1633881950,
            "pin_american": None,
            "pin_limit": None,
            "pin_status": "absent_from_list",
            "pin_live": False,
            "pin_child_live": False,
            "pin_period0_ml_status": "withdrawn",
            "pin_period0_withdrawn": True,
            "pin_parent_absent_from_list": True,
            "pin_nested_isLive": None,
            "pin_nested_hasMarkets": None,
            "pin_child_1634353344_isLive": None,
            "pin_child_1634353344_period0": None,
            "pin_child_absent": True,
            "ended_no_cashout": True,
        },
        {
            "状态": status_lgd,
            "事件": "TT vs LGD",
            "队A": "TT",
            "队B": "LGD",
            "PM_A": pm_a_tt,
            "PM_B": pm_b_lgd,
            "PIN_A": pin_tt_use,
            "PIN_B": pin_lgd_use,
            "Stake_A": stake_tt2,
            "Stake_B": stake_lgd,
            "Duel_A": duel_tt2,
            "Duel_B": duel_lgd,
            "stake_duel_stale": dagger,
            "oai_429": dagger,
            "pm_A_sz": s_a_tt,
            "pm_B_sz": s_b_lgd,
            "slug": "lol-tt-lgd-2026-08-23",
            "pm_start_cst": "2026-08-23 15:00",
            "oai_id": 5958057944,
            "oai_status": oai_status_lgd,
            "oai_live": oai_live_lgd,
            "stake_updated": stake_upd,
            "duel_updated": duel_upd,
            "l1_thick": l1_thick,
            "gamma_bestAsk_A": float(mw_lgd.get("bestAsk") or 0) if mw_lgd.get("bestAsk") is not None else None,
            "clob_ask_A": pm_a_tt,
            "clob_ask_B": pm_b_lgd,
            "gamma_outcomePrices": prices_lgd,
            "gamma_live": gamma_live_lgd,
            "gamma_closed": gamma_closed_lgd,
            "gamma_ended": gamma_ended_lgd,
            "gamma_acceptingOrders": mw_accept_lgd,
            "gamma_event_acceptingOrders": ev_accept_lgd,
            "gamma_score": gamma_score_lgd,
            "pin_listed": pin_tt_lgd_listed,
            "pin_matchup_id": pin_tt_parent_id,
            "pin_american": None,
            "pin_limit": None,
            "pin_status": "period0_withdrawn",
            "pin_live": pin_any_live,
            "pin_parent_status": pin_tt_parent_status,
            "pin_parent_isLive": pin_tt_parent_live,
            "pin_period0_withdrawn": pin_period0_withdrawn_tt,
            "pin_child_1634593525_isLive": pin_child_live,
        },
    ],
    "table2": table2_json,
    "gt_0p5_paths": gt_0p5_paths,
    "data_gaps": gaps,
}

OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("WROTE", OUT_MD, "scan", SCAN)
print("WROTE", OUT_JSON)
print("should_send", should_send, reasons)
print("status_lgd", status_lgd, "live", is_live, "tt_ended", tt_ended, "both_ended", both_ended)
print("best", rate_pct_str(best_rate) if best_rate is not None else None, "pp", round(best_pp, 4) if best else None)
print("PM", pm_a_tt, pm_b_lgd, "sz", s_a_tt, s_b_lgd)
print("Stake", stake_tt2, stake_lgd, "Duel", duel_tt2, duel_lgd)
print("PIN", pin_tt_use, pin_lgd_use, "p0_withdrawn", pin_period0_withdrawn_tt)
print("paths", [(r["book"], r["book_team"], rate_pct_str(r["rate"]), round(r["profit"], 1)) for _, r, _ in paths_sorted])
print("oai_429", dagger, "gt_0p5", len(gt_0p5_paths))
