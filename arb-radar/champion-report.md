# TI15 冠军盘对照（仅冠军，不含八强胜负）

快照：2026-08-17 13:07 CST（Asia/Shanghai）  
范围：The International 2026 / TI15 Winner  
原则：只写本次实际请求到的数字；过期价不标现价；不下单建议。  
高价值阈值：扣费后净 ≥1.5%。Polymarket 电竞 taker fee = C×0.05×p×(1-p)，maker=0。

## 表1 概览

| 平台 | 盘口 | 状态 | 能否成交 | 更新时间（CST） | 缺口 |
|---|---|---|---|---|---|
| Polymarket | Winner `the-international-2026-winner-20260629212545745` | 开盘（8 队未关闭 / 8 队已结算 NO） | 能 | 2026-08-17 13:02 | 无。CLOB 8 支未关闭队均有 YES bid/ask。事件流动性 $213,531，24h 量 $135,189，总量 $1,485,211 |
| Polymarket | Winning Region `the-international-2026-winning-region-20260805215811238` | 开盘（仅 EE/CIS、西欧） | 能 | 2026-08-17 13:00 | 中/SEA/NA/SA 已结算 NO。PIN 无地区冠军盘 |
| Pinnacle | 联赛 5055「Dota 2 - The International」Futures / The International Winner / Place 1st（matchup 1633296958） | 已关闭 | **不可成交** | 2026-08-17 13:05 复核 | sports/12/leagues?all=false 共 11 条活跃联赛，名称含 International / Dota outright / futures 的只有 5055。冠军期货 period status=`closed`，cutoff **2026-08-13 13:00 CST**（2026-08-13T05:00:00Z）。接口仍回 8/13 前美式价，**不当现价**。无重开联赛 |
| Predict.fun | Winner `the-international-2026-winner-20260629165629925` | 页面在线 | **无报价** | 2026-08-17 13:05 | 生产 API 401；页面买卖栏 Yes- / No-；历史总成交 $6,153。JSON-LD 残留价含已淘汰队，不当现价 |
| Stake / Kalshi / 其他 | TI winner | 未拿到公开现价 | 否 | 2026-08-17 13:05 | Stake Cloudflare 403；Kalshi `KXDOTA` 空。不硬凑新闻旧赔率 |

## 表2 Polymarket 冠军盘（未关闭，CLOB 实盘）

事件截止/Other 条款：若 2026-09-06 23:59 ET（**2026-09-07 11:59 CST**）仍无冠军 → Other。结算源 Dotabuff。

| 队伍 | YES mid | bid | ask | ask 量（份） | 隐含概率（mid） | 24h 成交量 $ | 流动性 $ | 最近成交 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TEAM VISION | 0.400 | 0.39 | 0.41 | 370.62 | 40.00% | 5,904.95 | 21,379.55 | 0.41 |
| Team Spirit | 0.120 | 0.11 | 0.13 | 564.81 | 12.00% | 4,661.48 | 24,809.16 | 0.12 |
| Team Liquid | 0.105 | 0.09 | 0.12 | 303.08 | 10.50% | 2,864.65 | 21,612.35 | 0.12 |
| Team Yandex | 0.0965 | 0.091 | 0.102 | 118.00 | 9.65% | 7,569.38 | 28,265.61 | 0.103 |
| Team Falcons | 0.095 | 0.09 | 0.10 | 595.91 | 9.50% | 2,450.91 | 23,896.13 | 0.10 |
| Nigma Galaxy | 0.0775 | 0.068 | 0.087 | 258.30 | 7.75% | 25,973.18 | 25,619.50 | 0.087 |
| 1w Team | 0.0765 | 0.074 | 0.079 | 45.43 | 7.65% | 16,901.98 | 30,683.91 | 0.09 |
| BoomBoys | 0.075 | 0.07 | 0.08 | 25.00 | 7.50% | 6,524.91 | 38,510.24 | 0.08 |

8 队 mid 合计 1.0455（买卖价差造成超 100%）。8 队 YES ask 合计 1.108。深度最薄：BoomBoys ask 25 份、1w Team ask 45.43 份。

### 附表  Winning Region（小表）

| 赛区 | 状态 | YES mid | bid / ask | ask 量 | 隐含概率 | 24h 量 $ | 流动性 $ |
|---|---|---:|---|---:|---:|---:|---:|
| Eastern Europe & CIS | 可成交 | 0.775 | 0.77 / 0.78 | 540 | 77.5% | 785.10 | 1,397.99 |
| Western Europe | 可成交 | 0.235 | 0.23 / 0.24 | 375 | 23.5% | 458.76 | 1,132.55 |
| China / SEA / NA / SA | 已结算 NO | — | — | — | 0 | — | — |

地区盘 mid 合计 1.010。结算源 Liquipedia Teams Portal；取消或 9/6 ET 无冠军 → Other。

## 表3 跨平台对照（能对上的队）

队名映射（已确认）：TEAM VISION = PARIVISION = PVISION；1w Team = Iron Wing = 1win / PIN「1W」；BoomBoys = BetBoom = BB Team。  
PIN 列只写「不可成交」，**不填 8/13 过期价**。

| 队伍 | PM YES mid (bid/ask) | PIN 赔率 / 隐含概率 | Predict.fun | 价差 | 能否对冲 | 规则风险 |
|---|---|---|---|---|---|---|
| TEAM VISION / PVISION | 0.400（0.39/0.41） | 不可成交（cutoff 2026-08-13 13:00 CST） | 无报价（页面对应 TEAM VISION，历史量 $1,164） | 无法计算 | 否 | PIN 无腿。若重开：取消时 PM→Other、PIN 可能 void；队名 PVISION vs TEAM VISION 已映射 |
| Team Spirit / Spirit | 0.120（0.11/0.13） | 不可成交 | 无报价（历史量 $276.52） | 无法计算 | 否 | 同上 |
| Team Liquid / Liquid | 0.105（0.09/0.12） | 不可成交 | 无报价（历史量 $533.31） | 无法计算 | 否 | 同上 |
| Team Yandex / Yandex | 0.0965（0.091/0.102） | 不可成交 | 无报价（历史量 $1,779） | 无法计算 | 否 | 同上 |
| Team Falcons / Falcons | 0.095（0.09/0.10） | 不可成交 | 无报价（历史量 $786.76） | 无法计算 | 否 | 同上 |
| Nigma Galaxy | 0.0775（0.068/0.087） | 不可成交 | 无报价（历史量 $0） | 无法计算 | 否 | 同上 |
| 1w Team / Iron Wing / 1W | 0.0765（0.074/0.079） | 不可成交 | 无报价（页面对应 Iron Wing，历史量 $0） | 无法计算 | 否 | 映射已确认，但结算源若只认字符串仍有残差 |
| BoomBoys / BB Team | 0.075（0.07/0.08） | 不可成交 | 无报价（历史量 $1,609） | 无法计算 | 否 | 映射已确认 |

扣费后净 ≥1.5% 的跨平台路径：**0 条**（缺少第二腿可成交价）。

## 表4 未匹配 / 已关闭 / 无报价

| 对象 | 平台 | 状态 | 说明 |
|---|---|---|---|
| Aurora Gaming | Polymarket | 已关闭，结算 NO | closedTime 2026-08-16 08:48 UTC；总量 $62,358 |
| Xtreme Gaming | Polymarket | 已关闭，结算 NO | closedTime 2026-08-15 15:08 UTC；总量 $82,521 |
| HULIGANI | Polymarket | 已关闭，结算 NO | closedTime 2026-08-15 15:06 UTC；总量 $122,499。对应 PIN L1GA |
| Team Resilience | Polymarket | 已关闭，结算 NO | closedTime 2026-08-16 10:53 UTC；总量 $111,045 |
| Vici Gaming | Polymarket | 已关闭，结算 NO | closedTime 2026-08-16 08:48 UTC；总量 $83,959 |
| OG | Polymarket | 已关闭，结算 NO | closedTime 2026-08-15 15:07 UTC；总量 $55,480 |
| GamerLegion | Polymarket | 已关闭，结算 NO | closedTime 2026-08-16 10:52 UTC；总量 $93,458 |
| LGD Gaming | Polymarket | 已关闭，结算 NO | closedTime 2026-08-16 15:26 UTC；总量 $79,601 |
| A / B / C / Other | Polymarket | 未激活占位 | 无量、无盘，Other 仅在 9/6 ET 仍无冠军时启用 |
| Pinnacle 冠军期货 16 队 | Pinnacle | 已关闭 | 名单：PVISION, Aurora, 1W, Nigma Galaxy, GamerLegion, L1GA, BB Team, Falcons, Liquid, Vici, Resilience, Yandex, Spirit, Xtreme, LGD, OG。cutoff 2026-08-13 13:00 CST。**过期美式价仍在 straight 接口，不当现价** |
| Predict.fun 16 outcome | Predict.fun | 有页面、无买卖价 | 总成交 $6,153。JSON-LD 残留：VISION 0.42 / Aurora 0.20 / Liquid 0.12 / Spirit 0.12 / Yandex 0.10 / Resilience 0.10 / Falcons 0.08 / BoomBoys 0.08——含已淘汰队，**不当现价** |
| Stake TI outright | Stake | 无公开现价 | GraphQL/页面 403 Cloudflare。8/11 新闻赔率不采用 |
| Kalshi Dota | Kalshi | 无盘 | `series_ticker=KXDOTA` 返回 events=[] |

## 表5 规则对照

| 平台 | 延期 | 取消 / 无冠军 | walkover | 结算源 |
|---|---|---|---|---|
| Polymarket Winner | 赛程原文 Aug 13–23, 2026；未写「延期仍算」。超过 2026-09-06 23:59 ET 仍无冠军 → Other | 取消或逾期无冠军 → Other（不是 void） | 冠军盘原文未写 walkover；并列按盘上队名字母序 | Dotabuff 官方；也可可信报道共识 |
| Polymarket Winning Region | 同上逾期窗口 | 取消或 9/6 ET 无冠军 → Other | 按夺冠队在 Liquipedia Teams Portal 的赛区 | Liquipedia Dota 2 Teams Portal |
| Pinnacle Futures（当前不可成交） | Esports「To Win Final」：阶段完成即有 action，改期/延期仍算 | 无官方冠军时，General 倾向 void（未完成 fixture）；与 PM Other 不一致 | General #10：未开打 forfeit/walkover 整场 void。Dota 2：前 10 分钟 walkover 该图 void，并可能 void Match-period。冠军期货更接近「官方第1名」 | 赛事主管机构完成日最终裁定（General #5）。规则页 https://www.pinnacle.com/en/future/betting-rules |
| Predict.fun Winner | 页面规则与 PM 同构（并列字母序、9/6 ET → Other） | 同 PM：逾期 → Other | 原文未写 walkover | 同 PM：Dotabuff / 可信报道共识。页面另写 Ends Aug 24 @ 5:55AM（时区未标注） |

## 表6 结论

| 项 | 内容 |
|---|---|
| 有没有跨平台冠军盘套利 | **没有** |
| 为什么 | 今天能成交的冠军盘只有 Polymarket 一侧。Pinnacle 期货 cutoff 2026-08-13 13:00 CST 已关，没有重开的 outright/futures 联赛；Predict.fun 无买卖价；Stake/Kalshi 没有公开现价。单边无法对冲，扣费后净 ≥1.5% 的路径为 0。PM 8 队 ask 合计 1.108，也不是内部锁定。 |
| 不要做什么 | 不要把 PIN 接口里还挂着的 +200 / +300 等 8/13 前价格当现价。不要把 Predict.fun JSON-LD 当盘口。本次不扫八强胜负。 |
| 下一步盯什么 | 1）Pinnacle `sports/12/leagues` 是否出现新的 Dota outright/futures，或 matchup 1633296958 period 是否从 closed 重开；2）Predict.fun 页面/API 是否出现真实 bid/ask；3）8/20 开赛前后 PM VISION YES 与其余 7 队 ask 深度（1w / BoomBoys 很薄）。 |

本表只做定价差记录，不是下单建议。

---

## 本次请求成功 / 失败

**成功**
- https://gamma-api.polymarket.com/events?slug=the-international-2026-winner-20260629212545745 （200）
- https://gamma-api.polymarket.com/events?slug=the-international-2026-winning-region-20260805215811238 （200）
- https://gamma-api.polymarket.com/public-search?q=The%20International%202026%20winner （200）
- https://gamma-api.polymarket.com/public-search?q=The%20International%20winner&limit_per_type=30&events_status=active （200，TI winner 仅此一条）
- https://gamma-api.polymarket.com/events?slug_contains=the-international-2026 （200）
- https://clob.polymarket.com/book?token_id=… （8 支未关闭冠军 YES + 2 个未关闭地区 YES，全部 200）
- https://guest.api.arcadia.pinnacle.com/0.1/sports （200，E Sports id=12）
- https://guest.api.arcadia.pinnacle.com/0.1/sports/12/leagues?all=false （200，11 联赛，Dota 仅 5055）
- https://guest.api.arcadia.pinnacle.com/0.1/sports/12/matchups （200，含期货 1633296958，period closed）
- https://guest.api.arcadia.pinnacle.com/0.1/leagues/5055/matchups （200）
- https://guest.api.arcadia.pinnacle.com/0.1/leagues/5055/markets/straight （200，期货过期价仍在）
- https://guest.api.arcadia.pinnacle.com/0.1/matchups/1633296958/markets/straight （200）
- https://www.pinnacle.com/en/future/betting-rules （200）
- https://predict.fun/market/the-international-2026-winner-20260629165629925 （200，无买卖价）
- https://api.predict.fun/v1/categories （200，无报价）
- https://dev.predict.fun （200，文档：生产 API 需 Discord key）
- https://api-testnet.predict.fun/v1/markets?search=International （200，测试网无 TI 2026）
- https://api.elections.kalshi.com/trade-api/v2/events?series_ticker=KXDOTA&limit=5 （200，events=[]）

**失败 / 空**
- https://guest.api.arcadia.pinnacle.com/0.1/sports/12/leagues?all=true （401）
- https://guest.api.arcadia.pinnacle.com/0.1/matchups/1633296958 （401；已被 sports/12/matchups 覆盖）
- https://api.predict.fun/v1/markets （401）
- https://api.predict.fun/v1/markets?search=International （401）
- https://api.predict.fun/v1/markets/the-international-2026-winner-20260629165629925 （401）
- https://api.predict.fun/markets?q=The%20International （404）
- https://predict.fun/api/markets/the-international-2026-winner-20260629165629925 （404）
- https://api.predict.fun/v1/events?slug=the-international-2026-winner-20260629165629925 （404）
- https://gamma-api.predict.fun/events?slug=… （DNS 不存在）
- https://stake.com/_api/graphql （403 Cloudflare）
- https://stake.com/sports/esports/dota-2 （403）
- https://api.stake.com/sports/dota-2 （404）
- https://api.kalshi.com/trade-api/v2/events （DNS 不存在）

落盘：`/workspace/arb-radar/champion-markets.json` ；`/workspace/arb-radar/champion-report.md`
