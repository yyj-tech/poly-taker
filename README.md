# poly-taker

Polymarket 跨市场套利监控（只读分析，不下单）。

Read-only cross-market arb monitor. Analysis only — no order placement.

## 还剩什么 / What remains

- `arb-radar/apis/` — 可复用的赔率客户端（odds-api.io / Stake / Duel / 聚合）
- `arb-radar-web/` — Express 只读看板：Polymarket + Pinnacle + Stake/Duel
- `arb-radar-web/JP-PROXY.md` — 日本中转代理运维说明（看板出站）
- `arb-radar-web/BUILD.md` / `DEPLOY.md` — 本地启动与部署

没有通用的 `write_watch.py`：原先那份以及所有 `write_watch_*.py` 都是单场盯盘一次性脚本，不是可维护入口。看板本身就是监控入口。

There is no generic Python watch entrypoint. Timed `write_watch_*` clones and `write_watch.py` were match-specific one-shots and were removed. The web dashboard is the maintained monitor.

## 已剥离 / Stripped

历史扫描、小时报告、盯盘 JSON/Markdown、截图、实验性下单页（`order-v1.html`）和 ticket 图都已从仓库删除，不再随代码分发。

Historical hourly dumps, snapshot JSON/Markdown, screenshots, the unused experimental order page, and ticket images were removed.

## 说明

- 只查数据、汇总机会，永不自动下单
- `keys.json` 已 gitignore；只提交 `arb-radar-web/data/keys.example.json`
- 本地密钥与 `scans/` 抓取目录不要入库

## 看板启动

```
cd arb-radar-web
npm install
npm start
# http://127.0.0.1:8787
```
