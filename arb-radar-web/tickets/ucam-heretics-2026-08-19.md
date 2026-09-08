# UCAM Esports Club vs Team Heretics Academy — ticket check

**NO-GO — not executable.** Same event is real (LES Summer 2026 Playoffs SF2, Bo5, 19 Aug 23:00 CST), but (1) PM vs Duel settlement rules diverge (PM 50-50 / 14-day delay window vs book void), (2) live PM UCAM ask is 0.55 with 8 shares, not 0.460×133, so the printed 7.18% is a stale/wrong-token number, (3) Duel 2.140 is 8h stale and the limit is unknown.

Checked read-only. No bet/order placed. Shanghai snapshot after POST /api/refresh: **2026-08-19 11:15:42 CST**. Independent CLOB/Gamma from this box: **2026-08-19 11:14 CST**. Now ≈ **2026-08-19 11:17 CST**.

---

## Verdict checklist

| Question | Answer |
|---|---|
| REAL event? | **Yes.** LES 2026 Summer Playoffs semifinal 2. Independent listings (loltv / sheepesports / scores24 / bo3.gg) + PM + odds-api.io all name the same pair at 15:00 UTC. |
| SAME EVENT both legs? | **Yes on identity.** Same two orgs, same start, series ML (not map). PM title explicitly **BO5**. Books do not print Bo5 in the OAI row but the commence time + league match. |
| EXECUTABLE at printed size? | **No.** Cannot lift 133 UCAM shares at 0.460. Duel 2.140 last tick **2026-08-18 19:08 UTC / 2026-08-19 03:08 CST**, `duelStale=true`. Limit unknown — do not treat 62U as fillable. |
| Settlement consistent? | **No.** PM 50-50 on cancel / late postpone / pre-start walkover. Duel/Betby-class books typically **void** (often 48h). Per desk rule this kills the arb even if prices looked good. |
| GO / NO-GO | **NO-GO** |

---

## 1. Math

### Ticket prices (dashboard row — internally consistent, not live)

```
Duel stake D     = 133 / 2.140 = 62.14953271 U   (UI rounds to 62.1)
PM spend         = 133 × 0.460 = 61.18 U
PM fee           = spend × 0.05 × p × (1-p)
                 = 61.18 × 0.05 × 0.46 × 0.54 = 0.7598556 U
Cost             = 62.1495 + 61.18 + 0.76 = 124.0894 U   (UI 124.1)
Payout if either side wins (normal play) = 133 U
Profit           = 133 − 124.0894 = 8.9106 U   (UI 8.9)
Rate             = 8.9106 / 124.0894 = 7.181%
```

62.1 × 2.140 = **132.894** (display rounding). Engine uses unrounded D = 133/2.14.

### Live prices (CLOB UCAM yes token, 11:14 CST)

Best ask **0.55 × 8 only**. Walk for 133 shares:

| Level | Take | Cum shares | Cum USDC |
|---|---:|---:|---:|
| 0.55 | 8.00 | 8.00 | 4.40 |
| 0.56 | 115.36 | 123.36 | 69.00 |
| 0.57 | 9.64 | 133.00 | 74.50 |

VWAP **0.560**. If Duel 2.140 still existed (it is stale):

```
D = 133/2.14 = 62.15 U
spend = 74.50
fee ≈ 74.50 × 0.05 × 0.56 × 0.44 = 0.92
cost = 137.56
profit = 133 − 137.56 = −4.56 U    rate −3.32%
```

Implied: `1/2.140 + 0.55 = 0.467 + 0.55 = 1.017` already negative before fee and walk.

Dashboard fee 0.8 U on the printed ticket is the arb.js sports-fee formula, not a 0.8 flat book fee.

---

## 2. Live price table

Sources: Shanghai `GET /api/snapshot` after refresh 11:15:42 CST; odds-api.io cache row id `6861885085`; Gamma event `lol-ucam1-hrts-2026-08-19` market `3601260`; CLOB token UCAM `19346917…87643`, HRTS `30863829…86238`.

| Source | As-of (CST) | UCAM | Heretics Academy | Depth / note |
|---|---|---:|---:|---|
| **Dashboard PM (printed)** | 11:15 | **0.46** | **0.56** | 133 / 125.75 — **does not match live CLOB** |
| **Live PM CLOB ask** | 11:14 | **0.55** | **0.46** | UCAM 8 sh @0.55; then 115 @0.56. HRTS 520 sh @0.46 |
| Live PM CLOB bid | 11:14 | 0.54 | 0.45 | UCAM bid 520 @0.54 |
| Gamma mid/last | 11:12 | 0.545 / last 0.55 | 0.455 | bestBid 0.54 / bestAsk 0.55 |
| **Dashboard Duel** | tick 03:08 | 1.66 | **2.14** | `duelStale=true` (8.1h old) |
| Dashboard Stake | tick 23:37 Aug 18 | 1.65 | 2.10 | `stakeStale=true` (11.6h old) |
| Pinnacle | — | — | — | PIN 403 this refresh; **not a allowed leg** |

Printed ticket used PM UCAM 0.46 + Duel HRTS 2.14. Live UCAM *ask* is 0.55; live *Heretics* ask is 0.46. The 0.460 figure is the **wrong side’s ask** (or a stale UCAM book from when that was the offer). Lifting the cheap 0.46 book on PM buys **Heretics yes**, i.e. the **same side as the Duel leg**.

---

## 3. Position table

### A. Printed ticket (stale / not fillable)

| Leg | Action | Size | Price | UCAM wins | HRTS wins | Cancel / late postpone / pre-start WO |
|---|---|---:|---:|---:|---:|---|
| Duel | buy HRTS Academy | 62.15 U | 2.140 stale | 0 | 132.89 | **void → 62.15 back** (typical book) |
| PM | buy UCAM yes | 133 sh | 0.460 **not on book** | 133 | 0 | **50-50 → 66.50** |
| Fee | PM taker formula | | | −0.76 sunk | −0.76 sunk | −0.76 sunk |
| **Cost** | | **124.09** | | | | |
| **Net after fee** | | | | **+8.91** | **+8.80** | **~+4.6** (only if those prices filled) |

### B. Live reprice, same 133-share ambition (Duel 2.14 **if** it still existed)

| Leg | Action | Size | Price | UCAM wins | HRTS wins | Cancel / 50-50 + void |
|---|---|---:|---:|---:|---:|---:|
| Duel | buy HRTS | 62.15 U | 2.140 stale, limit unknown | 0 | 132.89 | 62.15 refund |
| PM | buy UCAM yes | 133 sh | VWAP 0.560 | 133 | 0 | 66.50 |
| Fee | | | | −0.92 | −0.92 | −0.92 |
| **Cost** | | **137.56** | | | | |
| **Net after fee** | | | | **−4.56** | **−4.67** | **−8.9** |

### C. Live size-down to actual UCAM best ask

| Leg | Action | Size | Price | Net if UCAM | Net if HRTS |
|---|---|---:|---:|---:|---:|
| PM | UCAM yes | 8 sh | 0.55 | | |
| Duel | HRTS | 3.74 U | 2.14 if live | | |
| Cost incl fee | | 8.19 | | **−0.19** | **−0.19** |

No positive edge at live PM even at 8 shares.

**Duel limit:** odds-api.io has no limit field. Conservative: **cannot size 62U**. If a fresh Duel quote ever returned, start at a probe (≈10–20U) only after rules and PM depth clear — they do not today.

---

## 4. Same-event identity

| Field | Polymarket | Duel / odds-api.io | Independent |
|---|---|---|---|
| Teams | UCAM Esports Club vs Team Heretics Academy | same, home/away same order | same |
| Org check | **UCAM Esports Club** = LES main side, not “UCAM Academy”. **Team Heretics Academy** ≠ LEC **Team Heretics** (that was NAVI vs Heretics, already ended). | same full names | rosters: UCAM Kozi/bluerzor/ESCIK/ANDARIEL/ILEVI; HRTS.A Papiteero/Lurox/Mercy9/Lure/Batuuu |
| League | LES Playoffs Semifinal 2 | League of Legends - LES Summer | LES 2026 Summer Playoffs UB SF |
| Format | **BO5** in title + match-winner market (not Game 1) | series ML, format not in OAI title | Bo5 |
| Start | `eventStartTime` 2026-08-19T15:00:00Z; copy says 11:00 AM ET | `date` 2026-08-19T15:00:00Z | 15:00 UTC |
| Slug / id | `lol-ucam1-hrts-2026-08-19` / event 852877 / market 3601260 | event 6861885085 | — |
| Status | prematch, accepting orders | OAI `pending`, `live=false` | scheduled |

Dashboard `8/19 23:00` is **Asia/Shanghai**, not ET. 15:00 UTC = 11:00 ET = **23:00 CST**. From 11:17 CST that is **~11.7 hours** (dashboard “约11.7小时”). Timezone is consistent.

Watchlist alias `heretics` → “team heretics” can collide with the LEC club; this row is a separate OAI event with the full Academy name and did not merge into NAVI vs Heretics. Team identity on *this* ticket is OK.

---

## 5. Settlement comparison

### Polymarket match-winner (quoted from Gamma `description`, market 3601260)

Resolution source text: official info from **https://gol.gg/esports/home**; fallback consensus/video if gol.gg is silent 2h. Event-level `resolutionSource` field also lists `https://www.twitch.tv/LES`.

Quoted rules:

- Winner of the **match** (series), not a map.
- **Canceled (not played) or tie → 50-50.**
- **Postpone:** must be rescheduled to start on or before **2026-09-02 23:59 ET** (14 calendar days after 19 Aug 11:00 AM ET). If the latest announced start is after that deadline → **50-50 even if later played**.
- Match **begins** then one side wins by forfeit/DQ/walkover → **that team wins**.
- Forfeit/DQ/walkover **before start** (other team wins automatically) → **50-50**.
- Name typos / academy tags resolve to the underlying match if uniquely identifiable; ambiguous name → 50-50.

gol.gg is a live stats site (prior LES regular-season UCAM vs HRTS pages exist). It is not a league “official” sheet; PM itself allows a 2h fallback.

### Duel (official slip text not fetched — no Stake/Duel scrape)

odds-api.io / Betby-class esports moneyline norms (bet365/SkyBet-type house rules, Duel guide: void on postponement/abandonment; confirm on Duel.com):

- Winner of the listed match/series as played.
- **Not played / postponed beyond a short window (commonly 48h) → void, stake back.**
- **Pre-start walkover / map awarded without play → usually void the matchup.**
- Format change (Bo5↔Bo3) can void.
- In-play: market can suspend or reject.

Duel.com official sports rules were not opened (constraint: do not scrape Stake/Duel sites). Treat the above as **known book norms**, not a screenshot of this slip.

### Mismatch (this is a hard stop)

| Scenario | PM | Duel (typical) | Hedge? |
|---|---|---|---|
| Played to a winner | pays winner | pays winner | OK |
| Canceled / never played | **50-50** | **void** | **Broken** |
| Postpone >14d (PM) / >~48h (book) | **50-50** | **void** | **Broken** |
| Walkover before start | **50-50** | **void** | **Broken** |
| Walkover after start | pays awarded winner | mixed (some void, some pay) | **Risky** |
| Roster / academy stand-in | “underlying match” | listed team; subst. usually action | usually OK |

Dashboard `arb.js` marks PIN as `rulesOk:false` with “PM 延期窗口/50-50 vs PIN 超时 void” but marks **Duel/Stake `rulesOk:true`**. Same divergence applies. That is why this row flipped `highValue: true` without a rule note.

**Flag: NOT executable** even if 0.46/2.14 were live.

---

## 6. Execution

### Polymarket

- Token to buy for the printed hedge: UCAM yes `19346917367595178814805852787250926653278398773361795948520740121299531087643`.
- Live: **cannot** lift 133 @ 0.460. Best ask **0.55 × 8**. Next 115.36 @ 0.56.
- Min order 5, tick 0.01. `feesEnabled`, `feeType=sports_fees_v2`, taker 5% × p(1-p).
- If someone hits the **0.46** ask, that is the **Heretics** token (520 sh @ 0.46). That doubles HRTS, does not hedge.
- Dashboard `pmAStale=false` is a false comfort: price is wrong vs independent CLOB/Gamma.

### Duel

- OAI row: `duelHome 1.66 / duelAway 2.14`, `duelUpdated 2026-08-18T19:08:46.341Z` (**2026-08-19 03:08 CST**).
- Refresh 11:15 CST **re-fetched OAI (36 events)** and the timestamps **did not move**. Book is not quoting fresh.
- **Limit unknown.** Do not assume 62U fills. Conservative max until a limit exists: small probe only, and not on this ticket.

### Staleness

| Feed | Fresh? |
|---|---|
| PM CLOB (this box) | Yes, ~minutes |
| Dashboard PM 0.46/0.56 | **No — disagrees with live book** |
| Duel 2.14 | **No — 8.1h, `duelStale`** |
| Stake 2.10 | **No — 11.6h, `stakeStale`** |

---

## 7. Timing

| Clock | Value |
|---|---|
| Scheduled start | 2026-08-19 **15:00 UTC** = **11:00 ET** = **23:00 CST** |
| Now | ~2026-08-19 11:17 CST |
| Hours to start | **~11.7 h** |
| PM delay deadline | 2026-09-02 23:59 ET |
| Prematch? | Yes (`非滚球`, OAI pending, start in future) |

After 23:00 CST the book can go in-play / suspend while PM `clearBookOnStart` / `automaticallyActive` still trades — one-leg fill risk.

---

## 8. Other risks

- **Currency:** Duel crypto/fiat vs PM USDC. Basis + withdrawal/KYC on Duel winnings.
- **Wrong-token flip:** printed 0.460 is Heretics’ live ask, labeled UCAM. Highest operational risk if someone “lifts 0.46”.
- **Academy vs main:** this pairing is Academy vs UCAM Club (correct). Do not hedge with LEC Team Heretics leftovers (NAVI vs Heretics row is a different, ended match).
- **Home/away:** both sources UCAM home, HRTS.A away. No flip vs OAI.
- **In-play switch:** 11.7h is enough for odds to move; stale Duel can already be dead.
- **PM sports fee** eats ~0.76U even on the fantasy ticket; more when walking the book.
- **gol.gg vs LES broadcast:** dual resolution sources (gol.gg vs twitch.tv/LES) — slow gol.gg can delay PM while Duel already grades.

---

## 9. What would make it executable

All of the following, together:

1. **Rules:** written Duel moneyline terms that pay the series winner the same way PM does on cancel / postpone / pre-start WO (no 50-50 vs void). Or a different book that is contractually aligned. Today they are not.
2. **Fresh Duel** quote with a **known limit**, `duelUpdated` < 30 min, still prematch.
3. **Live PM UCAM yes ask** (token `19346…87643`) deep enough at a price where `1/O_duel + p_ask + fee < 1`. At 2.14 that needs p ≲ 0.45 after fee — **not** 0.55.
4. Confirm the order ticket buys **UCAM yes**, not the 0.46 Heretics ask.
5. Size to **min(PM level-1 size, Duel limit, conservative 10–20U if limit still blank)**.

Until then: **do not place**.

---

## IDs / quotes (for the parent)

- PM event: https://polymarket.com/event/lol-ucam1-hrts-2026-08-19
- Gamma: `https://gamma-api.polymarket.com/events?slug=lol-ucam1-hrts-2026-08-19`
- CLOB UCAM: `https://clob.polymarket.com/book?token_id=19346917367595178814805852787250926653278398773361795948520740121299531087643`
- OAI cache: `/opt/arb-radar-web/data/oai-cache.json` row 6861885085
- Shanghai refresh: 2026-08-19 11:15:42 CST, `highValueCount=1` (this ticket) — **ignore that flag**

No services were changed. Visa/nginx on Shanghai not touched.
