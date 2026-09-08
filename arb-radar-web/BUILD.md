# BUILD

## path
/workspace/arb-radar-web

## start
cd /workspace/arb-radar-web
npm install
npm start
http://127.0.0.1:8787

## first-boot token

Generated on first start and written to `data/keys.json` (gitignored). Printed once in the startup log. Do not commit it.

## local source pull 2026-08-17 15:54 CST
- odds-api.io: OK, 45 Dota2/LoL events, Stake+Duel on watchlist except T1 vs DNS (no price).
- Pinnacle guest: OK no 401, 20 root matchups (TI 5055 + LEC + LCK CL + KeSPA). moneyline period=0, American->decimal.
- Polymarket: OK, 14 match-winner events, CLOB best ask (min ask, not mid).
- GET /api/snapshot with cookie: 14 price rows + 14 position rows.
- no cookie: 401. POST /api/login sets httpOnly cookie.
- GET /api/keys: configured last4=5560, pollSec, no full key.
- POST /api/keys pollSec 180 then 120: hot update OK.
- PIN vs PM marked rule-mismatch, not high-value.
- extras: OAI events with Stake/Duel that also match PIN or PM (cap ~20).

Read-only. No orders. Secret key copied at boot into data/keys.json only, not into README.

## deploy 2026-08-17 20:35 CST
public URL: http://8.153.173.192:8787
ECS /opt/arb-radar-web systemd arb-radar running HOST=0.0.0.0 PORT=8787
local curl 127.0.0.1:8787 = 200; public curl timed out (open Aliyun SG TCP 8787)
details: DEPLOY.md
