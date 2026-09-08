# poly-monitor

Polymarket 跨市场套利监控（数据汇总，不下单）。

## 目录

- `arb-radar/` — 扫描脚本、盯盘输出、API 客户端
- `arb-radar-web/` — 简易监控网页（若已包含）

## 说明

- 只查数据、汇总机会，永不自动下单
- 上传时已排除 `scans/` 原始抓取与本地密钥文件
