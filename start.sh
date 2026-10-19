#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "$SCRIPT_DIR/.env" ]; then
  set -a
  . "$SCRIPT_DIR/.env"
  set +a
fi

export CG_HOST="${CG_HOST:-0.0.0.0}"
export CG_PORT="${CG_PORT:-8000}"
export CG_ADMIN_USER="${CG_ADMIN_USER:-ghost}"
export CG_ADMIN_HASH="${CG_ADMIN_HASH:-}"
export CG_JWT_SECRET="${CG_JWT_SECRET:?CG_JWT_SECRET required — run install.sh first}"
export CG_AGENT_SECRET="${CG_AGENT_SECRET:?CG_AGENT_SECRET required — run install.sh first}"
export CG_TLS_CERT="${CG_TLS_CERT:-}"
export CG_TLS_KEY="${CG_TLS_KEY:-}"
export CG_REQUIRE_TLS="${CG_REQUIRE_TLS:-0}"
export CG_REQUIRE_PROXY="${CG_REQUIRE_PROXY:-0}"
export CG_USE_TOR="${CG_USE_TOR:-0}"
export CG_TOR_GATEWAY="${CG_TOR_GATEWAY:-socks5://127.0.0.1:9050}"
export CG_PROXIES_FILE="${CG_PROXIES_FILE:-$SCRIPT_DIR/proxies.txt}"
export CG_DB="${CG_DB:-$SCRIPT_DIR/cyberghost.db}"
export CG_LOG="${CG_LOG:-$SCRIPT_DIR/cyberghost.log}"

WORKERS="${WORKERS:-1}"

if [ ! -x "$SCRIPT_DIR/venv/bin/python" ]; then
  echo "[x] venv missing. Run: bash $SCRIPT_DIR/install.sh" >&2
  exit 1
fi

exec "$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/app.py" --workers "$WORKERS"
