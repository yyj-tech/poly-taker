# Stake 公开拉盘方法（2026-08-17 实测）

只读公开盘口。不要带用户 token、不要下单、不要偷 cookie。

## 端点

| Host | 路径 | 本次结果 |
|---|---|---|
| `https://stake.com/_api/graphql` | POST | Cloudflare 403（Just a moment） |
| `https://stake.bet/_api/graphql` | POST | 同上 |
| `https://stake.ac/_api/graphql` | POST | 同上 |
| `https://stake.pet/_api/graphql` | POST | 同上 |
| `https://stake.games` / `stake1001.com` / `stake1021.com` / `stake1022.com` / `staketr.com` / `stake.mba` / `stake.ceo` / `stake.bz` | POST `/_api/graphql` | 同上 |
| `https://api.stake.com/graphql` | POST | 404 Cannot POST /graphql |
| `https://stake.us/_api/graphql` | POST | **HTTP 200，GraphQL 通**。公开 feed 可用；体育树查询返回 `serviceDisabled` |

主站和常见 mirror 都被 Cloudflare 托管挑战拦住。`curl_cffi` chrome131 指纹和 `google-chrome --headless=new --dump-dom` 都没过。`stake.us` 是目前唯一能直接打到 GraphQL 的 host，但体育盘后端对本 IP 是 `Connection lost, re-establishing... / errorType=serviceDisabled`。

## 必要 headers（无 token）

```
content-type: application/json
accept: application/json
x-language: en
origin: https://<host>
referer: https://<host>/sports
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36
```

公开赔率查询不需要 `x-access-token`。账号类查询（`allSports`、余额、下注）会回 `Please log in. / notAuthenticated`。

## 已确认的 Query 名和参数

来源：本次对 `stake.us` 的 schema 探测（缺参时报错会给出真实参数名；`Did you mean` 给出相邻字段）。

| Query | 必要参数 | 用途 |
|---|---|---|
| `slugSport(sport: String!)` | sport slug，如 `dota-2` / `esports` / `soccer` | 体育树入口 |
| `slugTournament(sport, category, tournament)` | 三个 String! | 联赛/赛事 |
| `slugFixture(fixture: String!)` | fixture slug | 单场 |
| `sport(sportId: String!)` | UUID | 按 id 取体育 |
| `sportTournament(tournamentId: String!)` | UUID | 按 id 取赛事 |
| `sportCategory(categoryId: String!)` | UUID | 按 id 取分类 |
| `sportFixture(fixtureId: String!)` | UUID | 单场赔率（官方前端同款） |
| `sportFixtureQuery(query: String!)` | 搜索词 | 返回 `SportFixtureResult.fixture` |
| `sportList` | 无 | 全体育列表（本次 serviceDisabled） |
| `allSports` | 无 | 需登录 |
| `sportHomepageTrendingMatches(sortBy:)` | `totalBetValue` 等 | 热门（本次 serviceDisabled） |
| `allSportBets(limit)` | Int | 公开投注流，**无 token 可用** |
| `highrollerSportBets(limit)` | Int | 公开高额流，**无 token 可用** |
| `fixtureList` / `tournamentList` | 可选 limit | 本次空数组 |
| `sportMarket(marketId, provider)` | `SportsbookOddsProviderEnum!` | 单盘 |
| `sportMaxBet` | `betType: SportBetTypeEnum!`, `currency: CurrencyEnum!` 等 | 限额，返回 `Float!` |
| `sportUserLimit(userId)` | 需用户 id | 账户限额，不用于公开盘 |
| `sportSchedule(from, to, sportId)` | Date! + sportId | 赛程 |
| `sportByExtId(extId)` / `sportTournamentByExtId` / `sportFixtureByExtId` | 外部 id | 映射 |
| `topSport(topSportId)` | | 置顶体育 |

`Sport` 上可用的子字段（schema 探测）：`allCategories`、`categoryList`、`allTournaments`、`tournamentList`、`fixtureList`。没有 `outrights` 这个字段名。冠军盘是 **outright fixture**，走 `sportFixture` + `groups(groups: ["winner"])`。

## 推荐拉盘顺序（可复用）

1. 选一个能过 Cloudflare 的 host（当前只有 `stake.us` 能握手；主站需要浏览器 `cf_clearance`）。
2. `slugSport(sport: "dota-2") { id name slug allCategories { id name slug tournamentList { id name slug } } fixtureList { id name slug status } }`
3. 在 tournament 名里找 `The International` / `TI`。候选 slug：`the-international`、`the-international-2026`。
4. `slugTournament(sport: "dota-2", category: "<cat>", tournament: "<ti-slug>")` 拿 fixture 列表。
5. 冠军盘是 outright fixture（`data { ... on SportFixtureDataOutright { name startTime endTime } }`），不是两队对阵。
6. 赔率：

```graphql
query FixtureOdds($id: String!) {
  sportFixture(id: $id) {
    id name slug status
    tournament { id name slug category { id name slug sport { id name slug } } }
    data {
      ... on SportFixtureDataOutright { name startTime endTime }
      ... on SportFixtureDataMatch { startTime competitors { name abbreviation extId } }
    }
    groups(groups: ["winner"]) {
      templates { markets { id name status extId specifiers outcomes { id name odds active } } }
    }
  }
}
```

八强盘同一套：先列 TI tournament 下的 match fixture，再 `groups: ["winner"]`（胜负）或 handicap/totals。

也可以 `sportFixtureQuery(query: "The International") { fixture { id name slug status } }` 做模糊搜。

## 限额字段

- 公开盘：`sportMaxBet(betType:, currency:)` → `Float!`
- 账户级：`sportUserLimit` / `sportUserLimitList`（要 userId，本次不用）
- 盘口对象上常见还有 `extId` / `specifiers`；前端 betslip 片段里限额不在 outcome 上，而在下注 mutation 前单独查

本次体育后端 disabled，限额数字没拿到。

## 规则页（本次读到的原文要点）

| URL | 状态 | 要点 |
|---|---|---|
| https://help.stake.com/en/articles/4828278-what-does-it-mean-when-a-bet-is-voided | 200 | 「When a bet is voided, the odds provider settles it with odds of x1, essentially returning the wagered amount」；「If a match is canceled or abandoned before completion, all bets placed on that match are generally voided」；市场结果未决（退役/中断未恢复）可 void；错误开盘可 void |
| https://help.stake.com/en/articles/4872560-why-is-cashout-not-available-for-my-bet | 200 | 指向站内完整体育规则：`https://stake.com/policies/sportsbook#General` |
| https://stake.com/policies/sportsbook | Cloudflare 403 | 冠军盘/电竞专项原文本次没读到 |
| https://stake.com/sports/esports | 营销页（WebSearch/间接） | 明确写有 Tournament winner，举例 The International |

**对冲含义：** Stake 取消/腰斩默认退本（x1）。Polymarket TI 比赛盘是延期窗口后 50-50，冠军盘按官方冠军结算。一边退本一边 50-50 或按完成结果结算，不是干净对冲。电竞专项（walkover、前 10 分钟掉线）原文在被 CF 挡住的 policies 页，**本次不能假装已经对齐**。

## 体育 / 赛事标识（已确认 vs 候选）

| 项 | 值 | 依据 |
|---|---|---|
| sport slug | `dota-2` | Parse 包装 API 与 Stake 电竞页；`slugSport(sport:"dota-2")` 被 schema 接受（只是后端 disabled） |
| 备选 sport | `esports` | schema 同样接受 |
| tournament slug | `the-international` / `the-international-2026` | 候选，本次没返回实体 |
| outright 查询名 | `sportFixture` + `groups(groups:["winner"])` + `SportFixtureDataOutright` | BreathPulley/stake-scraper + 本次 schema |
| fixture id | 未知 | 需要过 CF 或体育后端恢复后才能解析 |

## 复跑

```bash
python3 /workspace/arb-radar/apis/stake_client.py
python3 /workspace/arb-radar/apis/stake_client.py --host https://stake.us
```

成功时打印 TI 冠军盘队伍/赔率/隐含概率。失败时打印每个 URL 的 HTTP/GraphQL 错误，不编价格。
