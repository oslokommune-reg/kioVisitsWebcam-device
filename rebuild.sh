#!/bin/bash
# rebuild.sh — nuke og bygg prod-containeren fra scratch

set -e

REPO_DIR="/home/kioVisitsWebcam/kioVisitsWebcam-device"
ENV_FILE="/home/kioVisitsWebcam/prod.env"

# Bekreftelsesprompt
echo "Dette vil stoppe containeren, slette imaget og bygge alt på nytt."
read -p "Er du sikker? (j/N): " confirm
[[ "$confirm" =~ ^[jJ]$ ]] || { echo "Avbrutt."; exit 0; }

# Last env-variabler
if [ -f "$ENV_FILE" ]; then
    echo "Laster $ENV_FILE..."
    set -a && source "$ENV_FILE" && set +a
else
    echo "ADVARSEL: $ENV_FILE ikke funnet — env-variabler mangler."
fi

cd "$REPO_DIR"

echo "==> Stopper og fjerner containere..."
sudo -E docker compose down --remove-orphans

echo "==> Sletter gammelt prod-image..."
sudo docker image rm kiovisitswebcam-device-prod 2>/dev/null || echo "(Intet image å slette)"

echo "==> Bygger fra scratch (ingen cache)..."
sudo -E docker compose build --no-cache prod

echo "==> Starter opp..."
sudo -E docker compose up -d prod

echo "==> Ferdig. Logg:"
sudo docker logs --tail 20 prod
