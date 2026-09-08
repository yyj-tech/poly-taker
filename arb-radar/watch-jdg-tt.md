# JDG/TT 盯盘 2026-08-23 17:33 CST

只分析，未下注。数据：PM Gamma + CLOB 档1最佳 ask（不累加）；Stake/Duel 经 odds-api.io 本轮无密钥（ODDS_API_IO_KEY / apis/.odds_api_io_key / scans/.odds_api_io_key 均缺失，未 glob /home/box），非429，无†，表1 Stake/Duel 写—（结束盘不沿用16:38滚球陈价）。PIN guest 199353 related/straight 404，已回退 /leagues/199353/markets/straight；JDG/TT PIN period-0 仍撤；TT vs LGD 父盘 1634146968 本轮已从 matchups 消失，period-0 系列 ML 仍无，PIN 套现跳过。档1只吃最佳 ask。单档>2000份标「档1异常厚」。高价值 = 费后≥1.5% 且规则一致。两场均已结束，不硬算套现。parent 应删 routine（本脚本不删）。

scan_cst：2026-08-23 17:33 CST（Asia/Shanghai）
是否滚球：否。两场均已结束。JDG vs TT 已结束（8/20 17:00 CST 开赛，赛后约 4354 分钟；PM live=False、closed=True、ended=True、accepting=False（market；event accepting=None）、score 000-000|2-1|Bo3；odds-api.io 本轮 NO_KEY，JDG/TT 未请求；PIN 父盘 1633881950 absent_from_list，period-0 系列 ML 已撤；PIN 子盘 1634353344 absent。TT vs LGD **已结束、非滚球**：PM live=False、closed=False、ended=True、accepting=True（market；event accepting=None）、score 000-000|0-2|Bo3；OAI NO_KEY；PIN 父盘 1634146968 ABSENT from matchups（上轮 listed status=started），period-0 系列 ML 仍撤；PIN 滚球子盘 1634593525 本轮 absent（上轮 isLive=True 地图盘）。开赛 15:00 CST，本扫描约 154 分钟后。
是否结束：JDG vs TT 已结束（PM live=False closed=True ended=True score 000-000|2-1|Bo3，Bo3 2-1 JDG 胜；不要硬算套现）。TT vs LGD **已结束** score 000-000|0-2|Bo3（系列 0-2，LGD 2-0 胜；上轮 0-1 滚球 → 本轮结束）。两场均结束，parent 应删 routine（本脚本不删）。

## 表1 价格对照

| 状态 | 事件 | 队A | 队B | PM_A | PM_B | PIN_A | PIN_B | Stake_A | Stake_B | Duel_A | Duel_B |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 结束 | JDG vs TT | JDG | TT | — | — | — | — | — | — | — | — |
| 结束 | TT vs LGD | TT | LGD | 0.001 | — | — | — | — | — | — | — |

PM 档1深度：JDG vs TT 已结束，不吃套现档。CLOB 双边 404（No orderbook exists for the requested token id；Gamma outcomePrices ['1', '0'] bestAsk 1 bestBid 0.999 uma=resolved）。昨日 leftover 盘口已撤，不当套现。 TT vs LGD **已结束** leftover CLOB TT 806589.3份 @0.001 / LGD —份 @—（档1异常厚，结束盘 leftover，不套现）。Gamma bestAsk 0.001 vs CLOB L1 0.001（一致，本轮结束不套现）；outcomePrices ['0.0005', '0.9995']。LGD CLOB NO_ASKS（赢家侧无卖盘）。
Stake/Duel 本轮 odds-api.io **NO_KEY**（非429，无†）。JDG vs TT 已结束，表1 Stake/Duel 写—（不沿用陈价）。TT vs LGD 已结束，表1 Stake/Duel 写—（不沿用 16:38 滚球 7.5/1.08 与 8.5/1.09）。PIN JDG/TT 系列 period-0 ML 已撤（父盘 1633881950 不在 matchups；子盘 1634353344 不在 matchups 与 /markets/straight；related/straight 404，已回退 /markets/straight）。PIN TT vs LGD 父盘 1634146968 本轮 ABSENT（上轮 listed started / period-0 已撤）；滚球子盘 1634593525 本轮 ABSENT。表1 PIN 写—，不硬算 PIN 套现。

## 表2 套现仓位

| 状态 | 事件 | 左买 | 右买 | 成本 | 手续费 | 利率 | 多久结算 | 一单利润 |
|---|---|---|---|---:|---:|---:|---|---:|
| 结束 | JDG vs TT | — | — | — | — | — | 已结束，不硬算套现 | — |
| 结束 | TT vs LGD | — | — | — | — | — | 已结束，不硬算套现 | — |

## 费后>0.5%（本轮要标出，完整仓位）

无。JDG vs TT 已结束不硬算（已报结束，本轮仍结束）。TT vs LGD 已结束不硬算（上轮滚球 0-1 → 本轮结束 0-2；不沿用陈价路径、不升格）。

高价值（费后≥1.5%、规则一致）：没有（两场均已结束，不硬算、不升格）。

## 相对 16:38 CST

- JDG vs TT：PM 结束→结束（Gamma 1/0 不变；CLOB 404 双边无盘）；Stake —→—（NO_KEY，结束盘已撤）；Duel —→—；PIN —→—。最佳利率 结束→结束（不硬算）。未把陈价路径当翻正/翻负。JDG 档1 无→无；TT CLOB 404→CLOB 404 (unused)。状态 结束→结束。score 000-000|2-1|Bo3→000-000|2-1|Bo3。closed True→True；market accepting False→False；uma resolved。PIN 父盘仍 absent；子盘 1634353344 仍 absent。
- TT vs LGD：PM 0.1/0.91→0.001/—（CLOB leftover TT @0.001 档1异常厚 806589.4份；LGD NO_ASKS）；Stake 7.5/1.08→—（NO_KEY，结束盘不沿用陈价）；Duel 8.5/1.09→—（NO_KEY，结束盘不沿用陈价）；PIN —→—（period-0 仍撤；父盘 listed→ABSENT）。最佳利率 −1.76%（Duel买LGD）→结束（不硬算）。TT 档1 55.0@0.1→806589.4份 @0.001（档1异常厚，leftover 不套现）；LGD 档1 409.0@0.91→无ask。未把结束盘 leftover 当翻正/翻负。买TT侧：Duel 买LGD −1.76%→结束；Stake 买LGD −2.57%→结束；PIN 买LGD —→—。买LGD侧：Duel 买TT −3.04%→结束；Stake 买TT −4.49%→结束；PIN 买TT —→—。状态 滚球→结束。比分 000-000|0-1|Bo3→000-000|0-2|Bo3。
- 是否 ≥1.5%：否（已结束不硬算）。
- 是否滚球/结束：JDG vs TT 已结束、非滚球（PM live=False closed=True ended=True accepting=False score=000-000|2-1|Bo3；PIN isLive父=False status=absent_from_list period-0=withdrawn；子盘 1634353344 absent）。TT vs LGD **已结束、非滚球**（PM live=False closed=False ended=True score=000-000|0-2|Bo3；OAI NO_KEY；PIN 父盘 1634146968 ABSENT period-0=withdrawn；子盘 1634593525 ABSENT）。
- should_send：YES（TT vs LGD结束；比分系列变化 000-000|0-1|Bo3→000-000|0-2|Bo3；PM ask≥0.02）。

数据缺口：PIN LPL 199353 本轮 2 场父对阵：JD Gaming/ThunderTalk 1633881950 ABSENT from matchups list (child 1634353344 also ABSENT; 17:00 CST 8/20 / 09:00Z)；ThunderTalk/LGD 1634146968 ABSENT this round (was listed 16:38 status=started isLive=False, period-0 withdrawn)；EDward Gaming/JD Gaming 1634147466 2026-08-23 17:30 CST / 2026-08-23T09:30:00Z pending isLive=False；Bilibili/Anyone's Legend 1634147502 2026-08-23 19:00 CST / 2026-08-23T11:00:00Z pending isLive=False。no live children。TT vs LGD 父盘子盘均不在列表；period-0 系列 ML 仍无。related/straight 本轮 404，已用 /leagues/199353/markets/straight 回退（200）。 odds-api.io NO_KEY this round (not 429); env ODDS_API_IO_KEY/OAI_API_KEY empty; apis/.odds_api_io_key and scans/.odds_api_io_key missing; did not glob /home/box. JDG/TT 7291391184 not requested; TT/LGD 5958057944 not pulled. Stake/Duel table1 = — (ended, no stale reuse). TT vs LGD Stake/Duel not refreshed (NO_KEY); last 16:38 was Stake 7.5/1.08 Duel 8.5/1.09 live — not reused. Gamma JDG vs TT bestAsk 1 vs CLOB L1 404 (不一致); outcomePrices ['1', '0']; ended, leftover gone Gamma TT vs LGD bestAsk 0.001 vs CLOB L1 0.001 (一致); outcomePrices ['0.0005', '0.9995']; live=False closed=False ended=True score=000-000|0-2|Bo3; LGD CLOB NO_ASKS; TT leftover 806589.3@0.001 档1异常厚 unused JDG vs TT JDG L1 none→none; TT leftover CLOB 404→CLOB 404 unused TT vs LGD TT L1 55.0@0.1→806589.3@0.001; LGD L1 409.0@0.91→NO_ASKS BOTH matches ended; parent should delete routine (this scan does not delete).

本表只做定价差记录，不是下单建议。
