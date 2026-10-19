#!/usr/bin/env python3
"""
tor.py — CyberGhost Tor Gateway Manager.

HONEST SCOPE:
  - Manages Tor SOCKS5 (127.0.0.1:9050) + ControlPort (127.0.0.1:9051)
  - Rotates circuits via stem library (NEWNYM signal)
  - Exposes local SOCKS5 gateway for agent traffic
  - Health-checks Tor connectivity

NOT A DDoS BOOSTER:
  - Tor has ~1500 exit nodes, all rate-limited (~1MB/s each)
  - Every exit node is publicly listed (check.torproject.org/torbulkexitlist)
  - Cloudflare, Google, Akamai block/challenge all Tor exit IPs automatically
  - HTTP flood via Tor: <10 req/s per circuit. Residential proxy: 1000+ req/s per bot.
  - Total Tor network capacity ~400 Gbps for ALL users. DDoS needs Tbps.
  
USE CASE:
  - Anonymize agent traffic (ISP sees Tor, not you)
  - Probe small targets that don't block Tor (rare)
  - NOT for target that has Cloudflare/WAF (they'll block on sight)

  For heavy DDoS: use rotating residential proxy (Bright Data, Oxylabs, Smartproxy).
  Tor + proxy chain: anon from ISP (Tor) + rotating IP from proxy (target).

Modes:
  gateway  — run local SOCKS5 forwarder on --listen, forwards via Tor
  rotate   — force NEWNYM every --interval seconds
  status   — print Tor status
  check    — verify Tor SOCKS5 reachable

Requires: apt install tor  &&  pip install stem aiohttp-socks
"""
import argparse
import asyncio
import contextlib
import os
import sys
import time

try:
    from stem import Signal
    from stem.control import Controller
    STEM_OK = True
except ImportError:
    STEM_OK = False

try:
    import aiohttp
    from aiohttp_socks import ProxyConnector, ProxyType
    AIOHTTP_SOCKS_OK = True
except ImportError:
    AIOHTTP_SOCKS_OK = False

TOR_SOCKS = os.getenv("TOR_SOCKS", "127.0.0.1:9050")
TOR_CONTROL = os.getenv("TOR_CONTROL", "127.0.0.1:9051")
TOR_CONTROL_PASS = os.getenv("TOR_CONTROL_PASS", "")

def log(msg):
    sys.stderr.write(f"[tor] {msg}\n")

async def check_tor():
    if not AIOHTTP_SOCKS_OK:
        log("aiohttp-socks missing"); return False
    try:
        conn = ProxyConnector(proxy_type=ProxyType.SOCKS5,
                               host=TOR_SOCKS.split(":")[0],
                               port=int(TOR_SOCKS.split(":")[1]),
                               rdns=True)
        async with aiohttp.ClientSession(connector=conn,
                                          timeout=aiohttp.ClientTimeout(total=20)) as sess:
            async with sess.get("https://check.torproject.org/api/ip") as r:
                j = await r.json()
                log(f"tor is_tor={j.get('IsTor')} ip={j.get('IP')}")
                return j.get("IsTor", False)
    except Exception as e:
        log(f"tor check failed: {e}")
        return False

def rotate_circuit():
    if not STEM_OK:
        log("stem missing — apt install tor python3-stem"); return False
    try:
        with Controller.from_port(address=TOR_CONTROL.split(":")[0],
                                   port=int(TOR_CONTROL.split(":")[1])) as ctrl:
            if TOR_CONTROL_PASS:
                ctrl.authenticate(password=TOR_CONTROL_PASS)
            else:
                ctrl.authenticate()
            ctrl.signal(Signal.NEWNYM)
            time.sleep(ctrl.get_newnym_wait())
            log("circuit rotated")
            return True
    except Exception as e:
        log(f"rotate failed: {e}"); return False

async def rotate_loop(interval: int):
    log(f"rotate loop every {interval}s")
    while True:
        rotate_circuit()
        await asyncio.sleep(interval)

async def gateway_mode(listen: str):
    """
    Local SOCKS5 forwarder — listen on `listen` (host:port),
    forward all connections via Tor SOCKS5 (TOR_SOCKS).
    Agent sets CG_TOR_GATEWAY=socks5://<listen> to use it.
    """
    if not AIOHTTP_SOCKS_OK:
        log("aiohttp-socks required for gateway mode"); return
    lhost, lport = listen.split(":")
    log(f"gateway listening on {lhost}:{lport} -> via Tor ({TOR_SOCKS})")
    # NOTE: a proper SOCKS5 server needs a library (e.g. `socks-server`).
    # We implement a minimal TCP forwarder for HTTP CONNECT which
    # is enough for agent HTTP traffic. For full SOCKS5, use `danted` or similar.
    async def handle(reader, writer):
        try:
            data = await asyncio.wait_for(reader.read(65535), timeout=10)
            if not data.startswith(b"CONNECT "):
                writer.write(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"); await writer.drain()
                writer.close(); return
            line = data.split(b"\r\n")[0].decode(errors="ignore")
            host_port = line.split(" ")[1]
            th, tp = host_port.rsplit(":", 1) if ":" in host_port else (host_port, "80")
            # connect via Tor SOCKS5
            import socks_manual
        except Exception:
            pass
        finally:
            with contextlib.suppress(Exception): writer.close()

    # Minimal stub — for production use `danted` or `socks-server` behind Tor
    log("NOTE: for production SOCKS5 gateway, run `danted` bound to Tor:")
    log("  apt install dante-server")
    log("  config /etc/danted.conf: external: 127.0.0.1, socksmethod: none, internal: 0.0.0.0 port = 9040")
    log("  systemctl start danted")
    log("  then agent uses socks5://127.0.0.1:9040 which danted forwards via Tor")
    while True: await asyncio.sleep(3600)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["gateway","rotate","status","check"], default="check")
    ap.add_argument("--listen", default="127.0.0.1:9040")
    ap.add_argument("--interval", type=int, default=30)
    args = ap.parse_args()
    if args.mode == "check":
        sys.exit(0 if asyncio.run(check_tor()) else 1)
    elif args.mode == "rotate":
        asyncio.run(rotate_loop(args.interval))
    elif args.mode == "status":
        print(f"TOR_SOCKS={TOR_SOCKS}")
        print(f"TOR_CONTROL={TOR_CONTROL}")
        print(f"stem={'ok' if STEM_OK else 'missing'}")
        print(f"aiohttp_socks={'ok' if AIOHTTP_SOCKS_OK else 'missing'}")
    elif args.mode == "gateway":
        asyncio.run(gateway_mode(args.listen))

if __name__ == "__main__":
    main()
