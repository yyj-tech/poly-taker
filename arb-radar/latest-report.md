套利雷达 Hourly Report
时间：2026-08-17 12:59 CST (UTC+8)
数据源与缺口：Polymarket Gamma + CLOB 实时报价抓到（TI 冠军盘 + 4 场 8/20 季后赛胜负/大小/让分，盘口深度可用）。Pinnacle 公开页 HTML 为空，但 guest.api.arcadia.pinnacle.com 联赛 5055「Dota 2 - The International」成功返回 4 场公开赛盘 + 限额；冠军期货 cutoff 2026-08-13 已关闭，不可成交。Predict.fun 冠军页打开但无买卖价（需登录），API 401/404，本轮不当作可执行盘。Oddsportal TI 页显示暂无 bookmaker 盘。未编造任何价格。

今日背景：TI15 上海，小组赛/淘汰赛已结束，8/17–8/19 休赛，主赛事 8/20 开打。四场上半区八强均已在两边上架。

🔥 高价值机会
无。
本轮没有任何「扣费后净收益 ≥ 1.5%」且可立即吃单的跨平台对冲。最接近的 taker 路径是「买 Polymarket TEAM VISION -1.5 图 @0.49 + 买 Pinnacle BoomBoys +1.5 @-102」，扣 Polymarket taker fee 后约 -0.74%。若在 PM 以 maker 挂 0.48 成交，理论约 +1.53%，但成交不保证，且 Pinnacle 限额把可执行本金压到约 585 USDT，规则也不一致——不升格为高价值。

🟡 潜在机会
价差在，但流动性/规则/费用有问题，不建议立刻执行。只供人工核对盘口是否继续偏移。

1) Nigma Galaxy vs Team Falcons（BO3）比赛胜负
- 事件：TI 上半区八强，开赛 2026-08-20 11:00 UTC / 19:00 CST。同一场、同一 BO3，匹配确定。
- 两边价格：
  - Polymarket 胜负：NGX mid 0.345，可买 NGX @0.35（ask 量约 3448 份），可买 Falcons @0.66（ask 量约 3409 份）。24h 量约 2.59 万，CLOB 流动性约 2.17 万。
  - Pinnacle 全场 ML（period 0）：NGX +149（十进制 2.49，隐含 40.16%），Falcons -185（1.541，隐含 64.91%），maxRiskStake 300 USD。Juice 约 5.1%。
- 理论套利（未计 PM 手续费）：买 PM NGX @0.35 + 买 PIN Falcons @1.541，合成成本 0.9991 / 每 1 USD 赔付，理论 +0.09%。
- 手续费后：PM sports taker fee = C×0.05×p×(1-p) → 每股约 0.0114，合成成本 1.0105，净收益约 -1.04%。投入 10000 USDT 无约束理论亏损约 104 USDT；受 PIN 300 限额约束，可执行本金约 467 USDT，预期约 -5 USDT。
- 建议资金：不要按 10000 去想。Pinnacle 300 封顶是硬约束。若只做人工观察，关注 PM NGX ask 是否掉到 ≤0.33 或 PIN Falcons 是否短于 -175。
- 风险星级：★★★★☆（规则不一致为主）
- 规则是否一致：50%。两边都是「这场 BO3 谁赢」。但原文冲突明显：
  - PM：「If the match is postponed, it must be rescheduled ... on or before September 3, 2026 at 11:59 PM ET ... Otherwise, this market resolves 50-50」；赛中对手弃权/DQ 判胜者；赛前 walkover「resolve to 50-50」。
  - PIN Esports：「If a Match isn't started 30 hours after its scheduled starting time, all bets on that Match will be deemed void。」General：「In any fixture involving a forfeit, walkover ... all bets will be voided。」Dota 2：前 10 分钟掉线/裁判判负则图 void，且「If a Map is voided due to retirement, disconnection, disqualification, walkover ... all bets on the Match-period will be deemed void。」
  - 延期 30 小时–14 天、赛前 walkover、技术重赛：一边 50-50、一边退本，对冲会裂开。
- 可执行 vs 理论：理论 +0.09% → 扣费后 -1.04% → 可执行同样为负（深度够，限额小）。不值得下单，只值得盯盘。

2) Team Liquid vs Team Yandex（BO3）比赛胜负
- 事件：TI 上半区八强，2026-08-20 08:00 UTC / 16:00 CST。匹配确定。
- 两边价格：
  - PM：Liquid mid 0.545，可买 Liquid @0.55（约 3967 份），可买 Yandex @0.46（约 3578 份）。量约 3.64 万。
  - PIN：Liquid -146（1.685，59.35%），Yandex +120（2.20，45.45%），限额 300。Juice 约 4.8%。
- 理论套利：买 PM Liquid @0.55 + 买 PIN Yandex @2.20，成本 1.0045，理论 -0.45%（尚未覆盖）。
- 手续费后：约 -1.66%。10000 USDT 无约束约亏 166；可执行本金约 467 USDT 量级。
- 建议资金：无。若 Liquid PM ask ≤0.52 且 PIN Yandex 仍 ≥2.20，再人工复算。
- 风险星级：★★★★☆
- 规则是否一致：50%（同上 30h void vs 14 天 50-50 / walkover 处理不同）。
- 可执行 vs 理论：理论已亏 → 扣费更亏。价差方向存在（PM 更看好 Liquid），但是 juice 盘，不是套利。

3) TEAM VISION -1.5 图 vs BoomBoys +1.5
- 事件：同一场 VISION vs BoomBoys 的地图让分，两边都是「VISION 净胜 ≥2 图（2-0）」。匹配较确定，但弃权计图规则可能分叉。
- 两边价格：
  - PM：VISION -1.5 mid 0.485，bid 0.48 / ask 0.49，量约 1.30 万，流动性约 1.23 万。
  - PIN spread home -1.5 -119（1.840，54.34%），away +1.5 -102（1.980，50.50%），限额 300。
- 理论套利（taker）：买 PM VISION @0.49 + 买 PIN BoomBoys +1.5 @1.980，成本 0.995，理论 +0.51%。
- 手续费后（taker）：约 -0.74%。
- 若 PM maker 在 0.48 挂单成交（maker fee 0）：约 +1.53%，可执行本金约 585 USDT（PIN 300 + PM ~285），理论利润约 9 USDT。这是本轮唯一触及 1.5% 的数字，但是条件收益。
- 建议资金：不建议立刻吃单。若有人坚持验证，也只是「小额、先确认 PIN 限额与账户、再看 PM 挂单是否真的被吃」，不是执行指令。
- 风险星级：★★★★★（让分 + 弃权计图 + 成交不确定）
- 规则是否一致：45%。PM 原文：「Games won by forfeit, disqualification, walkover, or default are counted towards the handicap, provided that the match is completed。」PIN：赛前 walkover 全场 void；图在前 10 分钟裁判判负则图 void，并可能拖垮 Match-period。2-0 因 walkover 出现时，一边可能算让分打出，一边退本。
- 可执行 vs 理论：taker 理论 +0.51% → 扣费 -0.74%；maker 条件 +1.53% 但不可立即成交。

4) TEAM VISION vs BoomBoys 胜负（价差方向，不是套利）
- PM VISION 0.795（可买 0.80，ask 量 1.56 万份，深度足够）；PIN VISION -461（隐含 82.17%）/ BoomBoys +317（24.00%）。
- PM 比 PIN 更不看好 VISION（79.5% vs 82.2%）。对冲成本 taker 约 -3.9% 到 -4.6%。无套利，只说明两市对热门队定价差约 3 个百分点。
- 风险星级：★★★☆☆（定价差可观察，规则风险同 1）
- 不建议执行。

❌ 排除
发现 15 条路径被排除，汇总原因：

规则不同（4）
- 四场比赛胜负/让分/大小在「延期窗口、walkover、前 10 分钟掉线」上，PM 50-50 或按完成结果计，PIN void。即使价格偶发打平，对冲也不是无风险。
- TI 冠军盘：PM 仍交易（VISION 39.5%、Spirit 12%、Liquid 10.5% 等）；PIN 期货已于 2026-08-13 05:00 UTC cutoff 关闭，盘面还挂着小组赛前的 PVISION +200 / Yandex +300 等过期价，不可成交。若强行对照，队名还需映射（见下方「拿不准」）。

流动性不足 / 限额吃掉规模（4）
- Pinnacle 本轮 Dota 公开盘 maxRiskStake 仅 150–300 USD。即便出现 2% 价差，可吃金额也只有数百 USDT，10000 USDT 的理论收益表没有意义。
- PM 冠军盘 1w Team（=Iron Wing）ask 仅约 45 份；Liquid YES ask 仅约 303 份。冠军盘即使 PIN 重开，深度也不对称。
- 大量 PM 趣味盘（白天/黑夜结束、双队打肉山、Ultra Kill、Rampage）买卖价差 40–90 美分，近乎空盘，且 PIN 无对应盘。

费用吃掉（5）
- Iron Wing vs Spirit 两边都是 -110 vs PM 0.48/0.52，taker 后约 -2.6% / -5.3%。
- VISION vs BoomBoys 胜负 taker 后约 -3.9% / -4.6%。
- 四场 O/U 2.5：PIN juice 约 5–7%，PM 再收 sports taker，合成 -2.7% 到 -7%。Nigma O/U 买 PM Over@0.46 + PIN Under@-125 是 totals 里最好的，仍约 -2.7%。
- Game 1/2 单图：PIN 限额 150，PM 价差更宽（Liquid G1 bid/ask 0.52/0.57），对冲更差。

未匹配上（2+）
- Predict.fun「The International 2026: Winner」有同事件页面（成交额约 6153），但本轮拿不到 YES/NO 可成交价，不能配。
- PM 冠军趣味盘（最 Ban 英雄、Radiant/Dire 胜率、英雄池深浅、新英雄公布）在 Pinnacle 无对应。
- 历史/已结束的 DreamLeague、BLAST、Streamers Battle 等 PM 事件未与 PIN 对齐，本轮不配。

今日结论
跨市场价差存在，但还不是可执行套利。Pinnacle 把四场八强打得很「尖」（2 向 juice 约 5%），Polymarket 在 NGX/Falcons 和 Liquid/Yandex 上略偏主队，扣 sports taker fee 后全部翻负。冠军盘目前是单边市场：只有 Polymarket 能交易，Pinnacle 期货已关。今天是休赛日，盘口不会被比赛结果冲击，更可能被资金和限额微调。

下一步该等什么盘口变化
- 8/20 开赛前 6–12 小时：看 Pinnacle 是否提高限额（300→1000+）或重开冠军盘；限额不上来，再好的价差也只能做几百刀。
- Nigma/Falcons：PM NGX ask ≤0.33 且 PIN Falcons 仍约 -185，taker 才可能转正；同时必须接受 30h void vs 14 天 50-50 的规则裂口。
- VISION -1.5：只有 maker 成交 + PIN +1.5 不缩短时才接近 1.5%，且让分规则更脏，优先当观察项。
- 队名映射已确认但期货未开：VISION=PARIVISION，Iron Wing=1w/1win（中国站禁博彩赞助临时名），BoomBoys=BetBoom。PIN 若重开冠军盘，先核队名再核价。
- Predict.fun 若之后给出可成交买卖价，再把它当第三腿，本轮忽略。

本报告只做定价差分析，不下单、不自动交易。上面「潜在」条目的含义是：是否值得人工再看一眼盘口和规则，不是「去买」。

---

实际请求过的 URL 和是否成功

成功
- https://gamma-api.polymarket.com/public-search?q=Dota&limit_per_type=50&events_status=active （200，TI 比赛事件）
- https://gamma-api.polymarket.com/public-search?q=The+International&limit_per_type=50&events_status=active （200，冠军盘）
- https://gamma-api.polymarket.com/public-search?q=TI+2026&limit_per_type=50&events_status=active （200，新英雄盘）
- https://gamma-api.polymarket.com/public-search?q=esports&limit_per_type=50&events_status=active （200，但主结果是 LoL，Dota 被挤掉）
- https://gamma-api.polymarket.com/public-search?q=Iron+Wing&limit_per_type=10&events_status=active （200）
- https://gamma-api.polymarket.com/events?tag_slug=dota-2&active=true&closed=false&limit=100 （200，37 个事件）
- https://gamma-api.polymarket.com/events?tag_slug=the-international&active=true&closed=false&limit=50 （200）
- https://gamma-api.polymarket.com/events?slug=dota2-ironwi-ts8-2026-08-19 （200）
- https://gamma-api.polymarket.com/events?slug=dota2-vsn2-boombo-2026-08-20 （200）
- https://gamma-api.polymarket.com/events?slug=dota2-liquid-ty-2026-08-20 （200）
- https://gamma-api.polymarket.com/events?slug=dota2-ngx-flc-2026-08-20 （200）
- https://gamma-api.polymarket.com/events?slug=the-international-2026-winner-20260629212545745 （200）
- https://gamma-api.polymarket.com/events?slug=the-international-2026-winning-region-20260805215811238 （200）
- https://clob.polymarket.com/book?token_id=... （四场胜负 + 未关闭冠军 outcome 200；已结算队 404）
- https://guest.api.arcadia.pinnacle.com/0.1/sports （200，E Sports id=12）
- https://guest.api.arcadia.pinnacle.com/0.1/sports/12/leagues?all=false （200，联赛 5055 Dota 2 - The International，matchupCount=2→抓取时实际 4 场公开赛）
- https://guest.api.arcadia.pinnacle.com/0.1/leagues/5055/matchups （200，9 条含 special）
- https://guest.api.arcadia.pinnacle.com/0.1/leagues/5055/markets/straight （200，29 条盘，含限额与美式赔率）
- https://www.pinnacle.com/en/future/betting-rules （200，Esports / Dota 2 / General void 原文）
- https://www.pinnacle.com/config/app.json （200）
- https://predict.fun/market/the-international-2026-winner-20260629165629925 （页面 200，无报价）
- https://help.polymarket.com/en/articles/13364478-trading-fees （200，sports feeRate 0.05）
- https://docs.polymarket.com/trading/fees （检索到，公式一致）

失败 / 空
- https://www.pinnacle.com/en/esports/dota-2/matchups/ （404）
- https://www.pinnacle.com/en/esports/dota-2/ （404）
- https://www.pinnacle.com/en/esports/games/dota-2/matchups/ （200 但 HTML 无赔率，前端渲染）
- https://www.pinnacle.com/en/esports/matchups/ （200 空正文）
- https://www.pinnacle.com/en/betting-rules/esports （404）
- https://api.pinnacle.com/v3/sports （451 Unavailable For Legal Reasons）
- https://guest.api.arcadia.pinnacle.com/0.1/leagues/5055/markets/special （401）
- https://api.the-odds-api.com/v4/sports/ （401，无 key，未使用）
- https://www.oddsportal.com/esports/dota-2/the-international/ （200，「Next Matches will appear here...」无赔率）
- https://paripulse.com/en/line/esports/1051333-dota-2-the-international/360716760-team-vision-bb-team （200，赛程在，赔率未渲染）
- https://api.predict.fun/v1/markets?search=International （401）
- https://api.predict.fun/markets?q=The%20International （404）
- https://predict.fun/api/markets/the-international-2026-winner-20260629165629925 （404）

匹配逻辑里拿不准的事件
- 已确认、本轮按同一队处理：TEAM VISION = PARIVISION = Pinnacle「VISION / PVISION」；Iron Wing = 1w Team / 1win（中国站禁博彩赞助临时名）；BoomBoys = BetBoom / BB Team；HULIGANI = L1GA（已淘汰）。
- 拿不准 / 未硬配：Pinnacle 已关闭的冠军期货仍列出 Aurora、Vici、OG 等已淘汰队，价格是 8/13 前的，不能当现价。PM 冠军盘没有「Iron Wing」这个字符串，只有「1w Team」——按公开报道视为同一支，但若结算源只认队名不认组织，存在 residual 风险，故冠军盘即使 PIN 重开也要先读两边 settlement 原文。
- Predict.fun 冠军盘 16 个 outcome 与 PM 同构，但无报价，列入未匹配。
- PM「Winning Region」EE/CIS 77.5% vs 西欧 23.5%，PIN 无地区冠军盘，不配。
- 单图 G1/G2 与 PIN period 1/2 结构相近，但 PM 部分盘买卖价差 4–7 分，本轮不当作干净匹配去报套利。

手续费假设（2026-08 查到的现状，用于扣费，不是下单建议）
- Polymarket：电竞/体育类 feeType=sports_fees_v2，takerOnly，rate=0.05，rebateRate=0.15。公式 fee = C × 0.05 × p × (1-p)，maker 为 0。50¢ 附近 100 份最高约 1.25 USDC。本轮全部按 taker 即时吃单计；maker 路径单独标注。平台充提 USDC 无平台费，Polygon gas 忽略（<0.05）。未计入 taker rebate（不确定账户等级）。
- Pinnacle：体育注无佣金，成本是 juice（本轮 2 向约 4.8–6.2%）。限额取接口 limits.amount maxRiskStake（胜负 300，单图/大小 150，期货 100）。提现：平台本身不另抽成下注，但法币/钱包通道常见 0–2%；本轮净收益未再扣提现，若计入 0.5% 则所有路径更差。
- 资金占用：两边都要预留保证金，不能把 10000 当成单边。PIN 300 封顶时，PM 对冲腿通常 160–300，总占用约 450–600 USDT。
- 高价值阈值：扣上述 PM taker + PIN juice（已含在赔率里）后净收益 ≥1.5%。本轮 taker 无一达标。

落盘文件
- /workspace/arb-radar/markets.jsonl
- /workspace/arb-radar/opportunities.jsonl
- /workspace/arb-radar/history.jsonl
- /workspace/arb-radar/latest-report.md
