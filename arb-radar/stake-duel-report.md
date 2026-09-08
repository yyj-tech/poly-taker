# Stake + Duel TI 冠军盘 / API 实测

时间：2026-08-17 13:12 CST（UTC+8）。数字只来自本轮真实请求。未下单、未用用户账号、未编价格。

队名映射（沿用已确认）：TEAM VISION = PARIVISION = PVISION；Iron Wing = 1w Team = 1win；BoomBoys = BetBoom = BB Team。

---

## 表1 API 状态

| 平台 | 端点 | 鉴权 | 本次是否打通 | 拿到什么 | 失败原因 |
|---|---|---|---|---|---|
| Stake 主站 | POST https://stake.com/_api/graphql | 公开盘不需要 token | 否 | 无 | Cloudflare 403 Just a moment。curl_cffi chrome131、headless Chrome dump-dom 同样拦 |
| Stake mirror | POST https://stake.bet/_api/graphql 以及 stake.ac / stake.pet / stake.games / stake1001.com / stake1021.com / stake1022.com / staketr.com / stake.mba / stake.ceo / stake.bz | 无 token | 否 | 无 | 同上 CF 403 |
| Stake 错误 host | POST https://api.stake.com/graphql | — | 否 | 无 | 404 Cannot POST /graphql |
| Stake.us | POST https://stake.us/_api/graphql | 无 token 即可握手 | **部分** | GraphQL schema、公开 feed 空数组、query 名/参数 | 体育树 `slugSport`/`sportList`/`sportFixtureQuery` 回 `serviceDisabled`（Connection lost, re-establishing...）。`allSports` 要登录 |
| Duel 站点 | GET https://duel.com 及 /sports /sportsbook /match-betting | 无 | 壳打通 | Vue SPA + `/assets/index-BQIzxYso.js` + `sports-fT7y-JGf.js` | 页面无赔率（iframe 未起来） |
| Duel 元数据 | GET https://duel.com/api/v2/metadata | 无 | **是** | service=duel，域名列表，tos_version=1-20260127 | 随后曾 429 |
| Duel 体育 | GET https://duel.com/api/v2/match-betting | 无 | 端点在、产品关 | 403 JSON：`Match betting is temporarily disabled while we work on some updates.` | 产品关闭 |
| Duel Betby session | POST https://duel.com/api/v2/match-betting/betby/user-session/en/USD/false | 游客空 body；登录才带 security_token | 否 | 无 JWT / libraryUrl | 403 HTML「IP or Country blocked」（本机出口 US） |
| Duel 代理 | GET https://sports-proxy.duel.com/ | Betby JWT | 否 | 无 | 403 `{"error":"access blocked"}` |
| Betby UI | GET https://ui.invisiblesport.com/bt-renderer.min.js | brand/jwt | 脚本 200 | 脚本体内是 403 错误页 | 未授权/地区拦 |
| Polymarket | GET gamma-api + clob.polymarket.com/book | 无 | **是** | TI 冠军盘 8 支未淘汰队 CLOB 买卖价 | — |
| Pinnacle | GET guest.api.arcadia.pinnacle.com/0.1/matchups/1633296958/markets/straight | 无 | **是（盘已关）** | cutoffAt=2026-08-13T05:00:00Z，限额 100，过期美式价仍挂着 | 期货不可成交 |
| Predict.fun | 本轮未作为主目标 | — | 上轮 401/无买卖价 | — | 仍不当作可执行盘 |

成功 URL：`https://stake.us/_api/graphql`（握手+schema）；`https://duel.com/api/v2/metadata`；`https://duel.com/assets/sports-fT7y-JGf.js`；`https://gamma-api.polymarket.com/events?slug=the-international-2026-winner-20260629212545745`；`https://clob.polymarket.com/book?token_id=...`（8 支）；`https://guest.api.arcadia.pinnacle.com/0.1/matchups/1633296958/markets/straight`；`https://guest.api.arcadia.pinnacle.com/0.1/leagues/5055/matchups`；`https://help.stake.com/en/articles/4828278-what-does-it-mean-when-a-bet-is-voided`。

失败 URL：Stake 主站/mirror GraphQL 全 403；`https://stake.com/policies/sportsbook` 403；Duel match-betting 403 产品关；Duel user-session 403 地区拦；sports-proxy 403。

---

## 表2 Stake 冠军盘

| 队伍 | 赔率 | 隐含概率 | 限额 | 状态 |
|---|---|---|---|---|
| （无） | — | — | — | **本轮没有从 Stake 拿到任何冠军盘价格** |

说明：query 已写进 `apis/stake_client.py`（`slugSport` → `slugTournament` → `sportFixture` + `groups(groups:["winner"])`）。对 `stake.us` 实跑：握手 200，`slugSport(sport:"dota-2")` 200 但 `serviceDisabled`，12 组 slug 组合均为空。sport slug 确认为 `dota-2`；tournament slug 候选 `the-international` / `the-international-2026`，实体 id 未解析到。win.gg 2026-08-11 文章写过 Stake VISION 2.80，那是第三方旧文且本页未渲染数字，**不当作本轮 Stake 现价**。

---

## 表3 Duel 冠军盘

| 队伍 | 赔率 | 隐含概率 | 限额 | 状态 |
|---|---|---|---|---|
| （无） | — | — | — | **本轮没有从 Duel 拿到任何冠军盘价格** |

说明：内部接口已定位。`duel_client.py` 复跑仍是：metadata 200；match-betting「暂时关闭」；user-session 被美国 IP 拦。不缺用户密码。缺：match-betting 重新打开 + 非封锁出口。

---

## 表4 四平台对照（PM / PIN / Stake / Duel）

价格口径：PM = 本轮 CLOB YES 可买价（best ask），括号内 mid≈(bid+ask)/2。PIN = 本轮仍返回的美式价，但 cutoff 已过，**不可成交**。Stake/Duel = 无价。

| 队伍 | PM 可买 / mid | PIN（已关） | Stake | Duel | 最大价差 | 能否对冲 | 规则风险 |
|---|---|---|---|---|---|---|---|
| TEAM VISION / PVISION | 0.41 / 0.400 | +200 → 3.00（33.3%）cutoff 过期 | 无 | 无 | 仅 PM↔过期 PIN，约 7.3pp | 否 | PIN 不可成交；Stake 取消退本 vs PM 按官方冠军 |
| Team Spirit | 0.13 / 0.120 | +750 → 8.50（11.8%）过期 | 无 | 无 | 无活盘差 | 否 | 同上 |
| Team Liquid | 0.12 / 0.105 | +700 → 8.00（12.5%）过期 | 无 | 无 | 无活盘差 | 否 | 同上 |
| Team Falcons | 0.10 / 0.095 | +650 → 7.50（13.3%）过期 | 无 | 无 | 无活盘差 | 否 | 同上 |
| Team Yandex | 0.102 / 0.0965 | +300 → 4.00（25.0%）过期 | 无 | 无 | 过期 PIN 明显偏高，不能吃 | 否 | 小组赛前定价，含已淘汰队 |
| Nigma Galaxy | 0.087 / 0.0775 | +2400 → 25.00（4.0%）过期 | 无 | 无 | 无活盘差 | 否 | 同上 |
| 1w / Iron Wing | 0.079 / 0.0765 | +1196 → 12.96（7.7%）过期 | 无 | 无 | 无活盘差 | 否 | 队名映射已确认，结算源仍要再核 |
| BoomBoys / BB Team | 0.080 / 0.075 | +400 → 5.00（20.0%）过期 | 无 | 无 | 过期 PIN 偏高，不能吃 | 否 | 同上 |
| 已淘汰（Aurora/XG/HULIGANI/Vici/OG/LGD/GL/Resilience） | PM 已关，YES=0 | PIN 仍挂旧价 | 无 | 无 | — | 否 | PIN 名单未更新是盘已死的证据 |

PM CLOB 深度（本轮）：VISION ask 366 份；Spirit 665；Liquid 303；Falcons 596；Yandex 118；NGX 258；1w 仅 45；BoomBoys 25。1w/BoomBoys 深度薄。

PIN 期货：matchup 1633296958，`cutoffAt=2026-08-13T05:00:00+00:00`（13:00 CST），`maxRiskStake=100`，`status=pending`，`startTime=2026-08-13T05:00:00Z`。价是小组赛前的，Yandex/BB 还按热门挂着，已淘汰队没下架。

---

## 表5 复用方法

| 平台 | 请求方式 | 关键 query/path | 还缺什么 |
|---|---|---|---|
| Stake | POST GraphQL，无 token | `slugSport(sport:"dota-2")` → `slugTournament(sport,category,tournament)` → `sportFixture(id)` + `groups(groups:["winner"])`；搜索 `sportFixtureQuery(query)`；限额 `sportMaxBet` | 过 Cloudflare 的 host（或恢复的体育后端）。fixture id / 确切 TI slug。policies 电竞原文 |
| Stake 公开流 | 同上 | `allSportBets` / `highrollerSportBets` | 本轮空。不能当赔率源 |
| Duel | POST `/api/v2/match-betting/betby/user-session/{lang}/{ccy}/{fiat}` → Betby JWT + `libraryUrl` → `BTRenderer`（brand `2482975601191952386`，operator `2432909813404016640`，theme `duel`） | 深链 `bt-path`；赔率在 `sports-proxy.duel.com` | match-betting 重新打开；非美/非封锁 IP；session 成功后的 Betby 内部 REST 路径（iframe 没起来，未抓到 XHR） |
| Polymarket | GET gamma event + CLOB book | slug `the-international-2026-winner-20260629212545745` | 无（冠军盘已通） |
| Pinnacle | GET guest arcadia | league 5055，futures matchup 1633296958 | 期货重开或新的 outright matchup |

脚本：`/workspace/arb-radar/apis/stake_client.py`、`/workspace/arb-radar/apis/duel_client.py`。文档：`apis/stake.md`、`apis/duel.md`。

---

## 表6 结论

| 问题 | 结论 |
|---|---|
| 有没有冠军盘套利？ | **没有。** 活盘只有 Polymarket。PIN 期货 8/13 05:00 UTC 已 cutoff。Stake/Duel 本轮零价格，无法对冲。 |
| Stake API 卡在哪？ | 主站/mirror 卡 Cloudflare。`stake.us` GraphQL 通，但体育服务 `serviceDisabled`。query 名、参数、outright 形态已经确定，缺的是能返回 `data.slugSport` 的 host。 |
| Duel API 卡在哪？ | 接口已拆完（Betby session）。卡在产品关闭 + 美国 IP 封锁。不卡登录密码。 |
| 规则 | Stake help：取消/腰斩一般 x1 退本。完整电竞/冠军盘条款在 `stake.com/policies/sportsbook`（CF 拦了）。Duel 规则页 `/sports-betting-rules`，i18n 显示 Updated: 01.06.2026，正文未拉到。和 PM「官方冠军 / 比赛盘 50-50」不能当作同一套 void。 |
| 下一步 | 1) 非美出口或带 cf_clearance 的浏览器再跑 `stake_client.py`；2) 同一出口再跑 `duel_client.py` 等 match-betting 开；3) PIN 若重开 1633296958 或新 futures，先核队名再核 cutoff。 |

本报告只做拉盘与对照，不下单。
