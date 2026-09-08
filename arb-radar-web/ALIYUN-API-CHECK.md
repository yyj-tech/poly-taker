# 阿里云 ECS 三家 API 连通性实测

- 机器：`8.153.173.192`（阿里云 ECS，hostname `iZuf6ercqt0o3tc3og6u7uZ`，时区 CST / Asia/Shanghai）
- 探测时间：2026-08-17 21:03–21:06 CST
- 方式：本机 paramiko SSH 到已授权 ECS，在远程 `curl`，不是本机猜的
- 出口 IP：`8.153.173.192`（`ifconfig.me` / `ipinfo.io/ip` 均返回该地址）
- `https://api.ipify.org`：连接被拒（curl 7，约 30–90ms），改用上面两个源
- 密钥：`/opt/arb-radar-web/data/keys.json` 的 `oddsApiIo` 长度 64，**last4=`5560`**（全文未打印）
- 无 HTTP/HTTPS 代理；IPv6 不通（`curl -6 https://ipv6.google.com` 立刻失败）

## 结果表

| 源 | HTTP码 | 耗时 | 能否用 | 备注 |
|---|---|---|---|---|
| 出口 IP（ifconfig.me） | 200 | <1s | 能 | 出口即 ECS 公网 `8.153.173.192` |
| 出口 IP（ipinfo.io/ip） | 200 | <1s | 能 | 同上 |
| 出口 IP（api.ipify.org） | 000 | ~0.03–0.09s | 否 | `Connection refused`，该探测站被拦，不影响结论 |
| odds-api.io `/v3/bookmakers`（无 key） | **000** | 15.001s | **否** | DNS 正常（`api.odds-api.io` → Railway `69.46.46.39`），TCP 443 **超时**。HTTP 明文同样 000/10s 超时 |
| odds-api.io `/v3/events?sport=esports&limit=5`（key last4 `5560`） | **000** | 20.000s | **否** | 同样连不上，未拿到 JSON，无法数 events / home/away |
| Pinnacle guest `/0.1/sports`（无 key） | **000** | 7.711s | **否** | `guest.api.arcadia.pinnacle.com` A=`174.37.154.236`，TCP 443 **超时**。不是 401 |
| Pinnacle guest `/0.1/sports/12/leagues?all=false`（无 key） | **000** | 7.701s | **否** | 同上，超时，未见 401 |
| Pinnacle sports（`X-API-Key` + 强制 IPv4） | **000** | 7.502s | **否** | 按约定 401 才带头重试；实际是超时，仍补测了带头请求，依旧连不上。看不到 E Sports / 联赛条数 |
| Pinnacle leagues sport=12（`X-API-Key` + IPv4） | **000** | 7.502s | **否** | 同上 |
| Polymarket gamma `/events?closed=false&limit=3` | **000** | 7.703s | **否** | `gamma-api.polymarket.com` A=`69.63.190.26`，TCP 443 **超时**。IPv4 强制同样 000/7.5s |
| Polymarket CLOB `https://clob.polymarket.com/` | **000** | 7.702s | **否** | A=`128.242.240.149`，TCP 443 **超时** |
| Polymarket gamma `/public-search?q=dota` | **000** | 7.702s | **否** | 同上，gamma 主机不可达 |
| 对照：baidu.com | 200 | 0.104s | 能 | 国内 HTTPS 正常 |
| 对照：api.github.com | 200 | 0.646s | 能 | 部分境外站可通 |
| 对照：www.google.com | 000 | 5.003s | 否 | 典型墙 |
| 对照：1.1.1.1（Cloudflare） | 000 | 10.002s | 否 | 境外常用 IP 也被拦 |

HTTP `000` = curl 未建立 TLS/HTTP（`Connection timed out` / `Connection refused`），不是业务 4xx/5xx。

## 看板进程侧（交叉验证，不是猜）

`arb-radar.service` **active (running)**，PID 108322，`/usr/bin/node src/server.js`，监听 `0.0.0.0:8787`。
最近一次重启：2026-08-17 **21:02:07 CST**。`pollSec=120`。

本机 `GET http://127.0.0.1:8787/api/snapshot`（用 keys.json 的 dashToken，未打印全文，last4=`2233`）：

| 源 | 看板 status | nEvents | error |
|---|---|---|---|
| oddsApiIo | 失败 | 0 | `fetch failed` |
| pinnacle | 失败 | 0 | `fetch failed` |
| polymarket | OK | 0 | 无（实现里单次 search/tag 失败被吞掉，最终仍标 OK；与 curl 超时一致，**实际不可用**） |

snapshot 时间：`2026-08-17 21:04:18 CST`。prices/positions 各 10 行（watchlist 空壳，无真实赔率）。

## journalctl -u arb-radar -n 40

无源失败日志。只有启动句：

```
Aug 17 21:02:07 ... systemd: Started arb-radar-web private dashboard.
Aug 17 21:02:08 ... node: 访问口令已存在（见 data/keys.json，不在此打印）
Aug 17 21:02:08 ... node: arb-radar-web http://0.0.0.0:8787
```

`journalctl -p err` 无条目。源错误只进 snapshot，不打 journal。

## 结论

三家都有实测 HTTP 结果，全部 **不能从这台上海 ECS 直连使用**：

1. **odds-api.io**：DNS 通，443 超时（被墙 / 运营商或安全组出站拦 Railway IP）
2. **Pinnacle guest**：DNS 通，443 超时；加 `X-API-Key` 也一样，**没碰到 401**
3. **Polymarket**（gamma + clob）：DNS 通，443 超时

国内站和 GitHub API 正常，Google / Cloudflare / 这三家 API 不行。要在这台机器跑套利看板，需要可访问这三家的出站通道（代理 / 境外中转 / 换区域），否则轮询会一直 `fetch failed` / 空事件。
