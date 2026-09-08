# arb-radar APIs

Read-only odds clients. No betting automation.

- `apis/odds_api_io.py` — Stake / Duel via odds-api.io（推荐；看板同源）
- `apis/odds_agg_client.py` — 第三方赔率聚合探测
- `apis/stake_client.py` / `apis/duel_client.py` — 直连只读客户端（文档见同目录 `*.md`）

Key：环境变量 `ODDS_API_IO_KEY`，或未入库的 `apis/.odds_api_io_key`。

```
python3 apis/odds_api_io.py
```

输出写到被 gitignore 的 `scans/`，不要提交。
