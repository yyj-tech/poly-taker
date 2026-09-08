# 套利雷达刷新

快照：2026-08-17 13:40 CST（Asia/Shanghai）
原则：只写本次请求到的数字；Stake/Duel 接口仍墙，网页价沿用 13:32 并标注；不下单；不编价。
公式：左博彩 D=100、欧赔 O；右 PM 买对立面 YES ask p，份数=D×O；fee=花费×0.05×p×(1-p)；利润=D×O−D−p×D×O−fee。转正：p<1−1/O。
高价值：费后净≥1.5% 且能立刻吃且规则一致。PM 14天/50-50 vs PIN 30h void → 即使微正也不升格。

## 表1 概览

| 时间 | Dota高价值 | LoL高价值 | 最接近 | 数据新鲜度 |
|---|---|---|---|---|
| 2026-08-17 13:40 CST | 0 | 0 | T1 vs DN SOOPers (BO5) KeSPA / Pinnacle T1 胜 费后 +0.64% | PM Gamma 22/22 事件 200；CLOB book 成功 1018 失败 86；PIN guest API 成功 15 失败 0（联赛/对阵/straight 全 200）；Stake.com GraphQL 403；stake.us 握手 200 但体育 serviceDisabled；Duel metadata/match-betting/session/proxy 全 403。Stake/Duel 价沿用网页价时刻 13:32，可能旧。 |

## 表2 高价值

| 事件 | 盘种 | 左 | 右 | 深度 | 投入 | 收回 | 费后% | 要转正 |
|---|---|---|---|---|---|---|---|---|
| （空） |  |  |  |  |  |  |  | 无费后≥1.5%且规则一致的路径 |

## 表3 潜在/最接近仓位

只留费后 > −3% 或比上轮明显变好。按费后排序。左本金按 100；深度列为可执行 D。Stake/Duel 为网页价时刻 13:32，可能旧。

| 事件 | 盘种 | 左（平台/方向/美式/欧赔/金额） | 右（平台/方向/ask/份数/花费） | fee | 深度 | 投入 | 收回 | 费后% | 要转正 |
|---|---|---|---|---:|---|---:|---:|---:|---|
| T1 vs DN SOOPers (BO5) KeSPA | 全场胜负 | Pinnacle / T1 胜 / +140 / 2.400 / 100 | PM / PM 买 DNS YES / 0.570 / 240.0 / 136.80 | 1.68 | 500.0 | 238.48 | 240.00 | +0.64% | 已转正（费前 -0.013） |
| TEAM VISION vs BoomBoys (BO3) TI 八强 | 全场胜负 | Pinnacle / VISION 胜 / -366 / 1.273 / 100 | PM / PM 买 BoomBoys YES / 0.210 / 127.3 / 26.74 | 0.22 | 105.8 | 126.96 | 127.32 | +0.29% | 已转正（费前 -0.005） |
| DRX.C vs HLE.C (BO3) LCK CL | 全场胜负 | Pinnacle / DRX.C 胜 / -183 / 1.546 / 100 | PM / PM 买 HLE.C YES / 0.350 / 154.6 / 54.13 | 0.62 | 250.0 | 154.74 | 154.64 | -0.06% | 已转正（费前 -0.003） |
| T1 vs DN SOOPers (BO5) KeSPA | 让分 1.5 | Pinnacle / DNS -1.5 / +125 / 2.250 / 100 | PM / PM 买 T1 +1.5 YES / 0.550 / 225.0 / 123.75 | 1.53 | 274.3 | 225.28 | 225.00 | -0.12% | 已转正（费前 -0.006） |
| NAVI vs Team Heretics (BO3) LEC | 让分 1.5 | Pinnacle / NAVI -1.5 / +141 / 2.410 / 100 | PM / PM 买 Heretics +1.5 YES / 0.580 / 241.0 / 139.78 | 1.70 | 1986.3 | 241.48 | 241.00 | -0.20% | 已转正（费前 -0.005） |
| Nigma Galaxy vs Team Falcons (BO3) TI 八强 | 全场胜负 | Pinnacle / Falcons 胜 / -185 / 1.541 / 100 | PM / PM 买 NGX YES / 0.350 / 154.1 / 53.92 | 0.61 | 300.0 | 154.53 | 154.05 | -0.31% | 已转正（费前 -0.001） |
| GIANTX vs Karmine Corp (BO3) LEC | 全场胜负 | Duel / Karmine 胜 / — / 1.180 / 100 | PM / PM 买 GIANTX YES / 0.160 / 118.0 / 18.88 | 0.13 | 1978.8 ·13:32网页 | 119.01 | 118.00 | -0.85% | 0.007 |
| Team Liquid vs Team Yandex (BO3) TI 八强 | 全场胜负 | Pinnacle / Yandex 胜 / +121 / 2.210 / 100 | PM / PM 买 Liquid YES / 0.550 / 221.0 / 121.55 | 1.50 | 300.0 | 223.05 | 221.00 | -0.92% | 0.002 |
| Gen.G vs KT Rolster (BO3) LCK | 全场胜负 | Duel / Gen.G 胜 / — / 1.250 / 100 | PM / PM 买 KT Rolster YES / 0.210 / 125.0 / 26.25 | 0.22 | 853.1 ·13:32网页 | 126.47 | 125.00 | -1.16% | 0.010 |
| Nigma Galaxy vs Team Falcons (BO3) TI 八强 | Game 1 胜负 | Pinnacle / NGX G1 / +130 / 2.300 / 100 | PM / PM 买 Team Falcons G1 YES / 0.570 / 230.0 / 131.10 | 1.61 | 6.6 | 232.71 | 230.00 | -1.16% | 0.005 |
| T1 vs DN SOOPers (BO5) KeSPA | 全场胜负 | Stake / T1 胜 / — / 2.300 / 100 | PM / PM 买 DN SOOPers YES / 0.570 / 230.0 / 131.10 | 1.61 | 1136.4 ·13:32网页 | 232.71 | 230.00 | -1.16% | 0.005 |
| TEAM VISION vs BoomBoys (BO3) TI 八强 | Game 1 胜负 | Pinnacle / VISION G1 / -245 / 1.408 / 100 | PM / PM 买 BoomBoys G1 YES / 0.300 / 140.8 / 42.24 | 0.44 | 150.0 | 142.69 | 140.82 | -1.31% | 0.010 |
| LGD vs BLG (BO3) LPL | 全场胜负 | Duel / BLG 胜 / — / 1.230 / 100 | PM / PM 买 LGD Gaming YES / 0.200 / 123.0 / 24.60 | 0.20 | 870.8 ·13:32网页 | 124.80 | 123.00 | -1.44% | 0.013 |
| WE vs EDG (BO3) LPL | 全场胜负 | Duel / EDG 胜 / — / 4.800 / 100 | PM / PM 买 Team WE YES / 0.800 / 480.0 / 384.00 | 3.07 | 7.3 ·13:32网页 | 487.07 | 480.00 | -1.45% | 0.008 |
| DRX.C vs HLE.C (BO3) LCK CL | Game 1 胜负 | Pinnacle / DRX.C G1 / -157 / 1.637 / 100 | PM / PM 买 HLE.C G1 YES / 0.400 / 163.7 / 65.48 | 0.79 | 125.0 | 166.26 | 163.69 | -1.55% | 0.011 |
| LNG vs Weibo (BO3) LPL | 全场胜负 | Duel / LNG 胜 / — / 4.000 / 100 | PM / PM 买 Weibo Gaming YES / 0.760 / 400.0 / 304.00 | 2.77 | 18.8 ·13:32网页 | 406.77 | 400.00 | -1.66% | 0.010 |
| DK.C vs KT.C (BO3) LCK CL | 全场胜负 | Pinnacle / KT.C 胜 / +144 / 2.440 / 100 | PM / PM 买 DK.C YES / 0.600 / 244.0 / 146.40 | 1.76 | 1000.0 | 248.16 | 244.00 | -1.68% | 0.010 |
| NAVI vs Team Heretics (BO3) LEC | Game 1 胜负 | Pinnacle / NAVI G1 / -180 / 1.556 / 100 | PM / PM 买 Team Heretics G1 YES / 0.370 / 155.6 / 57.56 | 0.67 | 3.2 | 158.23 | 155.56 | -1.69% | 0.013 |
| DK.C vs KT.C (BO3) LCK CL | 让分 1.5 | Pinnacle / KT.C +1.5 / -216 / 1.463 / 100 | PM / PM 买 DK.C -1.5 YES / 0.330 / 146.3 / 48.28 | 0.53 | 114.9 | 148.81 | 146.30 | -1.69% | 0.014 |
| DRX.C vs HLE.C (BO3) LCK CL | 让分 1.5 | Pinnacle / DRX.C -1.5 / +170 / 2.700 / 100 | PM / PM 买 HLE.C YES（对立让分） / 0.640 / 270.0 / 172.80 | 1.99 | 250.0 | 274.79 | 270.00 | -1.74% | 0.010 |
| NAVI vs Team Heretics (BO3) LEC | 全场胜负 | Duel / NAVI 胜 / — / 1.440 / 100 | PM / PM 买 Team Heretics YES / 0.320 / 144.0 / 46.08 | 0.50 | 6145.6 ·13:32网页 | 146.58 | 144.00 | -1.76% | 0.014 |
| Iron Wing vs Team Spirit (BO3) TI 八强 | 全场胜负 | Pinnacle / Spirit 胜 / -110 / 1.909 / 100 | PM / PM 买 Iron Wing YES / 0.490 / 190.9 / 93.55 | 1.17 | 300.0 | 194.71 | 190.91 | -1.95% | 0.014 |
| NAVI vs Team Heretics (BO3) LEC | 全场胜负 | Pinnacle / NAVI 胜 / -230 / 1.435 / 100 | PM / PM 买 Heretics YES / 0.320 / 143.5 / 45.91 | 0.50 | 2500.0 | 146.41 | 143.48 | -2.00% | 0.017 |
| Nongshim vs Kiwoom DRX (BO3) LCK | 全场胜负 | Duel / DRX 胜 / — / 2.360 / 100 | PM / PM 买 Nongshim Red Force YES / 0.590 / 236.0 / 139.24 | 1.68 | 88.5 ·13:32网页 | 240.92 | 236.00 | -2.04% | 0.014 |
| Nigma Galaxy vs Team Falcons (BO3) TI 八强 | 总局数 O/U 2.5 | Pinnacle / Under 2.5 / -125 / 1.800 / 100 | PM / PM 买 Over YES / 0.460 / 180.0 / 82.80 | 1.03 | 19.4 | 183.83 | 180.00 | -2.08% | 0.016 |
| T1 vs DN SOOPers (BO5) KeSPA | Game 1 胜负 | Pinnacle / DNS G1 / -136 / 1.735 / 100 | PM / PM 买 T1 G1 YES / 0.440 / 173.5 / 76.35 | 0.94 | 207.6 | 177.29 | 173.53 | -2.12% | 0.016 |
| TI2026 冠军盘 | 冠军 | Duel / Team Yandex 夺冠 / — / 9.000 / 100 | PM / PM 买 Team Yandex NO / 0.909 / 900.0 / 818.10 | 3.38 | 55.6 ·13:32网页 | 921.48 | 900.00 | -2.33% | 0.020 |
| Dplus KIA vs HLE (BO3) LCK | 全场胜负 | Duel / HLE 胜 / — / 1.850 / 100 | PM / PM 买 Dplus KIA YES / 0.480 / 185.0 / 88.80 | 1.11 | 22.2 ·13:32网页 | 189.91 | 185.00 | -2.58% | 0.021 |
| BRION vs DN SOOPers (BO3) LCK | 全场胜负 | Duel / BRION 胜 / — / 1.920 / 100 | PM / PM 买 DN SOOPers YES / 0.500 / 192.0 / 96.00 | 1.20 | 60.4 ·13:32网页 | 197.20 | 192.00 | -2.64% | 0.021 |
| GIANTX vs Karmine Corp (BO3) LEC | 全场胜负 | Pinnacle / Karmine 胜 / -649 / 1.154 / 100 | PM / PM 买 GIANTX YES / 0.160 / 115.4 / 18.47 | 0.12 | 2023.3 | 118.59 | 115.41 | -2.68% | 0.026 |
| NAVI vs Team Heretics (BO3) LEC | 全场胜负 | Stake / NAVI 胜 / — / 1.420 / 100 | PM / PM 买 Team Heretics YES / 0.320 / 142.0 / 45.44 | 0.49 | 6232.2 ·13:32网页 | 145.93 | 142.00 | -2.70% | 0.024 |
| DRX.C vs HLE.C (BO3) LCK CL | 全场胜负 | Stake / DRX.C 胜 / — / 1.480 / 100 | PM / PM 买 HLE.C YES / 0.350 / 148.0 / 51.80 | 0.59 | 621.6 ·13:32网页 | 152.39 | 148.00 | -2.88% | 0.026 |
| DK.C vs KT.C (BO3) LCK CL | Game 1 胜负 | Pinnacle / DK.C G1 / -153 / 1.654 / 100 | PM / PM 买 KT Rolster Challengers G1 YES / 0.420 / 165.4 / 69.45 | 0.85 | 500.0 | 170.30 | 165.36 | -2.90% | 0.025 |
| AL vs TES (BO3) LPL | 全场胜负 | Duel / TES 胜 / — / 2.160 / 100 | PM / PM 买 Anyone's Legend YES / 0.560 / 216.0 / 120.96 | 1.49 | 638.5 ·13:32网页 | 222.45 | 216.00 | -2.90% | 0.023 |
| T1 vs DN SOOPers (BO5) KeSPA | 让分 2.5 | Pinnacle / DNS -2.5 / +328 / 4.280 / 100 | PM / PM 买 T1 +2.5 YES / 0.790 / 428.0 / 338.12 | 2.80 | 0.9 | 440.92 | 428.00 | -2.93% | 0.024 |
| GIANTX vs Karmine Corp (BO3) LEC | 全场胜负 | Stake / Karmine 胜 / — / 1.150 / 100 | PM / PM 买 GIANTX YES / 0.160 / 115.0 / 18.40 | 0.12 | 2030.5 ·13:32网页 | 118.52 | 115.00 | -2.97% | 0.030 |

## 表4 相对上轮变化

| 事件 | 左 | 本轮费后 | 上轮费后 | 变化 | 评 |
|---|---|---:|---:|---:|---|
| T1 vs DNS 全场 | PIN T1 | +0.64% | -0.20% | +0.84pp | **变好（价）**：PIN +147→+140，PM DNS ask 0.59→0.57 |
| VISION vs BoomBoys 全场 | PIN VISION | +0.29% | 上轮约 -3.9% | 明显转正 | **变好（价）**：PIN VISION -461→-366，PM BoomBoys ask 仍 0.21，深度薄（ask 135 份） |
| Liquid vs Yandex 全场 | PIN Yandex | -0.92% | -1.66% | +0.74pp | 略好：PIN Yandex +120→+121；上轮 Dota 小时报 fee 口径更重，本轮统一为花费×0.05×p×(1-p) |
| NGX vs Falcons 全场 | PIN Falcons | -0.31% | -1.04% | +0.73pp | **价几乎没变**（仍 -185 / PM NGX 0.35）；差额主要是 fee 口径对齐 LoL 上轮表 |
| Iron Wing vs Spirit 全场 | PIN Spirit | -1.95% | -2.56% | +0.61pp | 价仍 -110 / PM Iron Wing 0.49；差额主要是 fee 口径 |
| DK.C vs KT.C 全场 | PIN KT.C | -1.68% | -1.68% | 0 | 持平（+144 / PM DK.C 0.60） |
| GX vs KC 全场 | PIN KC | -2.68% | -2.68% | 0 | 持平（-649 / PM GX 0.16） |
| NAVI vs TH 全场 | PIN NAVI | -2.00% | -2.00% | 0 | 持平（-230 / PM TH 0.32） |
| DRX.C vs HLE.C 全场 | PIN DRX.C | -0.06% | +0.19% | -0.25pp | **变差（价）**：PIN -181→-183，PM HLE.C 仍 0.35，费后由微正翻负 |
| VISION -1.5 / BoomBoys +1.5 | PIN BB +1.5 | -3.80% | -0.74% | -3.06pp | **变差（价）**：PIN BoomBoys +1.5 -102→-119，PM VISION -1.5 仍 0.49 |
| Duel LCK/LPL 主联赛 | Duel 网页+本次 CLOB | 最好 -0.85%（KC） | 上轮缺深度 | — | 新算。网页价时刻 13:32，可能旧；无左腿深度 |
| WBG vs IG (lol-wb-ig1-2026-08-16) | — | 已关 | 若上轮还开 | — | 8/16 已打完，主盘 accepting=false |
| PIN TI 冠军期货 1633296958 | — | 仍 closed | 已关 | 持平 | cutoff 仍 2026-08-13 13:00 CST |
| EDG vs JDG (lol-edg-jdg-2026-08-23) | PM 有 CLOB | 无左腿 | — | — | PIN 无 LPL；Duel 13:32 网页未列这场 |

## 表5 结论

| 项 | 内容 |
|---|---|
| 有没有套利 | **没有**高价值套利（费后≥1.5% 且规则一致且能立刻吃 = 0） |
| 盯什么 | 1）KeSPA T1 胜：PIN +140 + PM DNS YES 0.57，费后 +0.64%，限额 500；规则仍 14天/50-50 vs 30h void，不升格。DNS ask≤0.56 或 PIN T1≥+150 才更接近 1.5%。2）VISION 胜：PIN -366 + PM BoomBoys YES 0.21，费后 +0.29%，PM 深度约 135 份。3）DRX.C 上轮微正已翻负。4）Duel LCK/LPL 已对上本次 CLOB，网页价时刻 13:32 可能旧，先重抓再谈。5）TI 冠军仍单边。 |
| 不要做什么 | 不要下单。不要把 PIN 已关期货当现价。不要把 13:32 网页价当成此刻成交价。不要把趣味盘当对冲腿。 |

本表只做定价差记录，不是下单建议。

---

## 本次请求成功 / 失败

| 结果 | 方法 | URL | HTTP | 备注 |
|---|---|---|---|---|
| 成功 | GET | https://gamma-api.polymarket.com/events?slug=（22 个指定 slug 全 200） | 200 | TI冠军 + 4 场 Dota 八强（含 Iron Wing）+ 17 场 LoL（含 WBG-IG 已关主盘、EDG-JDG） |
| 成功 | GET | https://gamma-api.polymarket.com/public-search?q=T1+DN+SOOPers / 3v+LYON / paiN+Ei+Nerd / Iron+Wing+Spirit / DK+HLE / WBG+IG | 200 | slug 确认：lol-t1-dnf-2026-08-17、lol-3v-lyna-2026-08-17、lol-pnga-nerd-2026-08-17、dota2-ironwi-ts8-2026-08-19 |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/sports/12/leagues?all=false | 200 | 6185B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/sports/12/matchups | 200 | 338128B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/sports/12/markets/straight | 200 | 232129B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/5055/matchups | 200 | 28805B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/5055/markets/straight | 200 | 15780B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/211515/matchups | 200 | 12963B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/211515/markets/straight | 200 | 20419B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/196921/matchups | 200 | 181979B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/196921/markets/straight | 200 | 77263B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/192181/matchups | 200 | 11382B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/192181/markets/straight | 200 | 32434B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/288709/matchups | 200 | 11442B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/288709/markets/straight | 200 | 16753B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/262934/matchups | 200 | 9488B |
| 成功 | GET | https://guest.api.arcadia.pinnacle.com/0.1/leagues/262934/markets/straight | 200 | 21352B |
| 成功 | POST | https://stake.us/_api/graphql 握手 | 200 | __typename=Query；slugSport(lol/dota-2) 回 serviceDisabled，无赔率 |
| 失败/空 | POST | https://stake.com/_api/graphql | 403 | <!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title><meta htt |
| 失败/空 | GET | https://duel.com/api/v2/metadata | 403 | <!DOCTYPE html> <html>    <head>       <meta charset="utf-8">       <title>IP or |
| 失败/空 | GET | https://duel.com/api/v2/match-betting | 403 | <!DOCTYPE html> <html>    <head>       <meta charset="utf-8">       <title>IP or |
| 失败/空 | GET | https://sports-proxy.duel.com/ | 403 | {  "error": "access blocked" } |
| 失败/空 | POST | https://duel.com/api/v2/match-betting/betby/user-session/en/USD/false | 403 | <!DOCTYPE html> <html>    <head>       <meta charset="utf-8">       <title>IP or |
| 成功 | GET | https://clob.polymarket.com/book?token_id=… | 200×1018 | 失败 86（多为已关/已结算 token，如淘汰队冠军、WBG-IG 已打完）；胜负/让分/大小/G1/冠军 YES+NO 活盘已用 |
| 沿用 | 网页 | Duel/Stake LoL+TI 冠军（上轮浏览器） | — | 网页价时刻 13:32，可能旧；本轮 API 仍 403/disabled，未编新价 |

落盘：`/workspace/arb-radar/latest-refresh.md` ；`/workspace/arb-radar/latest-refresh.json`
