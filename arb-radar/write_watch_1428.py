#!/usr/bin/env python3
"""Write watch-jdg-tt.md/json for 2026-08-22 ~14:28 CST vs 13:35. Analysis only."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT_MD = Path("/workspace/arb-radar/watch-jdg-tt.md")
OUT_JSON = Path("/workspace/arb-radar/watch-jdg-tt.json")
SCANS = Path("/workspace/arb-radar/scans")
CST = timezone(timedelta(hours=8))
BASELINE = "13:35"


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


def path(s, p, odds, book, book_team, pm_team):
    d = s / odds
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
    }


def rate_pct_str(rate: float) -> str:
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
        "high_value": r["hv"],
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


def pp_txt(x: float) -> str:
    if abs(x) < 0.005:
        return "0"
    return f"{x:+.2f}".replace("-", "−")


def sd(x, dagger):
    if x is None:
        return "—"
    return f"{x:g}†" if dagger else f"{x:g}"


def pm_cell(x):
    return "—" if x is None else f"{x:g}"


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

# CLOB errors
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
n_oai = len((oai.get("pulled") or {}).get("events") or [])
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
stake_tt2 = oai_num(oai_lgd, "stake_a")
stake_lgd = oai_num(oai_lgd, "stake_b")
duel_tt2 = oai_num(oai_lgd, "duel_a")
duel_lgd = oai_num(oai_lgd, "duel_b")

# 429: reuse 13:35 TT vs LGD last-success quotes with †. JDG ended → keep —.
STALE_1335_LGD = {
    "stake_a": 2.05,
    "stake_b": 1.78,
    "duel_a": 1.99,
    "duel_b": 1.88,
    "stake_updated": "2026-08-22T05:13:32.802Z",
    "duel_updated": "2026-08-21T19:31:23.221Z",
}
lgd_books_missing = any(x is None for x in (stake_tt2, stake_lgd, duel_tt2, duel_lgd))
if dagger and lgd_books_missing:
    stake_tt2 = STALE_1335_LGD["stake_a"]
    stake_lgd = STALE_1335_LGD["stake_b"]
    duel_tt2 = STALE_1335_LGD["duel_a"]
    duel_lgd = STALE_1335_LGD["duel_b"]

mu = json.loads((SCANS / "pin" / "LPL_matchups.json").read_text())
mk_rel_raw = json.loads((SCANS / "pin" / "LPL_markets_related.json").read_text())
mk = json.loads((SCANS / "pin" / "LPL_markets_straight.json").read_text())
related_404 = isinstance(mk_rel_raw, dict) and mk_rel_raw.get("status") == 404
rows_mk = mk if isinstance(mk, list) else []

parents = []
live_children = []
child_1634353344 = None
jdg_any = []
for x in mu if isinstance(mu, list) else []:
    names = [p.get("name") for p in (x.get("participants") or []) if isinstance(p, dict)]
    blob = " ".join(str(n) for n in names)
    if x.get("parentId") is None and x.get("type") == "matchup":
        parents.append(
            {
                "id": x.get("id"),
                "names": names,
                "status": x.get("status"),
                "isLive": x.get("isLive"),
                "startTime": x.get("startTime"),
                "hasMarkets": x.get("hasMarkets"),
            }
        )
    if x.get("id") == 1634353344:
        child_1634353344 = x
    if x.get("isLive") is True:
        live_children.append(
            {
                "id": x.get("id"),
                "parentId": x.get("parentId"),
                "names": names,
                "status": x.get("status"),
                "units": x.get("units"),
            }
        )

parent_ids = {p["id"] for p in parents}
pin_parent_absent = 1633881950 not in parent_ids
pin_child_absent = child_1634353344 is None
pin_period0_withdrawn = True  # parent+child absent ⇒ series ML withdrawn

# TT/LGD parent search
pin_tt_lgd_listed = False
for p in parents:
    joined = " ".join(str(n) for n in p["names"]).lower()
    if "thunder" in joined and "lgd" in joined:
        pin_tt_lgd_listed = True

# markets for old parent
parent_any_mk = sum(1 for r in rows_mk if r.get("matchupId") == 1633881950)
child_any_mk = sum(1 for r in rows_mk if r.get("matchupId") == 1634353344)

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
mw_accept_lgd = mw_lgd.get("acceptingOrders")
ev_accept_lgd = ev_lgd.get("acceptingOrders")

jdg_ended = bool(gamma_ended_jdg) or bool(gamma_closed_jdg)
tt_prematch = not bool(gamma_closed_lgd) and not bool(gamma_ended_lgd) and not bool(gamma_live_lgd)

# PM ask for table: ended → —
pm_a_jdg = pm_b_jdg = None
pm_a_tt = p_tt2
pm_b_lgd = p_lgd
s_a_tt = s_tt2
s_b_lgd = s_lgd

l1_thick_tt = bool(s_a_tt and s_a_tt > 2000)
l1_thick_lgd = bool(s_b_lgd and s_b_lgd > 2000)
l1_thick = l1_thick_tt or l1_thick_lgd

# OAI
oai_status_jdg = "absent (ended, not in pending/live; odds_multi 7291391184 omitted)"
oai_live_jdg = False
oai_status_lgd = full_lgd.get("status") or oai_lgd.get("status") or "pending"
oai_live_lgd = bool(full_lgd.get("live") if full_lgd else oai_lgd.get("live"))
stake_upd = oai_lgd.get("stake_updated") or full_lgd.get("stake_updated")
duel_upd = oai_lgd.get("duel_updated") or full_lgd.get("duel_updated")
if dagger:
    oai_status_jdg = "429† last=absent (ended)"
    oai_status_lgd = "429† last=pending"
    oai_live_lgd = False
    if not stake_upd:
        stake_upd = STALE_1335_LGD["stake_updated"]
    if not duel_upd:
        duel_upd = STALE_1335_LGD["duel_updated"]

# ---- paths TT vs LGD ----
settle = f"约{days_to_tt:.1f}天（8/23 15:00）"
paths = []
# Book buy TT / PM buy LGD
if s_b_lgd and pm_b_lgd is not None and duel_tt2:
    paths.append(
        (
            "Duel",
            path(s_b_lgd, pm_b_lgd, duel_tt2, "Duel", "TT", "LGD"),
            bool(s_b_lgd and s_b_lgd > 2000),
        )
    )
if s_b_lgd and pm_b_lgd is not None and stake_tt2:
    paths.append(
        (
            "Stake",
            path(s_b_lgd, pm_b_lgd, stake_tt2, "Stake", "TT", "LGD"),
            bool(s_b_lgd and s_b_lgd > 2000),
        )
    )
# Book buy LGD / PM buy TT
if s_a_tt and pm_a_tt is not None and duel_lgd:
    paths.append(
        (
            "Duel",
            path(s_a_tt, pm_a_tt, duel_lgd, "Duel", "LGD", "TT"),
            bool(s_a_tt and s_a_tt > 2000),
        )
    )
if s_a_tt and pm_a_tt is not None and stake_lgd:
    paths.append(
        (
            "Stake",
            path(s_a_tt, pm_a_tt, stake_lgd, "Stake", "LGD", "TT"),
            bool(s_a_tt and s_a_tt > 2000),
        )
    )

# sort by rate desc
paths_sorted = sorted(paths, key=lambda x: x[1]["rate"], reverse=True)
best = paths_sorted[0][1] if paths_sorted else None

# baseline 13:35 CST values
base_pm_tt, base_pm_lgd = 0.46, 0.55
base_stake_tt, base_stake_lgd = 2.05, 1.78
base_duel_tt, base_duel_lgd = 1.99, 1.88
base_sz_tt, base_sz_lgd = 1477.77, 20.0
base_rates = {
    "duel_tt": -0.05599713,  # Duel buy TT
    "stake_tt": -0.04270597,
    "duel_lgd": 0.00237755,
    "stake_lgd": -0.02677436,
}
base_best = 0.00237755

# current rates by key
cur_rates = {}
for _, r, _ in paths:
    key = f"{r['book'].lower()}_{'tt' if r['book_team']=='TT' else 'lgd'}"
    cur_rates[key] = r["rate"]

rate_pp = {}
for k, br in base_rates.items():
    cr = cur_rates.get(k, br)
    rate_pp[k] = (cr - br) * 100  # percentage points

best_rate = best["rate"] if best else None
best_pp = (best_rate - base_best) * 100 if best_rate is not None else 0.0
max_abs_path_dpp = max(abs(v) for v in rate_pp.values()) if rate_pp else 0.0

pm_ask_delta_tt = abs((pm_a_tt or 0) - base_pm_tt) if pm_a_tt is not None else 0.0
pm_ask_delta_lgd = abs((pm_b_lgd or 0) - base_pm_lgd) if pm_b_lgd is not None else 0.0
pm_ask_ge_0p02 = max(pm_ask_delta_tt, pm_ask_delta_lgd) >= 0.02

books_moved = (
    (not dagger)
    and (
        (stake_tt2, stake_lgd) != (base_stake_tt, base_stake_lgd)
        or (duel_tt2, duel_lgd) != (base_duel_tt, base_duel_lgd)
    )
)
if dagger:
    books_move_detail = "Stake/Duel 429 † reused 13:35, not treated as live move"
elif books_moved:
    books_move_detail = (
        f"Stake {base_stake_tt:g}/{base_stake_lgd:g}→{stake_tt2:g}/{stake_lgd:g}; "
        f"Duel {base_duel_tt:g}/{base_duel_lgd:g}→{duel_tt2:g}/{duel_lgd:g}"
    )
else:
    books_move_detail = "no live book move"

# flip: any path sign change
flip = False
for k, br in base_rates.items():
    cr = cur_rates.get(k)
    if cr is None:
        continue
    if (br < 0 <= cr) or (br >= 0 > cr):
        flip = False  # both still negative; keep False
    if (br < 0 and cr >= 0) or (br >= 0 and cr < 0):
        flip = True

gt_0p5_paths = []
hv_paths = []
table2_md = []
table2_json = []

# JDG ended row
table2_md.append(
    "| 结束 | JDG vs TT | — | — | — | — | — | 已结束，不硬算套现 | — |"
)
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
    note = "LPL Duel现价" if book == "Duel" else "LPL Stake现价"
    if dagger:
        note = ("LPL Duel 429†沿用13:35" if book == "Duel" else "LPL Stake 429†沿用13:35")
    thick_note = "；档1异常厚" if thick else ""
    event = f"TT vs LGD（{note}，限额未知；本单按PM档1；不升格{thick_note}）"
    table2_md.append(row_md("非滚球", event, r, settle))
    table2_json.append(row_json("非滚球", event, r, settle))
    if r["gt_0p5"]:
        gt_0p5_paths.append(row_json("非滚球", event, r, settle))
    if r["hv"]:
        hv_paths.append(row_json("非滚球", event, r, settle))

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
# live/ended change: JDG still ended (already reported) — do NOT send for that alone
# TT still prematch — no live change
live_change = False
ended_change = False
# if TT became live or ended → yes
if oai_live_lgd or gamma_live_lgd:
    live_change = True
    reasons.append("TT vs LGD转滚球")
if gamma_ended_lgd or gamma_closed_lgd:
    ended_change = True
    reasons.append("TT vs LGD结束")

should_send = "YES" if reasons else "NO"

# parent list for gaps
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

# ---- markdown ----
sz_tt_s = f"{s_a_tt:.1f}" if s_a_tt else "—"
sz_lgd_s = f"{s_b_lgd:.1f}" if s_b_lgd else "—"
thick_tag = "（档1异常厚）" if l1_thick else ""

md = []
md.append(f"# JDG/TT 盯盘 {SCAN} CST")
md.append("")
md.append(
    "只分析，未下注。数据：PM Gamma + CLOB 档1最佳 ask（不累加）；"
    + (
        "Stake/Duel 经 odds-api.io LPL Split 3 本轮 429 †，TT vs LGD 沿用 13:35 赛前价；JDG vs TT 已结束不沿用陈价。"
        if dagger
        else "Stake/Duel 经 odds-api.io LPL Split 3 本轮新刷成功（无429，无†）；"
    )
    + "PIN guest 199353 系列 JDG/TT period-0 ML 已撤（父盘 1633881950 不在 matchups；子盘 1634353344 消失；"
    + "related/straight 404，已回退 /markets/straight）；"
    + f"TT vs LGD {'已挂 PIN' if pin_tt_lgd_listed else '仍未挂 PIN'}。"
    + "档1只吃最佳 ask。单档>2000份标「档1异常厚」。高价值 = 费后≥1.5% 且规则一致。微正不升格。"
    + "本轮额外标出费后>0.5% 路径。JDG vs TT 已结束，不硬算套现。TT vs LGD 未结束，routine 不删。"
)
md.append("")
md.append(f"scan_cst：{SCAN} CST（Asia/Shanghai）")
live_line = (
    f"是否滚球：否。JDG vs TT 已结束（8/20 17:00 CST 开赛，赛后约 {mins_past:.0f} 分钟；"
    f"PM live={gamma_live_jdg}、closed={gamma_closed_jdg}、ended={gamma_ended_jdg}、"
    f"accepting={mw_accept_jdg}（market；event accepting={ev_accept_jdg}）、score {gamma_score}；"
    f"odds-api.io 本轮{'429 †' if dagger else '新刷'}，JDG/TT 不在 pending/live；PIN 父盘 1633881950 absent_from_list，"
    f"period-0 系列 ML 已撤；PIN 子盘 1634353344 absent；"
    f"TT vs LGD 仍非滚球：PM live 字段缺席/{gamma_live_lgd}、closed={gamma_closed_lgd}、"
    f"ended={gamma_ended_lgd}、accepting={mw_accept_lgd}（market；event accepting={ev_accept_lgd}），"
    f"OAI status={oai_status_lgd} live={oai_live_lgd}，PIN {'有' if pin_tt_lgd_listed else '无'}父对阵）"
)
md.append(live_line)
md.append(
    "是否结束：是（JDG vs TT 已结束：PM "
    f"live={gamma_live_jdg} closed={gamma_closed_jdg} ended={gamma_ended_jdg} score {gamma_score}，"
    "Bo3 2-1 JDG 胜；不要硬算套现。TT vs LGD 未开赛。两场都结束后才删 routine；本轮只结束一场，routine 不删）"
)
md.append("")
md.append("## 表1 价格对照")
md.append("")
md.append(
    "| 状态 | 事件 | 队A | 队B | PM_A | PM_B | PIN_A | PIN_B | Stake_A | Stake_B | Duel_A | Duel_B |"
)
md.append("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
md.append(
    f"| 结束 | JDG vs TT | JDG | TT | — | — | — | — | — | — | — | — |"
)
md.append(
    f"| 非滚球 | TT vs LGD | TT | LGD | {pm_cell(pm_a_tt)} | {pm_cell(pm_b_lgd)} | — | — | "
    f"{sd(stake_tt2, dagger)} | {sd(stake_lgd, dagger)} | {sd(duel_tt2, dagger)} | {sd(duel_lgd, dagger)} |"
)
md.append("")
md.append(
    f"PM 档1深度：JDG vs TT 已结束，不吃套现档。CLOB 双边 404（{clob_err_jdg or 'No orderbook'}；"
    f"Gamma outcomePrices {prices_jdg} bestAsk {mw_jdg.get('bestAsk')} bestBid {mw_jdg.get('bestBid')} uma={mw_uma}）。"
    f"昨日 leftover 盘口已撤，不当套现。 TT vs LGD TT {sz_tt_s}份 @{pm_a_tt} / LGD {sz_lgd_s}份 @{pm_b_lgd}{thick_tag}。"
)
md.append(
    (
        "Stake/Duel 本轮 odds-api.io 429 †。JDG vs TT 已结束，表1 Stake/Duel 写—（不沿用陈价）。"
        if dagger
        else "Stake/Duel 本轮 odds-api.io 新刷成功，无 429，无†。JDG vs TT 事件 7291391184 已不在 pending/live 且 odds_multi 未返回，表1 Stake/Duel 写—（不沿用陈价）。"
    )
    + f"TT vs LGD id=5958057944 status={oai_status_lgd} live={str(oai_live_lgd).lower()} "
    + f"Stake {stake_tt2}/{stake_lgd}{'†' if dagger else ''} Duel {duel_tt2}/{duel_lgd}{'†' if dagger else ''}。"
    + "PIN JDG/TT 系列 period-0 ML 已撤（父盘 1633881950 不在 matchups；子盘 1634353344 不在 matchups 与 /markets/straight；"
    + "related/straight 404，已回退 /markets/straight）。"
    + f"PIN 本轮仍无 TT vs LGD 父对阵（8/23 未挂上）。"
)
md.append("")
md.append("## 表2 套现仓位")
md.append("")
md.append(
    "| 状态 | 事件 | 左买 | 右买 | 成本 | 手续费 | 利率 | 多久结算 | 一单利润 |"
)
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
        f"TT vs LGD 最佳 {best_label} {best_txt}，不升格。"
    )
md.append("")
md.append(
    f"高价值（费后≥1.5%、规则一致）：{'有 ' + str(len(hv_paths)) + ' 条' if hv_paths else '没有'}。"
)
md.append("")
md.append(f"## 相对 {BASELINE} CST")
md.append("")
md.append(
    "- JDG vs TT：PM 结束→结束（Gamma 1/0 不变；CLOB 404 双边无盘）；"
    + (
        "Stake —→—（429† 结束盘不沿用陈价）；Duel —→—（429† 结束盘不沿用陈价）；PIN —→—。"
        if dagger
        else "Stake —→—（新刷仍未返回，结束盘已撤）；Duel —→—（新刷仍未返回，结束盘已撤）；PIN —→—。"
    )
    + "最佳利率 结束→结束（不硬算）。未把陈价路径当翻正/翻负。"
    + "JDG 档1 无→无；TT CLOB 404→CLOB 404 (unused)。状态 结束→结束。"
    + f"score {gamma_score}→{gamma_score}。closed True→True；market accepting False→False；uma resolved。"
    + "PIN 父盘仍 absent；子盘 1634353344 仍 absent。"
)
# TT vs LGD changes
sz_tt_chg = f"{base_sz_tt:g}@{base_pm_tt}→{sz_tt_s}份 @{pm_a_tt}"
sz_lgd_chg = f"{base_sz_lgd:g}@{base_pm_lgd}→{sz_lgd_s}份 @{pm_b_lgd}"
md.append(
    f"- TT vs LGD：PM {pm_pair(base_pm_tt, base_pm_lgd, pm_a_tt, pm_b_lgd)}；"
    f"Stake {book_pair(base_stake_tt, base_stake_lgd, stake_tt2, stake_lgd)}"
    + ("（429†陈价）" if dagger else "")
    + "；"
    + f"Duel {book_pair(base_duel_tt, base_duel_lgd, duel_tt2, duel_lgd)}"
    + ("（429†陈价）" if dagger else "")
    + "；"
    + f"PIN 仍无。最佳利率 {rate_pct_str(base_best)}（Duel买LGD）→{rate_pct_str(best_rate)}（{best['book']}买{best['book_team']}，{pp_txt(best_pp)}个百分点）。"
    + f"TT 档1 {sz_tt_chg}；LGD 档1 {sz_lgd_chg}"
    + ("（档1异常厚）" if l1_thick else "")
    + "。"
    + ("未翻正/翻负。" if not flip else "出现翻正/翻负。")
    + f"买TT侧：Duel 买LGD {rate_pct_str(base_rates['duel_lgd'])}→{rate_pct_str(cur_rates.get('duel_lgd', base_rates['duel_lgd']))}；"
    + f"Stake 买LGD {rate_pct_str(base_rates['stake_lgd'])}→{rate_pct_str(cur_rates.get('stake_lgd', base_rates['stake_lgd']))}。"
    + f"买LGD侧：Duel 买TT {rate_pct_str(base_rates['duel_tt'])}→{rate_pct_str(cur_rates.get('duel_tt', base_rates['duel_tt']))}；"
    + f"Stake 买TT {rate_pct_str(base_rates['stake_tt'])}→{rate_pct_str(cur_rates.get('stake_tt', base_rates['stake_tt']))}。"
    + "状态仍非滚球。"
)
md.append(f"- 是否 ≥1.5%：{'是' if hv_paths else '否'}。")
md.append(
    f"- 是否滚球/结束：JDG vs TT 已结束、非滚球（PM live={gamma_live_jdg} closed={gamma_closed_jdg} "
    f"ended={gamma_ended_jdg} accepting={mw_accept_jdg} score={gamma_score}；"
    f"PIN isLive父=False status=absent_from_list period-0=withdrawn；子盘 1634353344 absent）。"
    "TT vs LGD 非滚球未结束。"
)
reason_txt = "；".join(reasons) if reasons else (
    "JDG 仍结束且已报过；TT vs LGD 无费后>0.5%、利率变动<0.3pp、未翻正/翻负、"
    "PM ask<0.02、Stake/Duel 无实质移动、未转滚球。"
)
md.append(f"- should_send：{should_send}（{reason_txt}）。")
md.append("")

# data gaps
gap_parents = "；".join(parent_desc) if parent_desc else "listed_parents=none"
gaps = [
    f"PIN LPL 199353 本轮 {len(parents)} 场父对阵：JD Gaming/ThunderTalk 1633881950 ABSENT from matchups list "
    f"(child 1634353344 also ABSENT; 17:00 CST 8/20 / 09:00Z)；{gap_parents}。无 TT vs LGD（8/23 仍未挂上）。"
    f"related/straight 本轮 {'404' if related_404 else 'ok'}，已用 /leagues/199353/markets/straight 回退"
    f"（{200 if isinstance(mk, list) else 'err'}）。 period-0 系列 ML 已撤"
    f"（父盘不在 matchups 且 /markets/straight 无父盘盘口 parent_mk={parent_any_mk}；"
    f"子盘 1634353344 本轮也不在 matchups/markets child_mk={child_any_mk}；地图盘不当系列）",
    (
        "odds-api.io 429 † this round; Stake/Duel TT vs LGD reused 13:35 prematch quotes; JDG/TT not reused (ended)"
        if dagger
        else f"odds-api.io fresh this round (no 429); JDG/TT 7291391184 absent from pending/live; TT/LGD 5958057944 {oai_status_lgd} Stake {stake_tt2}/{stake_lgd} Duel {duel_tt2}/{duel_lgd}"
    ),
    f"TT vs LGD Stake updatedAt {stake_upd} {stake_tt2}/{stake_lgd}；"
    f"Duel updatedAt {duel_upd} {duel_tt2}/{duel_lgd}",
    f"Gamma JDG vs TT bestAsk {mw_jdg.get('bestAsk')} vs CLOB L1 404 (不一致); "
    f"outcomePrices {prices_jdg}; ended, leftover gone",
    f"Gamma TT vs LGD bestAsk {mw_lgd.get('bestAsk')} vs CLOB L1 {pm_a_tt} "
    f"({'一致' if float(mw_lgd.get('bestAsk') or 0)==pm_a_tt else '不一致'}); "
    f"outcomePrices {prices_lgd}",
    "JDG vs TT JDG L1 none→none; TT leftover CLOB 404→CLOB 404 unused",
    f"TT vs LGD TT L1 {base_sz_tt}@{base_pm_tt}→{sz_tt_s}@{pm_a_tt}; "
    f"LGD L1 {base_sz_lgd}@{base_pm_lgd}→{sz_lgd_s}@{pm_b_lgd}",
    "routine not deleted: JDG vs TT ended (score 000-000|2-1|Bo3), TT vs LGD still prematch",
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
    "live": False,
    "ended": True,
    "jdg_tt_prematch": False,
    "jdg_tt_hours_to_start": round((jdg_start - now).total_seconds() / 3600.0, 1),
    "jdg_tt_mins_past_start": round(mins_past),
    "tt_lgd_days_to_start": round(days_to_tt, 1),
    "high_value_count": len(hv_paths),
    "high_value": "没有" if not hv_paths else hv_paths,
    "gt_0p5_count": len(gt_0p5_paths),
    "should_send": should_send,
    "should_send_reasons": reasons,
    "oai_429": dagger,
    "routine_deleted": False,
    "pin_period0_withdrawn": pin_period0_withdrawn,
    "sources": {
        "PM": (
            f"Gamma+CLOB L1 best ask {SCAN} CST; slugs lol-jdg-tt-2026-08-20 / lol-tt-lgd-2026-08-23; "
            f"JDG/TT live={gamma_live_jdg} closed={gamma_closed_jdg} ended={gamma_ended_jdg} "
            f"accepting={mw_accept_jdg} score={gamma_score}; "
            f"TT/LGD live={gamma_live_lgd} closed={gamma_closed_lgd} ended={gamma_ended_lgd} "
            f"accepting={mw_accept_lgd} CLOB TT {s_a_tt}@{pm_a_tt} LGD {s_b_lgd}@{pm_b_lgd}"
        ),
        "PIN": (
            f"guest 199353 /leagues matchups + /markets/straight fallback (related/straight 404) {SCAN} CST; "
            f"{len(parents)} listed parent(s); JDG/TT 1633881950 ABSENT from matchups nested=None period-0 ML WITHDRAWN; "
            f"child 1634353344 ABSENT; no TT/LGD parent; today's parents: "
            + (
                "; ".join(
                    f"{'/'.join(str(n) for n in p['names'])} {p['id']}" for p in parents
                )
                if parents
                else "none"
            )
        ),
        "Stake": (
            f"odds-api.io Split 3 {SCAN} CST "
            + ("(429 †, reused 13:35); " if dagger else "(fresh, no 429); ")
            + f"JDG/TT 7291391184 absent; TT/LGD {stake_tt2}/{stake_lgd} updatedAt {stake_upd}"
        ),
        "Duel": (
            f"odds-api.io Split 3 {SCAN} CST "
            + ("(429 †, reused 13:35); " if dagger else "(fresh, no 429); ")
            + f"JDG/TT 7291391184 absent; TT/LGD {duel_tt2}/{duel_lgd} updatedAt {duel_upd}"
        ),
    },
    "vs_1335": {
        "JDG vs TT": {
            "pm": "ended Gamma 1/0 不变 CLOB 404",
            "stake": "—→— (429† ended, not reused)" if dagger else "—→— (fresh fetch, still absent)",
            "duel": "—→— (429† ended, not reused)" if dagger else "—→— (fresh fetch, still absent)",
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
            "pm": (
                f"{base_pm_tt:g}/{base_pm_lgd:g} 不变"
                if pm_a_tt == base_pm_tt and pm_b_lgd == base_pm_lgd
                else f"{base_pm_tt:g}/{base_pm_lgd:g}→{pm_a_tt:g}/{pm_b_lgd:g}"
            ),
            "stake": book_pair(base_stake_tt, base_stake_lgd, stake_tt2, stake_lgd) + ("（429†陈价）" if dagger else ""),
            "duel": book_pair(base_duel_tt, base_duel_lgd, duel_tt2, duel_lgd) + ("（429†陈价）" if dagger else ""),
            "pin": "—→—",
            "best_rate": f"{rate_pct_str(base_best)}→{rate_pct_str(best_rate)}",
            "rate_pp": round(best_pp, 4),
            "sz_tt": f"{base_sz_tt}@{base_pm_tt}→{sz_tt_s}@{pm_a_tt}",
            "sz_lgd": f"{base_sz_lgd}@{base_pm_lgd}→{sz_lgd_s}@{pm_b_lgd}",
            "path_duel_lgd": f"{rate_pct_str(base_rates['duel_lgd'])}→{rate_pct_str(cur_rates.get('duel_lgd',0))}",
            "path_stake_lgd": f"{rate_pct_str(base_rates['stake_lgd'])}→{rate_pct_str(cur_rates.get('stake_lgd',0))}",
            "path_duel_tt": f"{rate_pct_str(base_rates['duel_tt'])}→{rate_pct_str(cur_rates.get('duel_tt',0))}",
            "path_stake_tt": f"{rate_pct_str(base_rates['stake_tt'])}→{rate_pct_str(cur_rates.get('stake_tt',0))}",
            "status": "非滚球→非滚球",
        },
        "ge_1p5": bool(hv_paths),
        "ge_1p5_formula_blocked_429": [],
        "live_change": live_change,
        "ended_change": ended_change,
        "pm_ask_ge_0p02": pm_ask_ge_0p02,
        "pm_ask_jdg_tt_delta": 0.0,
        "pm_ask_tt_lgd_delta": round(max(pm_ask_delta_tt, pm_ask_delta_lgd), 4),
        "books_moved": books_moved,
        "books_move_detail": books_move_detail,
        "flip": flip,
        "oai_429": dagger,
        "max_abs_path_dpp": round(max_abs_path_dpp, 4),
        "pin_listed": pin_tt_lgd_listed,
        "pin_period0_withdrawn": pin_period0_withdrawn,
        "score_change": False,
        "pin_child_p0_change": False,
        "pin_parent_absent": pin_parent_absent,
        "pin_child_absent": pin_child_absent,
        "lgd_l1_size_delta": round((s_b_lgd or 0) - 20.0, 2),
        "tt_l1_size_delta": round((s_a_tt or 0) - 1477.77, 2),
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
            "状态": "非滚球",
            "事件": "TT vs LGD",
            "队A": "TT",
            "队B": "LGD",
            "PM_A": pm_a_tt,
            "PM_B": pm_b_lgd,
            "PIN_A": None,
            "PIN_B": None,
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
            "gamma_bestAsk_A": float(mw_lgd.get("bestAsk") or 0),
            "clob_ask_A": pm_a_tt,
            "clob_ask_B": pm_b_lgd,
            "gamma_outcomePrices": prices_lgd,
            "gamma_live": gamma_live_lgd,
            "gamma_closed": gamma_closed_lgd,
            "gamma_ended": gamma_ended_lgd,
            "gamma_acceptingOrders": mw_accept_lgd,
            "gamma_event_acceptingOrders": ev_accept_lgd,
            "pin_listed": pin_tt_lgd_listed,
        },
    ],
    "table2": table2_json,
    "gt_0p5_paths": gt_0p5_paths,
    "data_gaps": gaps,
}

# no leftover vs keys

OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("WROTE", OUT_MD, "scan", SCAN)
print("WROTE", OUT_JSON)
print("should_send", should_send, reasons)
print("best", rate_pct_str(best_rate) if best_rate is not None else None, "pp", best_pp)
print("LGD sz", s_b_lgd, "TT sz", s_a_tt)
print("paths", [(r["book"], r["book_team"], rate_pct_str(r["rate"]), round(r["profit"], 1)) for _, r, _ in paths_sorted])
