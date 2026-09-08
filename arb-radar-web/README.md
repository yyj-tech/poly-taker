# 套利雷达（私人看板）

本机 Express 只读. Polymarket ask + Pinnacle + Stake/Duel via odds-api.io.

实验性 `public/order-v1.html` 和下单 ticket 截图已删除（未接 server 路由，也不下单）。

## start
cd /workspace/arb-radar-web
npm install
npm start
http://127.0.0.1:8787

bind 127.0.0.1:8787. token in data/keys.json and startup log.
POST /api/keys hot-reloads odds-api.io key and pollSec.
GET /api/keys returns last4 only.

Sources: odds-api.io / Pinnacle guest / Polymarket CLOB ask.
Read-only. No orders. No Stake/Duel scraping. Do not commit real keys.

## 三数据源
1. Stake/Duel -> https://api.odds-api.io/v3
2. Pinnacle guest.api.arcadia.pinnacle.com (esports 12, TI 5055)
3. Polymarket Gamma + CLOB best ask (not mid)

设置页可热更新 key / pollSec / token.
只读扫描，不下单。
