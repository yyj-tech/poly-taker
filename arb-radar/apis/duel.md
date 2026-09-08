# Duel 公开拉盘方法（2026-08-17 实测）

平台是 `duel.com`（Vue 3 + Vite SPA，不是 Next.js，没有 `__NEXT_DATA__`）。体育盘是 **Betby iframe**，不是 Duel 自研赔率库。只读公开盘。不要要用户密码、不要下单。

## 本次真实请求

| URL | 方法 | 结果 |
|---|---|---|
| https://duel.com | GET | 200，4585B SPA 壳，入口 JS `/assets/index-BQIzxYso.js` |
| https://duel.com/sports | GET | 200，同一壳（路由 `path: sports`） |
| https://duel.com/sportsbook /match-betting /betting /sports/esports/dota-2 | GET | 200，同一壳 |
| https://duel.com/assets/index-BQIzxYso.js | GET | 200，1.19MB，含 Betby 配置 |
| https://duel.com/assets/sports-fT7y-JGf.js | GET | 200，完整 Betby 组件 + session 调用 |
| https://duel.com/assets/sports-rules-BzX1ombu.js | GET | 200，规则页组件，读 `betby_rules_v20` |
| https://duel.com/api/v2/metadata | GET | **先 200 JSON**（约 27KB），随后被 429/挑战页限流 |
| https://duel.com/api/v2/games | GET | 先 200，后 429 |
| https://duel.com/api/v2/match-betting | GET | **403 JSON：`Match betting is temporarily disabled while we work on some updates.`**；随后 429 |
| https://duel.com/api/v2/match-betting/betby/user-session/en/USD/false | POST | 403 HTML「IP or Country blocked」；GET 404 |
| https://sports-proxy.duel.com/ | GET | 403 `{"error":"access blocked"}` |
| https://ui.invisiblesport.com/bt-renderer.min.js | GET | 200，但内容是 BTRenderer 403 错误页 |
| https://api.invisiblesport.com | GET | 503 `access blocked` |
| https://duel.com/sports-betting-rules | GET | 200 SPA 壳（规则正文在 i18n，未独立 JSON） |

## 真实内部接口（从 JS 拆出来）

Duel 自己的 HTTP 前缀是 `api/v2/`（axios `baseURL`）。体育盘只走这一条：

```
POST /api/v2/match-betting/betby/user-session/{lang}/{currency}/{displayInFiat}
```

源码（`sports-fT7y-JGf.js`）：

```js
var J = new P(`api/v2/match-betting/betby`)
re = (lang, currency, displayInFiat, nt, securityToken) => {
  let headers = nt ? { nt: `1` } : undefined
  return J.request(
    `user-session/${lang}/${currency}/${displayInFiat}`,
    `POST`,
    securityToken ? { security_token: securityToken } : null,
    null,
    headers,
  )
}
```

成功时应回 `{ token, libraryUrl }`：

- `token`：Betby JWT（游客可空/短时 token；登录后带 `security_token`）
- `libraryUrl`：`BTRenderer` 脚本地址（通常是 `ui.invisiblesport.com` 一类，经 `getBetbyProxyUrl` 改写成 `sports-proxy.duel.com`）

然后前端：

```js
new window.BTRenderer().initialize({
  brand_id: "2482975601191952386",
  token: jwt,
  themeName: "duel",
  lang,
  target,
  url: bt-path,          // 深链，例如电竞/Dota/TI
})
```

硬编码配置（index bundle `VITE_*`）：

| 键 | 值 |
|---|---|
| `VITE_BETBY_BRAND_ID_DUEL` | `2482975601191952386` |
| `VITE_BETBY_OPERATOR_ID` | `2432909813404016640` |
| `VITE_BETBY_THEME_DUEL` | `duel` |
| 功能开关 | `MATCH_BETTING_FE_BETBY` = `match_betting_fe_betby` |
| 代理 | `https://sports-proxy.duel.com`（mirror 上改成 `sports-proxy.<mirror>`） |
| 路由 | `/sports`（Betby），`/predictions`（自研 exchange，不是体育盘） |
| 规则路由 | `/sports-betting-rules` |

**没有** Duel 官方公开的 `/api/v2/sports` 赔率列表（404）。赔率在 Betby iframe / `sports-proxy` 后面。

## 拉盘方法（可复用，过了 session 才能拿到价）

1. `GET https://duel.com/api/v2/metadata` 看服务是否活着。
2. `POST https://duel.com/api/v2/match-betting/betby/user-session/en/USD/false`  
   - 游客：body 空  
   - 登录用户：body `{ "security_token": "..." }`（本次不要用户密码，不走这条）
3. 用返回的 `libraryUrl` + `token` 初始化 Betby，或直接打 `sports-proxy.duel.com` 的 Betby 内部 REST（需 JWT）。
4. 在 Betby 树里找 Esports → Dota 2 → The International → Outright / Tournament Winner。
5. `bt-path` 查询参数是深链，TI 冠军盘应类似 `/outright/...` 或 `/esports/dota-2/...`（本次 iframe 没起来，路径未证实）。

`duel_client.py` 按这个顺序跑，成功就打印队伍/赔率，失败打印原因。

## 本次为什么没有价格

1. **产品级关闭：** `/api/v2/match-betting` 明确返回  
   `Match betting is temporarily disabled while we work on some updates.`
2. **地理/IP：** 本机出口在美国（WebFetch 看到 Country: US）。session 和 `sports-proxy` 回 IP/Country blocked。加密货币体育站对美国流量常见硬拦。
3. **不需要登录才能看盘**（代码里游客也会 `user-session`），但现在连游客 session 都发不出来。  
   **缺的不是用户密码，是：match-betting 重新打开 + 非美国出口（或过 CF 的浏览器会话）。**

不要编 Duel 价格。

## 规则页

| 来源 | 状态 | 原文要点 |
|---|---|---|
| JS i18n `pages.betby_rules` | 读到 | title=`Sports Betting Rules` / `Match Betting Rules`；`updated_at_short`=`Updated: 01.06.2026` |
| `/sports-betting-rules` | 200 壳 | 正文来自 `betby_rules_v20.list`，由 `useTranslationLoader` 动态加载，独立 JSON 路径本次 200 但回 SPA HTML |
| https://duelcasinoguide.com/sportsbook/ | 第三方综述 | 写了 futures/void/official grading，**不是官网原文，不当作结算依据** |

冠军盘 / 比赛取消的 **Betby 原文条款本次没有拿到**。只能记：规则页存在、2026-06-01 更新、结算走 Betby 官方结果而不是 Duel Originals 的 provably-fair。对冲前必须再打开 `/sports-betting-rules` 读 void/walkover/延期。

## 复跑

```bash
python3 /workspace/arb-radar/apis/duel_client.py
```

非美出口或 match-betting 恢复后，同一脚本应能打出 session token 和（若 proxy 放行）冠军盘。
