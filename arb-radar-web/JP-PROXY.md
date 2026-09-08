# 日本中转代理

更新时间：2026-08-19 02:12 CST。

上海看板 **不再直连** 日本公网 `:80`。公网 `CONNECT`（尤其 Cloudflare 主机名）会被立刻 RST。可靠路径是 SSH 隧道：上海本机 `127.0.0.1:8888` → 日本本机 `127.0.0.1:80`（tinyproxy）。

## 日本机

- 地址：`8.209.244.243`（hostname `iZ6weei2bxum7h0grzvks1Z`）
- 系统：Ubuntu 24.04.2 LTS
- 只跑 tinyproxy，不跑 Node / nginx

日本本机直连（`curl -sS -m 15`）：

| 源 | HTTP | 结论 |
|---|---|---|
| https://api.odds-api.io/v3/bookmakers | **200** | 通 |
| https://guest.api.arcadia.pinnacle.com/0.1/sports | **403** | 网络通，Cloudflare 403 |
| https://gamma-api.polymarket.com/events?closed=false&limit=2 | **200** | 通 |

## 代理（日本 tinyproxy）

- 软件：tinyproxy 1.11.1，systemd `tinyproxy`（enabled）
- 监听：`0.0.0.0:80`（用户已放行 80；保持不动）
- `Listen 0.0.0.0`
- ACL：
  - `Allow 127.0.0.1`（SSH 隧道远端）
  - `Allow 8.153.173.192`（公网直连仍允许，但不给看板用）
- User/Group：`tinyproxy` / `tinyproxy`（root 起绑 80 后降权）
- 本机防火墙：INPUT 默认 ACCEPT
- 日本本机 `curl -x http://127.0.0.1:80`：odds-api.io **200**，polymarket **200**
- 配置：`/etc/tinyproxy/tinyproxy.conf`；旧 8888 备份：`/etc/tinyproxy/tinyproxy.conf.bak-8888`
- **日本 8888 已不再监听**

这是 **HTTP 正向代理**（CONNECT 隧道），不是 nginx 反代。

## 为什么不能上海直连日本 :80

上海 `curl -x http://8.209.244.243:80`（2026-08-19 01:46–01:50 CST）：

| 源 | 结果 | 说明 |
|---|---|---|
| https://odds-api.io / api.odds-api.io | **200**（间歇 RST） | CONNECT 成功时有真实 HTTP；连打几次后可能被 RST |
| https://gamma-api.polymarket.com | **RST**（~50–80ms） | tinyproxy 已对端建立 CONNECT，回客户端时 `Could not send SSL greeting to client` |
| Pinnacle guest | **RST**（同样） | 同上，Cloudflare 系 |

日本本机经 `:80` 拉 polymarket / pinnacle 正常（200 / 403）。问题在 **上海公网 → 日本:80 的 CONNECT 路径**，不是 tinyproxy 没起来。旧 8888 仍被云安全组挡住。

## 上海看板（当前）

- 代码：`/opt/arb-radar-web/src/proxy.js`（undici `ProxyAgent` + `setGlobalDispatcher`）
- systemd `jp-http-tunnel.service`（enabled）：
  - `ssh -N -i /root/.ssh/id_ed25519_jp ... -L 127.0.0.1:8888:127.0.0.1:80 root@8.209.244.243`
  - 远端是日本 **:80**（tinyproxy），不是旧的 :8888
- systemd `arb-radar.service`：
  - `After=` / `Wants=` `jp-http-tunnel.service`
  - `Environment=HTTP_PROXY=http://127.0.0.1:8888`
  - `Environment=HTTPS_PROXY=http://127.0.0.1:8888`
  - `Environment=NO_PROXY=127.0.0.1,localhost`
- 监听未改：`0.0.0.0:8787`（visa 的 nginx:80 / `127.0.0.1:8788` / `127.0.0.1:3000` 未动）
- journal：`fetch proxy: http://127.0.0.1:8888`，`arb-radar-web http://0.0.0.0:8787`

上海本机 `curl -x http://127.0.0.1:8888` 与 Node/undici（2026-08-19 02:11 CST）：

| 源 | HTTP | 结论 |
|---|---|---|
| https://api.odds-api.io/v3/bookmakers | **200** | 隧道通 |
| https://gamma-api.polymarket.com | **200** | 隧道修好了公网 RST |
| Pinnacle guest | **403** | 连上了（可接受；不是 RST/timeout） |

`POST /api/refresh` + `GET /api/snapshot`（本机 x-dash-token，口令未写入本文）时间 `2026-08-19 02:11:10 CST`：

| 源 | 结果 |
|---|---|
| oddsApiIo | 失败 **HTTP 429 日配额**（免费档 500/天，UTC 0 点=CST 08:00 重置）。代理已通；`/v3/bookmakers` 无需 key 为 200 |
| pinnacle | 失败 **HTTP 403**（已连上，Cloudflare 拦 guest） |
| polymarket | **OK**、nEvents=12，watchlist 有真实 pm 价（Iron Wing/GEN/VISION/Liquid/NGX） |

前端：`刷新赔率` → `POST /api/refresh`（`#btn-reload`），`/api/refresh` 存在，不是 JS 404。页面 `/` 与 `/app.js` 均为 200，登录 `/api/login` 200。

## odds-api.io 配额（刷新路径）

免费档 **100 req/h 且 500/天**。旧实现每次刷新打 `/v3/leagues` + 多条 `/v3/events` + `/odds/multi`，120s 轮询会几个小时打爆日配额，之后 Stake/Duel 全空。

2026-08-19 起 `src/sources/oddsApiIo.js`：

- 不再先打 `/v3/leagues`（那一次 429 会让整源失败）
- 单次 `/v3/events?sport=esports`，事件缓存 30 分钟，赔率缓存 4 分钟
- 成功结果落盘 `data/oai-cache.json`；429 时回吐上次成功盘（若有）
- UTC 0 点后应能再拉到 Stake/Duel；在此之前连上了也是 429，不是隧道问题

## 运维

```
# 上海
systemctl status arb-radar
systemctl status jp-http-tunnel   # 应为 active / enabled
journalctl -u arb-radar -n 30     # 应见 fetch proxy: http://127.0.0.1:8888
ss -lntp | grep -E '8787|8888'
curl -x http://127.0.0.1:8888 -sS -m 15 -o /dev/null -w "%{http_code}\n" https://api.odds-api.io/v3/bookmakers
curl -x http://127.0.0.1:8888 -sS -m 15 -o /dev/null -w "%{http_code}\n" "https://gamma-api.polymarket.com/events?closed=false&limit=2"

# 日本
systemctl status tinyproxy
ss -lntp | grep :80
tail -n 30 /var/log/tinyproxy/tinyproxy.log
curl -x http://127.0.0.1:80 -sS -m 15 -o /dev/null -w "%{http_code}\n" https://api.odds-api.io/v3/bookmakers
```

隧道密钥：上海 `/root/.ssh/id_ed25519_jp`（公钥在日本 authorized_keys）。unit 里不用密码。
