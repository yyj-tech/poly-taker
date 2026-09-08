---
name: 套利雷达扫描
description: 当用户要看套利/套现机会、说 /arb，或小时扫描时使用。必须输出价格对照表和仓位表。
---
# 套利雷达扫描

只查数据、汇总机会，永不下单。

## 固定输出：两张表

不要把多平台挤进一格。价和仓位分开。

### 表1 价格对照

| 状态 | 事件 | 队A | 队B | PM_A | PM_B | PIN_A | PIN_B | Stake_A | Stake_B | Duel_A | Duel_B |

- PM 写可买 ask；PIN/Stake/Duel 写欧赔
- 缺写—
- 不要用冠军盘冒充比赛盘

### 表2 套现仓位

| 状态 | 事件 | 左买 | 右买 | 成本 | 手续费 | 利率 | 多久结算 | 一单利润 |

- 仓位按 PM 最佳 ask 深度；博彩 D = 份数 / 欧赔
- 成本 = 博彩 + PM 花费 + PM 费
- 手续费 = PM taker = 花费 × 0.05 × p × (1−p)；博彩无佣金；未扣提现
- 利率 = 费后利润 / 成本
- 一单利润 = 收回 − 成本（U）
- 按一单利润从高到低
- 规则不一致必须标出，不升格为高价值（≥1.5% 且规则一致）
- 没有合格机会也出表

## 数据源（不要网页抓 Stake/Duel）

1. Polymarket：官方 CLOB / Gamma，可买 ask + 深度
2. Pinnacle：`guest.api.arcadia.pinnacle.com` HTTP（电竞 sportId=12，TI 联赛 5055）。不是浏览器。
3. Stake / Duel：只走 **odds-api.io**。跑 `python3 /workspace/arb-radar/apis/odds_api_io.py`，读 `scans/odds-api-io-matched.json`。Key 在环境变量 `ODDS_API_IO_KEY` 或 `apis/.odds_api_io_key`。
4. 匹配同一事件对立面，算两腿
5. 只输出两张表，不要散文

读不到的格子写—。不要退回 Stake GraphQL / Duel Betby / 打开网页。
