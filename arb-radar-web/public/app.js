const loginEl = document.getElementById("login");
const loginForm = document.getElementById("login-form");
const loginToken = document.getElementById("login-token");
const loginErr = document.getElementById("login-err");
const freshEl = document.getElementById("fresh");
const sourcesEl = document.getElementById("sources");
const hvEl = document.getElementById("hv");
const drawer = document.getElementById("drawer");
const keyOai = document.getElementById("key-oai");
const keyPoll = document.getElementById("key-poll");
const keyDash = document.getElementById("key-dash");
const keyMeta = document.getElementById("key-meta");
const setMsg = document.getElementById("set-msg");

let refreshing = false;

function dash(v, digits, stale) {
  if (v === null || v === undefined || v === "") return "—";
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  const s = n.toFixed(digits);
  return stale ? s + '<span class="stale">旧</span>' : s;
}

function money(v) {
  if (v === null || v === undefined) return "—";
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  return n.toFixed(1) + " U";
}

function pct(v) {
  if (v === null || v === undefined) return "—";
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  return (n * 100).toFixed(2) + "%";
}

function attr(s) {
  return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
}

function pill(name, src) {
  const st = (src && src.status) || "—";
  let cls = "pill js-refresh";
  if (st === "OK") cls += " ok";
  else if (st === "无key") cls += " nokey";
  else if (st === "失败") cls += " fail";
  return '<span class="' + cls + '" title="点击刷新">' + name + " " + st + "</span>";
}

function rowRefresh(eventName) {
  return '<td><button type="button" class="row-refresh" data-event="' + attr(eventName) + '">刷新</button></td>';
}

function render(snap) {
  if (!snap) return;
  freshEl.textContent = "最后刷新 " + (snap.tsShanghai || "—");
  const s = snap.sources || {};
  sourcesEl.innerHTML = [pill("OAI", s.oddsApiIo), pill("PIN", s.pinnacle), pill("PM", s.polymarket)].join("");
  const hv = snap.highValueCount || 0;
  hvEl.textContent = "高价值 " + hv;
  hvEl.classList.toggle("on", hv > 0);

  const pb = document.querySelector("#tbl-prices tbody");
  pb.innerHTML = (snap.prices || []).map((r) => {
    const st = r.status === "滚球" ? '<span class="live">滚球</span>' : "非滚球";
    return "<tr>" +
      "<td>" + st + "</td>" +
      "<td>" + (r.event || "") + "</td>" +
      "<td>" + (r.teamA || "") + "</td>" +
      "<td>" + (r.teamB || "") + "</td>" +
      '<td class="num">' + dash(r.pmA, 3, r.pmAStale) + "</td>" +
      '<td class="num">' + dash(r.pmB, 3, r.pmBStale) + "</td>" +
      '<td class="num">' + dash(r.pinA, 3, r.pinStale) + "</td>" +
      '<td class="num">' + dash(r.pinB, 3, r.pinStale) + "</td>" +
      '<td class="num">' + dash(r.stakeA, 3, r.stakeStale) + "</td>" +
      '<td class="num">' + dash(r.stakeB, 3, r.stakeStale) + "</td>" +
      '<td class="num">' + dash(r.duelA, 3, r.duelStale) + "</td>" +
      '<td class="num">' + dash(r.duelB, 3, r.duelStale) + "</td>" +
      rowRefresh(r.event) +
      "</tr>";
  }).join("");

  const qb = document.querySelector("#tbl-pos tbody");
  qb.innerHTML = (snap.positions || []).map((r) => {
    const st = r.status === "滚球" ? '<span class="live">滚球</span>' : "非滚球";
    return "<tr class=\"" + (r.highValue ? "hv-row" : "") + "\">" +
      "<td>" + st + "</td>" +
      "<td>" + (r.event || "") + "</td>" +
      "<td>" + (r.leftBuy || "—") + "</td>" +
      "<td>" + (r.rightBuy || "—") + "</td>" +
      '<td class="num">' + money(r.cost) + "</td>" +
      '<td class="num">' + money(r.fee) + "</td>" +
      '<td class="num">' + pct(r.rate) + "</td>" +
      "<td>" + (r.settle || "—") + "</td>" +
      '<td class="num">' + money(r.profit) + "</td>" +
      rowRefresh(r.event) +
      "</tr>";
  }).join("");
}

async function api(path, opts) {
  const res = await fetch(path, Object.assign({ credentials: "same-origin" }, opts || {}));
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.error || res.statusText);
    err.status = res.status;
    throw err;
  }
  return data;
}

async function doRefresh(btn) {
  if (refreshing) return;
  refreshing = true;
  const isBtn = btn && btn.tagName === "BUTTON";
  const prev = isBtn ? btn.textContent : null;
  if (isBtn) {
    btn.disabled = true;
    btn.textContent = "刷新中…";
  }
  document.body.classList.add("refreshing");
  try {
    const snap = await api("/api/refresh", { method: "POST" });
    render(snap);
    freshEl.textContent = "最后刷新 " + (snap.tsShanghai || "—");
    if (setMsg) setMsg.textContent = "已刷新 " + (snap.tsShanghai || "");
  } catch (err) {
    const msg = err.message || "刷新失败";
    freshEl.textContent = msg;
    if (setMsg) setMsg.textContent = msg;
  } finally {
    document.body.classList.remove("refreshing");
    if (isBtn) {
      btn.disabled = false;
      btn.textContent = prev;
    }
    refreshing = false;
  }
}

async function loadKeys() {
  const k = await api("/api/keys");
  keyPoll.value = k.pollSec || 120;
  if (k.oddsApiIo && k.oddsApiIo.configured) {
    keyMeta.textContent = "已配置，末4位 " + (k.oddsApiIo.last4 || "");
  } else {
    keyMeta.textContent = "未配置 odds-api.io key，Stake/Duel 将为 —";
  }
}

function connectSse() {
  const es = new EventSource("/api/stream");
  es.onmessage = (ev) => {
    try {
      const data = JSON.parse(ev.data);
      if (data && data.type === "snapshot") render(data);
    } catch (_) {}
  };
  es.onerror = () => {
    es.close();
    setTimeout(connectSse, 4000);
  };
}

async function boot() {
  try {
    await api("/api/me");
    loginEl.classList.add("hidden");
    const snap = await api("/api/snapshot");
    render(snap);
    connectSse();
    loadKeys().catch(() => {});
  } catch (e) {
    loginEl.classList.remove("hidden");
  }
}

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  loginErr.textContent = "";
  try {
    await api("/api/login", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ token: loginToken.value }),
    });
    loginToken.value = "";
    boot();
  } catch (err) {
    loginErr.textContent = err.message || "登录失败";
  }
});

document.getElementById("btn-settings").onclick = () => {
  drawer.classList.remove("hidden");
  loadKeys().catch(() => {});
};
document.getElementById("btn-close").onclick = () => drawer.classList.add("hidden");
drawer.addEventListener("click", (e) => { if (e.target === drawer) drawer.classList.add("hidden"); });

document.getElementById("btn-save").onclick = async () => {
  setMsg.textContent = "保存中…";
  const body = { pollSec: Number(keyPoll.value) };
  if (keyOai.value.trim()) body.oddsApiIo = keyOai.value.trim();
  if (keyDash.value.trim()) body.dashToken = keyDash.value.trim();
  try {
    const k = await api("/api/keys", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    });
    keyOai.value = "";
    keyDash.value = "";
    keyPoll.value = k.pollSec;
    setMsg.textContent = "已保存，下一轮拉取生效";
    loadKeys();
  } catch (err) {
    setMsg.textContent = err.message || "保存失败";
  }
};

document.addEventListener("click", (e) => {
  const el = e.target.closest("#btn-reload, #btn-refresh, .js-refresh, .row-refresh");
  if (!el) return;
  doRefresh(el);
});

boot();
