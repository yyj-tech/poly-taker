import "./proxy.js";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import express from "express";
import { loadConfig, updateConfig, publicKeys, getDashToken } from "./config.js";
import { startPoller, refreshNow, getSnapshot, addClient, reschedule, heartbeat } from "./poller.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const PORT = Number(process.env.PORT) || 8787;
const HOST = process.env.HOST || "127.0.0.1";
const COOKIE = "dash";

function parseCookies(header) {
  const out = {};
  String(header || "").split(";").forEach((part) => {
    const i = part.indexOf("=");
    if (i < 0) return;
    const k = part.slice(0, i).trim();
    const v = part.slice(i + 1).trim();
    if (k) out[k] = decodeURIComponent(v);
  });
  return out;
}

function readToken(req) {
  const cookies = parseCookies(req.headers.cookie);
  if (cookies[COOKIE]) return cookies[COOKIE];
  const auth = String(req.headers.authorization || "");
  if (auth.toLowerCase().startsWith("bearer ")) return auth.slice(7).trim();
  if (req.headers["x-dash-token"]) return String(req.headers["x-dash-token"]);
  return "";
}

function authorized(req) {
  const got = readToken(req);
  const need = getDashToken();
  return Boolean(need) && got === need;
}

function requireAuth(req, res, next) {
  if (authorized(req)) return next();
  res.status(401).json({ error: "unauthorized" });
}

const boot = loadConfig();
if (boot.generatedToken) {
  console.log("访问口令: " + boot.generatedToken);
} else {
  console.log("访问口令已存在（见 data/keys.json，不在此打印）");
}

const app = express();
app.disable("x-powered-by");
app.use(express.json({ limit: "64kb" }));
app.use(express.static(path.join(root, "public")));

app.post("/api/login", (req, res) => {
  const token = String((req.body && req.body.token) || "").trim();
  if (!token || token !== getDashToken()) {
    return res.status(401).json({ error: "口令不对" });
  }
  res.setHeader("Set-Cookie", COOKIE + "=" + encodeURIComponent(token) + "; HttpOnly; SameSite=Lax; Path=/");
  res.json({ ok: true });
});

app.post("/api/logout", (req, res) => {
  res.setHeader("Set-Cookie", COOKIE + "=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0");
  res.json({ ok: true });
});

app.get("/api/me", (req, res) => {
  if (!authorized(req)) return res.status(401).json({ ok: false });
  res.json({ ok: true });
});

app.get("/api/keys", requireAuth, (req, res) => {
  res.json(publicKeys());
});

app.post("/api/keys", requireAuth, (req, res) => {
  const body = req.body || {};
  const patch = {};
  if (body.oddsApiIo !== undefined) patch.oddsApiIo = body.oddsApiIo;
  if (body.pollSec !== undefined) patch.pollSec = body.pollSec;
  if (body.dashToken !== undefined) patch.dashToken = body.dashToken;
  updateConfig(patch);
  reschedule();
  res.json(publicKeys());
});

app.get("/api/snapshot", requireAuth, (req, res) => {
  res.json(getSnapshot());
});

app.post("/api/refresh", requireAuth, async (req, res) => {
  try {
    const snap = await refreshNow();
    res.json(snap);
  } catch (err) {
    res.status(500).json({ error: err && err.message ? err.message : String(err) });
  }
});

app.get("/api/refresh", requireAuth, async (req, res) => {
  try {
    const snap = await refreshNow();
    res.json(snap);
  } catch (err) {
    res.status(500).json({ error: err && err.message ? err.message : String(err) });
  }
});

app.get("/api/stream", requireAuth, (req, res) => {
  res.writeHead(200, {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    Connection: "keep-alive",
  });
  res.write(": connected" + String.fromCharCode(10,10));
  addClient(res);
  res.write("data: " + JSON.stringify(getSnapshot()) + String.fromCharCode(10,10));
});

const server = http.createServer(app);
server.listen(PORT, HOST, () => {
  console.log("arb-radar-web http://" + HOST + ":" + PORT);
  startPoller();
  heartbeat();
});
