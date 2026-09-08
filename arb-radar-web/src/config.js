import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dataDir = path.join(root, "data");
const keysPath = path.join(dataDir, "keys.json");
const SECRET_PATH = "/home/box/sand-data/connector-secrets/946f2321-c2df-4766-b1f6-3ce76d34928b/odds-api-io.json";
const PIN_GUEST_DEFAULT = "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R";

let state = {
  oddsApiIo: "",
  dashToken: "",
  pollSec: 120,
  pinGuestKey: PIN_GUEST_DEFAULT,
};

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return null;
  }
}

function writeKeys() {
  fs.mkdirSync(dataDir, { recursive: true });
  const out = {
    oddsApiIo: state.oddsApiIo || "",
    dashToken: state.dashToken || "",
    pollSec: state.pollSec,
    pinGuestKey: state.pinGuestKey || PIN_GUEST_DEFAULT,
  };
  fs.writeFileSync(keysPath, JSON.stringify(out, null, 2) + "\n");
}

function readSecretKey() {
  const dump = readJson(SECRET_PATH);
  const k = dump && typeof dump.apiKey === "string" ? dump.apiKey.trim() : "";
  return k || "";
}

function last4(key) {
  const s = String(key || "");
  return s.length >= 4 ? s.slice(-4) : "";
}

export function loadConfig() {
  fs.mkdirSync(dataDir, { recursive: true });
  const disk = readJson(keysPath) || {};
  state.oddsApiIo = String(disk.oddsApiIo || "").trim();
  state.dashToken = String(disk.dashToken || "").trim();
  state.pollSec = Number(disk.pollSec) > 0 ? Number(disk.pollSec) : 120;
  state.pinGuestKey = String(disk.pinGuestKey || PIN_GUEST_DEFAULT).trim() || PIN_GUEST_DEFAULT;

  if (!state.oddsApiIo) {
    const envKey = String(process.env.ODDS_API_IO_KEY || "").trim();
    if (envKey) state.oddsApiIo = envKey;
    else {
      const secret = readSecretKey();
      if (secret) state.oddsApiIo = secret;
    }
  }

  let generatedToken = "";
  if (!state.dashToken) {
    const envTok = String(process.env.DASH_TOKEN || "").trim();
    if (envTok) state.dashToken = envTok;
    else {
      state.dashToken = crypto.randomBytes(9).toString("base64url").slice(0, 12);
      generatedToken = state.dashToken;
    }
  }

  writeKeys();
  return { generatedToken };
}

export function getConfig() {
  return { ...state };
}

export function updateConfig(patch = {}) {
  if (patch.oddsApiIo !== undefined) {
    const v = String(patch.oddsApiIo || "").trim();
    if (v) state.oddsApiIo = v;
  }
  if (patch.dashToken !== undefined) {
    const v = String(patch.dashToken || "").trim();
    if (v) state.dashToken = v;
  }
  if (patch.pollSec !== undefined) {
    const n = Number(patch.pollSec);
    if (Number.isFinite(n)) state.pollSec = Math.min(3600, Math.max(30, Math.round(n)));
  }
  if (patch.pinGuestKey !== undefined) {
    const v = String(patch.pinGuestKey || "").trim();
    if (v) state.pinGuestKey = v;
  }
  writeKeys();
  return getConfig();
}

export function publicKeys() {
  return {
    oddsApiIo: {
      configured: Boolean(state.oddsApiIo),
      last4: last4(state.oddsApiIo),
    },
    pollSec: state.pollSec,
    dashTokenConfigured: Boolean(state.dashToken),
  };
}

export function getOddsKey() {
  return state.oddsApiIo || "";
}

export function getDashToken() {
  return state.dashToken || "";
}

export function getPollSec() {
  return state.pollSec || 120;
}

export function getPinGuestKey() {
  return state.pinGuestKey || PIN_GUEST_DEFAULT;
}

export { keysPath };
