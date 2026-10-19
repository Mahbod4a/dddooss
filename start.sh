#!/usr/bin/env bash
set -euo pipefail
cd /opt/cyberghost

export CG_HOST="${CG_HOST:-0.0.0.0}"
export CG_PORT="${CG_PORT:-8000}"
export CG_ADMIN_USER="${CG_ADMIN_USER:-ghost}"
export CG_ADMIN_HASH="${CG_ADMIN_HASH:-}"
export CG_JWT_SECRET="${CG_JWT_SECRET:?CG_JWT_SECRET required}"
export CG_AGENT_SECRET="${CG_AGENT_SECRET:?CG_AGENT_SECRET required}"
export CG_TLS_CERT="${CG_TLS_CERT:-}"
export CG_TLS_KEY="${CG_TLS_KEY:-}"
export CG_REQUIRE_TLS="${CG_REQUIRE_TLS:-0}"
export CG_REQUIRE_PROXY="${CG_REQUIRE_PROXY:-0}"
export CG_USE_TOR="${CG_USE_TOR:-0}"
export CG_TOR_GATEWAY="${CG_TOR_GATEWAY:-socks5://127.0.0.1:9050}"
export CG_PROXIES_FILE="${CG_PROXIES_FILE:-$PWD/proxies.txt}"
export CG_DB="${CG_DB:-$PWD/cyberghost.db}"
export CG_LOG="${CG_LOG:-$PWD/cyberghost.log}"

WORKERS="${WORKERS:-1}"

exec ./venv/bin/python ./app.py --workers "$WORKERS"
