# LoL 跨平台盘口扫描（第一次）

快照：2026-08-17 13:30 CST（Asia/Shanghai）  
范围：Polymarket / Pinnacle / Stake / Duel 上能配上的同一 LoL 事件  
原则：只写本次实际请求到的数字；不下单；不编造价格。  
套利公式：左博彩本金 D、欧赔 O；右 PM 买对立面份数 = D×O、价 = 可买 ask；稳收回 = D×O；taker fee = 花费×0.05×p×(1-p)；利润 = 收回−D−PM花费−fee。转正：PM NO ask < 1−1/O。  
高价值：费后净 ≥ 1.5% 且能立刻吃、规则基本一致。本次 **0 条**。

## 表1 概览

| 平台 | LoL 盘数量 | 能否成交 | 缺口 |
|---|---|---|---|
| Polymarket | Gamma「League of Legends」活跃事件 totalResults=174（本页 50）；去噪后本次合并去重 slug 140。CLOB 实盘：7 场跨平台比赛胜负/让分/大小/G1 共 90 token 全 200。另有 Worlds 赛区 / LPL / LCK 赛季冠军盘（Gamma） | 能（CLOB 7 场胜负均有 bid/ask；3v/LYON 胜负 ask 仅 28.75 份偏薄） | MSI 搜索 0。LPL/LCK 主联赛今日无单场（只有赛季冠军）。Worlds 只有 Winning Region，无单场。部分趣味盘价差 90c+ 近空盘 |
| Pinnacle | sports/12 活跃联赛 11 条，LoL 5 条：LCK CL / LEC / KeSPA Cup / LRN / Circuito Desafiante。父对阵 7 场，period 0 全场 ML 均为 status=open | 能（straight 接口现价 + maxRiskStake 125–2500） | **无 LPL、无 LCK 主联赛、无 Worlds**。已关闭期货不当现价（本轮这 7 场都是未开打的 open period 0） |
| Stake（国际站 stake.com） | 0（未读到任何 LoL 赔率） | 否 | stake.com GraphQL/电竞页 Cloudflare 403。stake.us GraphQL 握手 200 但 slugSport(league-of-legends/esports) 回 serviceDisabled，allSportBets=[]。**不要用 stake.us**（无真钱电竞） |
| Duel | 0（未读到任何 LoL 赔率） | 否 | 体育盘是 Betby iframe。/api/v2/match-betting 历史明确「temporarily disabled」；本次 metadata/match-betting 403 挑战页，sports-proxy 403 access blocked。美国出口 IP。**需网页 + 非美出口**，不编价 |

## 表2 Polymarket LoL 现价（CLOB，跨平台 7 场胜负）

结算原文要点（7 场单场胜负同构）：结算源 gol.gg；2 小时无结果可用可信报道/录像；取消或平局 → 50-50；延期须在原定开赛后 14 个自然日内重赛，否则 50-50；开打后对手弃权/DQ/walkover → 判胜者；赛前撤队自动获胜 → 50-50；队名轻微差异按真实比赛识别，无法唯一对应 → 50-50。

| 事件 | 队伍/方向 | YES bid / 量 | YES ask / 量 | NO ask / 量 | 开赛 CST | 截止 UTC |
|---|---|---:|---:|---:|---|---|
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | Dplus KIA Challengers | 0.59 / 3410.12 | 0.60 / 35404.71 | 0.41 / 3410.12 | 2026-08-17 16:15 | 2026-08-17T14:00:00Z |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | KT Rolster Challengers | 0.40 / 35404.71 | 0.41 / 3410.12 | 0.60 / 35404.71 | 2026-08-17 16:15 | 2026-08-17T14:00:00Z |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | Kiwoom DRX Challengers | 0.65 / 3328.37 | 0.66 / 3288.00 | 0.35 / 3328.37 | 2026-08-17 18:15 | 2026-08-17T16:00:00Z |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | Hanwha Life Esports Challengers | 0.34 / 3288.00 | 0.35 / 3328.37 | 0.66 / 3288.00 | 2026-08-17 18:15 | 2026-08-17T16:00:00Z |
| Natus Vincere vs Team Heretics (BO3) LEC | Natus Vincere | 0.68 / 8849.66 | 0.69 / 2897.84 | 0.32 / 8849.66 | 2026-08-17 23:00 | 2026-08-17T21:00:00Z |
| Natus Vincere vs Team Heretics (BO3) LEC | Team Heretics | 0.31 / 2897.84 | 0.32 / 8849.66 | 0.69 / 2897.84 | 2026-08-17 23:00 | 2026-08-17T21:00:00Z |
| GIANTX vs Karmine Corp (BO3) LEC | GIANTX | 0.15 / 10056.03 | 0.16 / 2301.54 | 0.85 / 10056.03 | 2026-08-18 01:15 | 2026-08-17T23:15:00Z |
| GIANTX vs Karmine Corp (BO3) LEC | Karmine Corp | 0.84 / 2301.54 | 0.85 / 10056.03 | 0.16 / 2301.54 | 2026-08-18 01:15 | 2026-08-17T23:15:00Z |
| T1 vs DN SOOPers (BO5) KeSPA Cup | T1 | 0.41 / 1928.09 | 0.42 / 2776.21 | 0.59 / 1928.09 | 2026-08-17 17:00 | 2026-08-17T15:00:00Z |
| T1 vs DN SOOPers (BO5) KeSPA Cup | DN SOOPers | 0.58 / 2776.21 | 0.59 / 1928.09 | 0.42 / 2776.21 | 2026-08-17 17:00 | 2026-08-17T15:00:00Z |
| 3v Team vs LYON Academy (BO5) LRN | 3v Team | 0.85 / 115.68 | 0.86 / 28.75 | 0.15 / 115.68 | 2026-08-18 07:00 | 2026-08-18T05:00:00Z |
| 3v Team vs LYON Academy (BO5) LRN | LYON Academy | 0.14 / 28.75 | 0.15 / 115.68 | 0.86 / 28.75 | 2026-08-18 07:00 | 2026-08-18T05:00:00Z |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | paiN Gaming Academy | 0.64 / 357.53 | 0.65 / 1420.19 | 0.36 / 357.53 | 2026-08-18 07:00 | 2026-08-18T05:00:00Z |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | Ei Nerd Esports | 0.35 / 1420.19 | 0.36 / 357.53 | 0.65 / 1420.19 | 2026-08-18 07:00 | 2026-08-18T05:00:00Z |

### 附表 冠军/赛区（Gamma bestAsk，本轮未拉 CLOB，不当套利腿）

| 事件 | 方向 | YES bid | YES ask | 截止 |
|---|---|---:|---:|---|
| Worlds 2026 Winning Region | LCK (South Korea) YES | 0.650 | 0.660 | 2026-12-31T00:00:00Z |
| Worlds 2026 Winning Region | LPL (China) YES | 0.260 | 0.270 | 2026-12-31T00:00:00Z |
| Worlds 2026 Winning Region | LEC (Europe / EMEA) YES | 0.059 | 0.061 | 2026-12-31T00:00:00Z |
| Worlds 2026 Winning Region | LCS (North America) YES | 0.017 | 0.018 | 2026-12-31T00:00:00Z |
| LPL 2026 Season Winner | Anyone's Legend YES | 0.150 | 0.160 | — |
| LPL 2026 Season Winner | Bilibili Gaming YES | 0.530 | 0.580 | — |
| LPL 2026 Season Winner | Invictus Gaming YES | 0.046 | 0.048 | — |
| LPL 2026 Season Winner | JD Gaming YES | 0.060 | 0.061 | — |
| LPL 2026 Season Winner | Ninjas in Pyjamas YES | 0.014 | 0.017 | — |
| LPL 2026 Season Winner | Team WE YES | 0.027 | 0.062 | — |
| LPL 2026 Season Winner | Top Esports YES | 0.122 | 0.123 | — |
| LCK 2026 Season Winner | Dplus YES | 0.170 | 0.174 | 2026-12-31T00:00:00Z |
| LCK 2026 Season Winner | FEARX YES | 0.012 | 0.014 | 2026-12-31T00:00:00Z |
| LCK 2026 Season Winner | Gen.G Esports YES | 0.360 | 0.370 | 2026-12-31T00:00:00Z |
| LCK 2026 Season Winner | Hanwha Life Esports YES | 0.203 | 0.206 | 2026-12-31T00:00:00Z |
| LCK 2026 Season Winner | KT Rolster YES | 0.053 | 0.057 | 2026-12-31T00:00:00Z |
| LCK 2026 Season Winner | T1 YES | 0.220 | 0.230 | 2026-12-31T00:00:00Z |

PIN 无 LPL/LCK/Worlds 对应期货，上表只作 PM 现价记录。

## 表3 跨平台匹配

| 事件 | PM | PIN | Stake | Duel | 是否同一事件 |
|---|---|---|---|---|---|
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | Dplus KIA Challengers YES ask 0.6×35404.71；KT Rolster Challengers YES ask 0.41×3410.12 | ML Dplus KIA Challengers -178 (1.562) / KT Rolster Challengers +144 (2.440)；限额 1000；status=open | 无价 | 无价 | 是（同一场 BO3；PIN 开赛 08:15Z，PM gameStart 08:00Z，差 15 分钟） |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | Kiwoom DRX Challengers YES ask 0.66×3288.00；Hanwha Life Esports Challengers YES ask 0.35×3328.37 | ML Kiwoom DRX Challengers -181 (1.552) / Hanwha Life Challengers +146 (2.460)；限额 250；status=open | 无价 | 无价 | 是（同一场 BO3；PIN「Hanwha Life Challengers」= PM「Hanwha Life Esports Challengers」） |
| Natus Vincere vs Team Heretics (BO3) LEC | Natus Vincere YES ask 0.69×2897.84；Team Heretics YES ask 0.32×8849.66 | ML Natus Vincere -230 (1.435) / Heretics +181 (2.810)；限额 2500；status=open | 无价 | 无价 | 是（同一场 BO3；PIN「Heretics」= PM「Team Heretics」） |
| GIANTX vs Karmine Corp (BO3) LEC | GIANTX YES ask 0.16×2301.54；Karmine Corp YES ask 0.85×10056.03 | ML GIANTX +407 (5.070) / Karmine Corp -649 (1.154)；限额 2500；status=open | 无价 | 无价 | 是（同一场 BO3，队名一致） |
| T1 vs DN SOOPers (BO5) KeSPA Cup | T1 YES ask 0.42×2776.21；DN SOOPers YES ask 0.59×1928.09 | ML T1 +147 (2.470) / DN SOOPers -182 (1.549)；限额 500；status=open | 无价 | 无价 | 是（同一场 BO5 季后赛，队名一致） |
| 3v Team vs LYON Academy (BO5) LRN | LYON Academy YES ask 0.15×115.68；3v Team YES ask 0.86×28.8 | ML LYON Academy +471 (5.710) / 3v -803 (1.125)；限额 1000；status=open | 无价 | 无价 | 是（同一场 BO5；PIN 主客 LYON vs 3v，PM 标题对调） |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | Ei Nerd Esports YES ask 0.36×357.53；paiN Gaming Academy YES ask 0.65×1420.19 | ML Ei Nerd +162 (2.620) / paiN Academy -204 (1.490)；限额 250；status=open | 无价 | 无价 | 是（同一场 BO3；PIN 主客 Ei Nerd vs paiN Academy，PM 标题对调） |
| Worlds 2026 Winning Region | Gamma：LCK 0.66 / LPL 0.27 / LEC 0.061 | 无联赛 | 无价 | 无价 | PIN 无 Worlds，不能配 |
| LPL 2026 Season Winner | Gamma：BLG 0.58 / AL 0.16 / TES 0.123 等 | 无 LPL 联赛 | 无价 | 无价 | 不能配 |
| LCK 2026 Season Winner | Gamma：Gen.G 0.37 / T1 0.23 / HLE 0.206 / Dplus 0.174 | 无 LCK 主联赛（只有 LCK CL） | 无价 | 无价 | 不能配 |

## 表4 套利仓位（核心，按费后从好到差）

左=Pinnacle 买某结果，本金按 **100 USDT** 列（「每 100 USDT 博彩本金」）。右=Polymarket 买该结果 NO（即对立面 YES ask）。深度=min(PIN maxRiskStake, PM 最佳档 ask 量 / O)。没有正利润也出表。**费后 ≥1.5% 且规则一致：0 条。**

| 事件 | 盘种 | 左（平台/方向/美式/欧赔/金额） | 右（平台/方向/ask/份数/花费） | fee | 深度可执行D | 总投入 | 稳收回 | 费后利润 | 费后% | 要转正还差（ask−(1−1/O)） |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | 全场胜负 | Pinnacle / Kiwoom DRX Challengers 胜 / -181 / 1.552 / 100.00 | Polymarket / Kiwoom DRX Challengers NO（买 Hanwha Life Esports Challengers YES） / 0.350 / 155.25 / 54.34 | 0.62 | 250.00（PIN 250.00 / PM折D 2143.90） | 154.96 | 155.25 | 0.29 | 0.19% | 已转正 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 全场胜负 | Pinnacle / T1 胜 / +147 / 2.470 / 100.00 | Polymarket / T1 NO（买 DN SOOPers YES） / 0.590 / 247.00 / 145.73 | 1.76 | 500.00（PIN 500.00 / PM折D 780.60） | 247.49 | 247.00 | -0.49 | -0.20% | 费前已转正（−0.005），费后仍负 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 让分 +1.5/-1.5 | Pinnacle / DN SOOPers -1.5 / +120 / 2.200 / 100.00 | Polymarket / DN SOOPers -1.5 NO（买 T1 +1.5 YES） / 0.550 / 220.00 / 121.00 | 1.50 | 361.01（PIN 500.00 / PM折D 361.01） | 222.50 | 220.00 | -2.50 | -1.12% | 0.004 |
| GIANTX vs Karmine Corp (BO3) LEC | 让分 +1.5/-1.5 | Pinnacle / Karmine Corp -1.5 / -148 / 1.676 / 100.00 | Polymarket / Karmine Corp -1.5 NO（买 GIANTX +1.5 YES） / 0.410 / 167.57 / 68.70 | 0.83 | 1926.84（PIN 2500.00 / PM折D 1926.84） | 169.53 | 167.57 | -1.97 | -1.16% | 0.007 |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | Game 1 胜负 | Pinnacle / Kiwoom DRX Challengers G1 / -156 / 1.641 / 100.00 | Polymarket / Kiwoom DRX Challengers G1 NO（买 Hanwha Life Esports Challengers G1 YES） / 0.400 / 164.10 / 65.64 | 0.79 | 125.00（PIN 125.00 / PM折D 851.92） | 166.43 | 164.10 | -2.33 | -1.40% | 0.009 |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | 让分 -1.5/+1.5 | Pinnacle / Kiwoom DRX Challengers -1.5 / +171 / 2.710 / 100.00 | Polymarket / Kiwoom DRX Challengers -1.5 NO（买 Hanwha Life Esports Challengers +1.5 YES） / 0.640 / 271.00 / 173.44 | 2.00 | 250.00（PIN 250.00 / PM折D 1519.21） | 275.44 | 271.00 | -4.44 | -1.61% | 0.009 |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | 全场胜负 | Pinnacle / KT Rolster Challengers 胜 / +144 / 2.440 / 100.00 | Polymarket / KT Rolster Challengers NO（买 Dplus KIA Challengers YES） / 0.600 / 244.00 / 146.40 | 1.76 | 1000.00（PIN 1000.00 / PM折D 14510.13） | 248.16 | 244.00 | -4.16 | -1.68% | 0.010 |
| Natus Vincere vs Team Heretics (BO3) LEC | Game 1 胜负 | Pinnacle / Natus Vincere G1 / -180 / 1.556 / 100.00 | Polymarket / Natus Vincere G1 NO（买 Team Heretics G1 YES） / 0.370 / 155.56 / 57.56 | 0.67 | 6.43（PIN 1250.00 / PM折D 6.43） | 158.23 | 155.56 | -2.67 | -1.69% | 0.013 |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | 让分 -1.5/+1.5 | Pinnacle / KT Rolster Challengers +1.5 / -216 / 1.463 / 100.00 | Polymarket / KT Rolster Challengers +1.5 NO（买 Dplus KIA Challengers -1.5 YES） / 0.330 / 146.30 / 48.28 | 0.53 | 114.90（PIN 1000.00 / PM折D 114.90） | 148.81 | 146.30 | -2.52 | -1.69% | 0.013 |
| Natus Vincere vs Team Heretics (BO3) LEC | 全场胜负 | Pinnacle / Natus Vincere 胜 / -230 / 1.435 / 100.00 | Polymarket / Natus Vincere NO（买 Team Heretics YES） / 0.320 / 143.48 / 45.91 | 0.50 | 2500.00（PIN 2500.00 / PM折D 6167.94） | 146.41 | 143.48 | -2.93 | -2.00% | 0.017 |
| GIANTX vs Karmine Corp (BO3) LEC | 全场胜负 | Pinnacle / Karmine Corp 胜 / -649 / 1.154 / 100.00 | Polymarket / Karmine Corp NO（买 GIANTX YES） / 0.160 / 115.41 / 18.47 | 0.12 | 1994.26（PIN 2500.00 / PM折D 1994.26） | 118.59 | 115.41 | -3.18 | -2.68% | 0.026 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | Game 1 胜负 | Pinnacle / DN SOOPers G1 / -140 / 1.714 / 100.00 | Polymarket / DN SOOPers G1 NO（买 T1 G1 YES） / 0.440 / 171.43 / 75.43 | 0.93 | 250.00（PIN 250.00 / PM折D 618.91） | 176.36 | 171.43 | -4.93 | -2.80% | 0.023 |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | Game 1 胜负 | Pinnacle / Dplus KIA Challengers G1 / -153 / 1.654 / 100.00 | Polymarket / Dplus KIA Challengers G1 NO（买 KT Rolster Challengers G1 YES） / 0.420 / 165.36 / 69.45 | 0.85 | 500.00（PIN 500.00 / PM折D 604.74） | 170.30 | 165.36 | -4.94 | -2.90% | 0.025 |
| 3v Team vs LYON Academy (BO5) LRN | 让分 +2.5/-2.5 | Pinnacle / LYON Academy +2.5 / -168 / 1.595 / 100.00 | Polymarket / LYON Academy +2.5 NO（买 3v Team -2.5 YES） / 0.400 / 159.52 / 63.81 | 0.77 | 233.76（PIN 1000.00 / PM折D 233.76） | 164.58 | 159.52 | -5.05 | -3.07% | 0.027 |
| GIANTX vs Karmine Corp (BO3) LEC | Game 1 胜负 | Pinnacle / Karmine Corp G1 / -354 / 1.282 / 100.00 | Polymarket / Karmine Corp G1 NO（买 GIANTX G1 YES） / 0.250 / 128.25 / 32.06 | 0.30 | 1122.80（PIN 1250.00 / PM折D 1122.80） | 132.36 | 128.25 | -4.11 | -3.11% | 0.030 |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | Game 1 胜负 | Pinnacle / paiN Academy G1 / -169 / 1.592 / 100.00 | Polymarket / paiN Gaming Academy G1 NO（买 Ei Nerd Esports G1 YES） / 0.400 / 159.17 / 63.67 | 0.76 | 12.57（PIN 125.00 / PM折D 12.57） | 164.43 | 159.17 | -5.26 | -3.20% | 0.028 |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | 全场胜负 | Pinnacle / paiN Academy 胜 / -204 / 1.490 / 100.00 | Polymarket / paiN Gaming Academy NO（买 Ei Nerd Esports YES） / 0.360 / 149.02 / 53.65 | 0.62 | 239.92（PIN 250.00 / PM折D 239.92） | 154.27 | 149.02 | -5.25 | -3.40% | 0.031 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 让分 +2.5/-2.5 | Pinnacle / DN SOOPers -2.5 / +318 / 4.180 / 100.00 | Polymarket / DN SOOPers -2.5 NO（买 T1 +2.5 YES） / 0.790 / 418.00 / 330.22 | 2.74 | 0.89（PIN 500.00 / PM折D 0.89） | 432.96 | 418.00 | -14.96 | -3.46% | 0.029 |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | Game 1 胜负 | Pinnacle / Ei Nerd G1 / +138 / 2.380 / 100.00 | Polymarket / Ei Nerd Esports G1 NO（买 paiN Gaming Academy G1 YES） / 0.610 / 238.00 / 145.18 | 1.73 | 125.00（PIN 125.00 / PM折D 350.40） | 246.91 | 238.00 | -8.91 | -3.61% | 0.030 |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | 全场胜负 | Pinnacle / Ei Nerd 胜 / +162 / 2.620 / 100.00 | Polymarket / Ei Nerd Esports NO（买 paiN Gaming Academy YES） / 0.650 / 262.00 / 170.30 | 1.94 | 250.00（PIN 250.00 / PM折D 542.06） | 272.24 | 262.00 | -10.24 | -3.76% | 0.032 |
| 3v Team vs LYON Academy (BO5) LRN | 全场胜负 | Pinnacle / 3v 胜 / -803 / 1.125 / 100.00 | Polymarket / 3v Team NO（买 LYON Academy YES） / 0.150 / 112.45 / 16.87 | 0.11 | 102.87（PIN 1000.00 / PM折D 102.87） | 116.98 | 112.45 | -4.52 | -3.87% | 0.039 |
| 3v Team vs LYON Academy (BO5) LRN | 全场胜负 | Pinnacle / LYON Academy 胜 / +471 / 5.710 / 100.00 | Polymarket / LYON Academy NO（买 3v Team YES） / 0.860 / 571.00 / 491.06 | 2.96 | 5.04（PIN 1000.00 / PM折D 5.04） | 594.02 | 571.00 | -23.02 | -3.87% | 0.035 |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | Game 1 胜负 | Pinnacle / KT Rolster Challengers G1 / +125 / 2.250 / 100.00 | Polymarket / KT Rolster Challengers G1 NO（买 Dplus KIA Challengers G1 YES） / 0.590 / 225.00 / 132.75 | 1.61 | 500.00（PIN 500.00 / PM折D 2421.33） | 234.36 | 225.00 | -9.36 | -3.99% | 0.034 |
| Natus Vincere vs Team Heretics (BO3) LEC | 总局数 O/U 2.5 | Pinnacle / Under 2.5 / -136 / 1.735 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.460 / 173.53 / 79.82 | 0.99 | 188.70（PIN 1500.00 / PM折D 188.70） | 180.81 | 173.53 | -7.29 | -4.03% | 0.036 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | Game 1 胜负 | Pinnacle / T1 G1 / +115 / 2.150 / 100.00 | Polymarket / T1 G1 NO（买 DN SOOPers G1 YES） / 0.570 / 215.00 / 122.55 | 1.50 | 250.00（PIN 250.00 / PM折D 811.68） | 224.05 | 215.00 | -9.05 | -4.04% | 0.035 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 让分 -2.5/+2.5 | Pinnacle / T1 -2.5 / +571 / 6.710 / 100.00 | Polymarket / T1 -2.5 NO（买 DN SOOPers +2.5 YES） / 0.890 / 671.00 / 597.19 | 2.92 | 10.77（PIN 500.00 / PM折D 10.77） | 700.11 | 671.00 | -29.11 | -4.16% | 0.039 |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | 总局数 O/U 2.5 | Pinnacle / Under 2.5 / -126 / 1.794 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.480 / 179.37 / 86.10 | 1.07 | 375.00（PIN 375.00 / PM折D 438.21） | 187.17 | 179.37 | -7.80 | -4.17% | 0.037 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 让分 -1.5/+1.5 | Pinnacle / T1 -1.5 / +259 / 3.590 / 100.00 | Polymarket / T1 -1.5 NO（买 DN SOOPers +1.5 YES） / 0.760 / 359.00 / 272.84 | 2.49 | 290.18（PIN 500.00 / PM折D 290.18） | 375.33 | 359.00 | -16.33 | -4.35% | 0.039 |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | 总局数 O/U 2.5 | Pinnacle / Over 2.5 / -108 / 1.926 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.520 / 192.59 / 100.15 | 1.25 | 25.44（PIN 200.00 / PM折D 25.44） | 201.40 | 192.59 | -8.81 | -4.37% | 0.039 |
| GIANTX vs Karmine Corp (BO3) LEC | Game 1 胜负 | Pinnacle / GIANTX G1 / +258 / 3.580 / 100.00 | Polymarket / GIANTX G1 NO（买 Karmine Corp G1 YES） / 0.760 / 358.00 / 272.08 | 2.48 | 245.01（PIN 1250.00 / PM折D 245.01） | 374.56 | 358.00 | -16.56 | -4.42% | 0.039 |
| 3v Team vs LYON Academy (BO5) LRN | Game 1 胜负 | Pinnacle / 3v G1 / -307 / 1.326 / 100.00 | Polymarket / 3v Team G1 NO（买 LYON Academy G1 YES） / 0.290 / 132.57 / 38.45 | 0.40 | 21.25（PIN 500.00 / PM折D 21.25） | 138.84 | 132.57 | -6.27 | -4.52% | 0.044 |
| GIANTX vs Karmine Corp (BO3) LEC | 总局数 O/U 2.5 | Pinnacle / Over 2.5 / +150 / 2.500 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.640 / 250.00 / 160.00 | 1.84 | 204.00（PIN 1500.00 / PM折D 204.00） | 261.84 | 250.00 | -11.84 | -4.52% | 0.040 |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | 总局数 O/U 2.5 | Pinnacle / Under 2.5 / -123 / 1.813 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.490 / 181.30 / 88.84 | 1.11 | 200.00（PIN 200.00 / PM折D 2554.03） | 189.95 | 181.30 | -8.65 | -4.55% | 0.042 |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | 总局数 O/U 2.5 | Pinnacle / Over 2.5 / -105 / 1.952 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.530 / 195.24 / 103.48 | 1.29 | 375.00（PIN 375.00 / PM折D 1134.63） | 204.76 | 195.24 | -9.53 | -4.65% | 0.042 |
| Natus Vincere vs Team Heretics (BO3) LEC | 总局数 O/U 2.5 | Pinnacle / Over 2.5 / +103 / 2.030 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.550 / 203.00 / 111.65 | 1.38 | 254.90（PIN 1500.00 / PM折D 254.90） | 213.03 | 203.00 | -10.03 | -4.71% | 0.043 |
| GIANTX vs Karmine Corp (BO3) LEC | 总局数 O/U 2.5 | Pinnacle / Under 2.5 / -208 / 1.481 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.370 / 148.08 / 54.79 | 0.64 | 1049.57（PIN 1500.00 / PM折D 1049.57） | 155.43 | 148.08 | -7.35 | -4.73% | 0.045 |
| 3v Team vs LYON Academy (BO5) LRN | Game 1 胜负 | Pinnacle / LYON Academy G1 / +230 / 3.300 / 100.00 | Polymarket / LYON Academy G1 NO（买 3v Team G1 YES） / 0.740 / 330.00 / 244.20 | 2.35 | 16.80（PIN 500.00 / PM折D 16.80） | 346.55 | 330.00 | -16.55 | -4.78% | 0.043 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 让分 -1.5/+1.5 | Pinnacle / DN SOOPers +1.5 / -396 / 1.252 / 100.00 | Polymarket / DN SOOPers +1.5 NO（买 T1 -1.5 YES） / 0.250 / 125.25 / 31.31 | 0.29 | 500.00（PIN 500.00 / PM折D 616.00） | 131.61 | 125.25 | -6.35 | -4.83% | 0.048 |
| 3v Team vs LYON Academy (BO5) LRN | 让分 +2.5/-2.5 | Pinnacle / 3v -2.5 / +136 / 2.360 / 100.00 | Polymarket / 3v Team -2.5 NO（买 LYON Academy +2.5 YES） / 0.620 / 236.00 / 146.32 | 1.72 | 2.12（PIN 1000.00 / PM折D 2.12） | 248.04 | 236.00 | -12.04 | -4.86% | 0.044 |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | 总局数 O/U 2.5 | Pinnacle / Over 2.5 / -102 / 1.980 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.540 / 198.04 / 106.94 | 1.33 | 22.22（PIN 250.00 / PM折D 22.22） | 208.27 | 198.04 | -10.23 | -4.91% | 0.045 |
| GIANTX vs Karmine Corp (BO3) LEC | 全场胜负 | Pinnacle / GIANTX 胜 / +407 / 5.070 / 100.00 | Polymarket / GIANTX NO（买 Karmine Corp YES） / 0.850 / 507.00 / 430.95 | 2.75 | 1983.44（PIN 2500.00 / PM折D 1983.44） | 533.70 | 507.00 | -26.70 | -5.00% | 0.047 |
| paiN Gaming Academy vs Ei Nerd Esports (BO3) Circuito Desafiante | 总局数 O/U 2.5 | Pinnacle / Under 2.5 / -131 / 1.763 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.480 / 176.34 / 84.64 | 1.06 | 250.00（PIN 250.00 / PM折D 442.77） | 185.70 | 176.34 | -9.36 | -5.04% | 0.047 |
| Natus Vincere vs Team Heretics (BO3) LEC | 全场胜负 | Pinnacle / Heretics 胜 / +181 / 2.810 / 100.00 | Polymarket / Team Heretics NO（买 Natus Vincere YES） / 0.690 / 281.00 / 193.89 | 2.07 | 1031.26（PIN 2500.00 / PM折D 1031.26） | 295.96 | 281.00 | -14.96 | -5.06% | 0.046 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 总局数 O/U 4.5 | Pinnacle / Over 4.5 / +166 / 2.660 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.670 / 266.00 / 178.22 | 1.97 | 137.22（PIN 375.00 / PM折D 137.22） | 280.19 | 266.00 | -14.19 | -5.06% | 0.046 |
| Natus Vincere vs Team Heretics (BO3) LEC | Game 1 胜负 | Pinnacle / Heretics G1 / +146 / 2.460 / 100.00 | Polymarket / Team Heretics G1 NO（买 Natus Vincere G1 YES） / 0.640 / 246.00 / 157.44 | 1.81 | 1250.00（PIN 1250.00 / PM折D 1543.52） | 259.25 | 246.00 | -13.25 | -5.11% | 0.046 |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | 全场胜负 | Pinnacle / Dplus KIA Challengers 胜 / -178 / 1.562 / 100.00 | Polymarket / Dplus KIA Challengers NO（买 KT Rolster Challengers YES） / 0.410 / 156.18 / 64.03 | 0.77 | 1000.00（PIN 1000.00 / PM折D 2183.46） | 164.81 | 156.18 | -8.63 | -5.24% | 0.050 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 总局数 O/U 4.5 | Pinnacle / Under 4.5 / -235 / 1.425 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.350 / 142.55 / 49.89 | 0.57 | 55.42（PIN 375.00 / PM折D 55.42） | 150.46 | 142.55 | -7.91 | -5.26% | 0.051 |
| Dplus KIA Challengers vs KT Rolster Challengers (BO3) LCK CL | 让分 -1.5/+1.5 | Pinnacle / Dplus KIA Challengers -1.5 / +171 / 2.710 / 100.00 | Polymarket / Dplus KIA Challengers -1.5 NO（买 KT Rolster Challengers +1.5 YES） / 0.680 / 271.00 / 184.28 | 2.00 | 790.56（PIN 1000.00 / PM折D 790.56） | 286.29 | 271.00 | -15.29 | -5.34% | 0.049 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 总局数 O/U 3.5 | Pinnacle / Under 3.5 / +194 / 2.940 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.710 / 294.00 / 208.74 | 2.15 | 127.55（PIN 375.00 / PM折D 127.55） | 310.89 | 294.00 | -16.89 | -5.43% | 0.050 |
| GIANTX vs Karmine Corp (BO3) LEC | 让分 +1.5/-1.5 | Pinnacle / GIANTX +1.5 / +122 / 2.220 / 100.00 | Polymarket / GIANTX +1.5 NO（买 Karmine Corp -1.5 YES） / 0.600 / 222.00 / 133.20 | 1.60 | 1043.57（PIN 2500.00 / PM折D 1043.57） | 234.80 | 222.00 | -12.80 | -5.45% | 0.051 |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | Game 1 胜负 | Pinnacle / Hanwha Life Challengers G1 / +127 / 2.270 / 100.00 | Polymarket / Hanwha Life Esports Challengers G1 NO（买 Kiwoom DRX Challengers G1 YES） / 0.610 / 227.00 / 138.47 | 1.65 | 125.00（PIN 125.00 / PM折D 546.65） | 240.12 | 227.00 | -13.12 | -5.46% | 0.051 |
| 3v Team vs LYON Academy (BO5) LRN | 总局数 O/U 3.5 | Pinnacle / Over 3.5 / -158 / 1.633 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.440 / 163.29 / 71.85 | 0.89 | 33.71（PIN 125.00 / PM折D 33.71） | 172.73 | 163.29 | -9.44 | -5.47% | 0.052 |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | 让分 -1.5/+1.5 | Pinnacle / Hanwha Life Challengers +1.5 / -217 / 1.461 / 100.00 | Polymarket / Hanwha Life Esports Challengers +1.5 NO（买 Kiwoom DRX Challengers -1.5 YES） / 0.370 / 146.08 / 54.05 | 0.63 | 250.00（PIN 250.00 / PM折D 586.22） | 154.68 | 146.08 | -8.60 | -5.56% | 0.054 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 让分 +1.5/-1.5 | Pinnacle / T1 +1.5 / -146 / 1.685 / 100.00 | Polymarket / T1 +1.5 NO（买 DN SOOPers -1.5 YES） / 0.460 / 168.49 / 77.51 | 0.96 | 124.63（PIN 500.00 / PM折D 124.63） | 178.47 | 168.49 | -9.98 | -5.59% | 0.053 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 总局数 O/U 3.5 | Pinnacle / Over 3.5 / -314 / 1.319 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.300 / 131.85 / 39.55 | 0.42 | 52.66（PIN 375.00 / PM折D 52.66） | 139.97 | 131.85 | -8.12 | -5.80% | 0.059 |
| 3v Team vs LYON Academy (BO5) LRN | 总局数 O/U 4.5 | Pinnacle / Under 4.5 / -457 / 1.219 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.240 / 121.88 / 29.25 | 0.27 | 19.49（PIN 125.00 / PM折D 19.49） | 129.52 | 121.88 | -7.64 | -5.90% | 0.060 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 让分 -2.5/+2.5 | Pinnacle / DN SOOPers +2.5 / -1421 / 1.070 / 100.00 | Polymarket / DN SOOPers +2.5 NO（买 T1 -2.5 YES） / 0.130 / 107.04 / 13.91 | 0.08 | 500.00（PIN 500.00 / PM折D 619.83） | 113.99 | 107.04 | -6.96 | -6.10% | 0.064 |
| 3v Team vs LYON Academy (BO5) LRN | 总局数 O/U 3.5 | Pinnacle / Under 3.5 / +118 / 2.180 / 100.00 | Polymarket / Under NO（买 Over YES） / 0.600 / 218.00 / 130.80 | 1.57 | 69.66（PIN 125.00 / PM折D 69.66） | 232.37 | 218.00 | -14.37 | -6.18% | 0.059 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 全场胜负 | Pinnacle / DN SOOPers 胜 / -182 / 1.550 / 100.00 | Polymarket / DN SOOPers NO（买 T1 YES） / 0.420 / 154.95 / 65.08 | 0.79 | 500.00（PIN 500.00 / PM折D 1791.74） | 165.87 | 154.95 | -10.92 | -6.59% | 0.065 |
| T1 vs DN SOOPers (BO5) KeSPA Cup | 让分 +2.5/-2.5 | Pinnacle / T1 +2.5 / -531 / 1.188 / 100.00 | Polymarket / T1 +2.5 NO（买 DN SOOPers -2.5 YES） / 0.230 / 118.83 / 27.33 | 0.24 | 41.23（PIN 500.00 / PM折D 41.23） | 127.57 | 118.83 | -8.74 | -6.85% | 0.071 |
| Kiwoom DRX Challengers vs Hanwha Life Challengers (BO3) LCK CL | 全场胜负 | Pinnacle / Hanwha Life Challengers 胜 / +146 / 2.460 / 100.00 | Polymarket / Hanwha Life Esports Challengers NO（买 Kiwoom DRX Challengers YES） / 0.660 / 246.00 / 162.36 | 1.82 | 250.00（PIN 250.00 / PM折D 1336.59） | 264.18 | 246.00 | -18.18 | -6.88% | 0.067 |
| 3v Team vs LYON Academy (BO5) LRN | 让分 +1.5/-1.5 | Pinnacle / LYON Academy +1.5 / +198 / 2.980 / 100.00 | Polymarket / LYON Academy +1.5 NO（买 3v Team -1.5 YES） / 0.740 / 298.00 / 220.52 | 2.12 | 3.72（PIN 1000.00 / PM折D 3.72） | 322.64 | 298.00 | -24.64 | -7.64% | 0.076 |
| 3v Team vs LYON Academy (BO5) LRN | 总局数 O/U 4.5 | Pinnacle / Over 4.5 / +249 / 3.490 / 100.00 | Polymarket / Over NO（买 Under YES） / 0.800 / 349.00 / 279.20 | 2.23 | 43.52（PIN 125.00 / PM折D 43.52） | 381.43 | 349.00 | -32.43 | -8.50% | 0.086 |
| 3v Team vs LYON Academy (BO5) LRN | 让分 +1.5/-1.5 | Pinnacle / 3v -1.5 / -279 / 1.358 / 100.00 | Polymarket / 3v Team -1.5 NO（买 LYON Academy +1.5 YES） / 0.540 / 135.84 / 73.35 | 0.91 | 11.04（PIN 1000.00 / PM折D 11.04） | 174.27 | 135.84 | -38.42 | -22.05% | 0.276 |

说明：唯一费后微正是「PIN 买 DRX.C 胜 @−181（1.552）+ PM 买 HLE.C YES @0.35」，每 100 博彩本金约 +0.29 USDT（+0.19%），深度受 PIN 限额 250 封顶。**远低于 1.5%，且规则不一致，不升格。**

## 表5 结论

| 项 | 内容 |
|---|---|
| 有没有套利 | **没有**高价值套利（费后净 ≥1.5% 且能立刻吃、规则基本一致 = 0） |
| 最接近 | 1）LCK CL DRX.C vs HLE.C 全场：PIN DRX −181 + PM HLE YES 0.35，费后 +0.19%，要转正已过 0.006，但 fee 几乎吃光，限额 250。2）KeSPA T1 胜 +147 + PM DNS YES 0.59，费前已过转正 0.005，费后 −0.20%；ask 大约还要再降到 ~0.587 才费后打平。3）其余胜负/让分/大小费后 −1.1% 到 −8% |
| 盯哪条 | 写入小时报，与 Dota 同一套：优先盯 **DRX.C 胜负**（PM HLE ask 若 ≤0.33 或 PIN DRX 短于 −175）和 **T1 胜负**（PM DNS ask 若 ≤0.57 或 PIN T1 长于 +155）。其次 LEC NAVI / GX-KC 开赛前价差。不要盯 Stake/Duel，直到接口恢复 |
| 和 Dota 一样写入小时报 | **是**。LoL 今日有 7 场可双边成交（Dota 今日 PIN 冠军期货已关、只有八强）。小时报应并列：Dota TI 八强 + 本表 7 场 LoL。高价值栏两边目前都是「无」 |
| 不要做什么 | 不要下单。不要把 Stake/Duel 缺口补成旧新闻赔率。不要把 PIN 已关闭期货当现价（本轮 7 场都是 open，可用）。不要把 PM 趣味盘（Baron/龙/Penta）当对冲腿 |
| 规则 | 全部路径降级。一边 50-50、一边 void 会裂开 |

本表只做定价差记录，不是下单建议。

---

## 本次请求成功 / 失败

| 结果 | 方法 | URL | HTTP | 备注 |
|---|---|---|---|---|
| 成功 | GET | https://gamma-api.polymarket.com/public-search?q=League+of+Legends&limit_per_type=50&events_status=active | 200 | 50 事件 / totalResults=174 |
| 成功 | GET | https://gamma-api.polymarket.com/public-search?q=Worlds&limit_per_type=50&events_status=active | 200 | 3 事件（含 Worlds 2026 Winning Region） |
| 成功 | GET | https://gamma-api.polymarket.com/public-search?q=LPL&limit_per_type=50&events_status=active | 200 | 35 事件 |
| 成功 | GET | https://gamma-api.polymarket.com/public-search?q=LCK&limit_per_type=50&events_status=active | 200 | 33 事件 |
| 成功 | GET | https://gamma-api.polymarket.com/public-search?q=LEC&limit_per_type=50&events_status=active | 200 | 23 事件（含足球 Lecce 噪音） |
| 成功 | GET | https://gamma-api.polymarket.com/public-search?q=MSI&limit_per_type=50&events_status=active | 200 | 0 事件 |
| 成功 | GET | https://gamma-api.polymarket.com/public-search?q=LoL&limit_per_type=50&events_status=active | 200 | 50 事件 / totalResults=173 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-dkc-ktc-2026-08-17 | 200 | 23 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-drxc-hle-2026-08-17 | 200 | 23 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-navi-th-2026-08-17 | 200 | 29 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-gx-kc-2026-08-17 | 200 | 29 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-t1-dnf-2026-08-17 | 200 | 41 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-3v-lyna-2026-08-17 | 200 | 39 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-pnga-nerd-2026-08-17 | 200 | 23 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-worlds-2026-winning-region-226 | 200 | 7 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-lpl-2026-season-winner | 200 | 42 盘 |
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=lol-lck-2026-season-winner | 200 | 37 盘 |
| 成功 | GET | https://clob.polymarket.com/book?token_id=… | 200×90 | 7 场胜负/让分/大小/G1 共 90 个 token，全部 200 |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/sports | 200 | E Sports id=12 |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/sports/12/leagues?all=false | 200 | 11 联赛，LoL 5 条 |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/sports/12/matchups | 200 | 114 条 |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/211515/matchups + markets/straight | 200 | LCK CL |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/196921/matchups + markets/straight | 200 | LEC |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/192181/matchups + markets/straight | 200 | KeSPA |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/288709/matchups + markets/straight | 200 | LRN |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/262934/matchups + markets/straight | 200 | Circuito Desafiante |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/sports/12/markets/straight | 200 | 全电竞 straight |
| 成功 | GET | https://www.pinnacle.com/en/future/betting-rules | 200 | 读到 Esports + LoL 专项 |
| 成功 | POST | https://stake.us/_api/graphql handshake | 200 | __typename=Query |
| 成功 | POST | https://stake.us/_api/graphql slugSport(league-of-legends/esports) | 200 | errorType=serviceDisabled |
| 成功 | POST | https://stake.us/_api/graphql allSportBets | 200 | 数组空 |
| 失败/空 | GET | https://duel.com/api/v2/metadata | 403 | CF/挑战页（本次；文档里早些时候曾 200） |
| 失败/空 | GET | https://duel.com/api/v2/match-betting | 403/WebFetch挑战 | 产品级关闭 + 美国 IP；文档：Match betting is temporarily disabled |
| 失败/空 | POST | https://duel.com/api/v2/match-betting/betby/user-session/en/USD/false | 未再打通 | 历史：403 IP or Country blocked。本次不编价 |
| 失败/空 | GET | https://sports-proxy.duel.com/ | 403 | {"error":"access blocked"} 30B |
| 失败/空 | GET | https://duel.com/sports | 需网页 | Betby iframe，无公开赔率 JSON |
| 失败/空 | POST | https://stake.com/_api/graphql | 403 | Cloudflare Just a moment |
| 失败/空 | GET | https://stake.com/sports/esports/league-of-legends | WebFetch 挑战页 | 未读到盘口 DOM 价 |
| 失败/空 | POST | https://stake.us/_api/graphql sportFixtureQuery | 400 | schema 要 inline fragment，体育后端仍 disabled |
| 失败/空 | GET | https://guest.api.arcadia.pinnacle.com/0.1/sports/12/leagues?all=true | 未本轮重打 | 历史 401 |
| 失败/空 | — | Pinnacle LPL / LCK 主联赛 / Worlds | 无联赛 | sports/12/leagues?all=false 11 条里没有 |
| 失败/空 | — | Stake.us 真钱电竞 | 无 | stake.us 体育 serviceDisabled；不要用 stake.us 当国际站 |

落盘：`/workspace/arb-radar/lol-markets.json` ；`/workspace/arb-radar/lol-report.md`