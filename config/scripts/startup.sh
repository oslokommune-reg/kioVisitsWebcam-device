#!/bin/bash
set -euo pipefail

# ------------------------------------------------------------
# Startup script (kio/miljøstasjon style)
# - Ensures TeamViewer daemon is running
# - Loads local env files (dev/prod) from /home/<user>/
# - Ensures repo exists under /home/<user>/<REPO_NAME>
# - Marks repo as git safe.directory (fix "dubious ownership")
# - Pulls only when remote has new code AND repo is clean
# - Runs docker compose (rebuild only when code changed)
# - Performs safe docker cleanup
# ------------------------------------------------------------

# Resolve script directory and move there first (for any local helper scripts)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
echo "SCRIPT_DIR: $PWD"

# Function to check if TeamViewer daemon is active
is_teamviewer_daemon_active() {
  systemctl is-active --quiet teamviewerd
}

# Start TeamViewer daemon if not active
if ! is_teamviewer_daemon_active; then
  echo "Starting TeamViewer daemon..."
  sudo teamviewer daemon enable || true
  sudo teamviewer daemon start || true
  echo "TeamViewer daemon started."
else
  echo "No need to start TeamViewer daemon. It's already running."
fi

# Assign host to Teamviewer client using token (optional)
# ./scripts/enroll_teamviewer_host.sh

# -------------------------
# Local env files (not in git)
# -------------------------
set_env_variables() {
  local env_file="$1"
  if [ -f "$env_file" ]; then
    echo "Setting environment variables from $env_file"
    set -a
    # shellcheck source=/dev/null
    source "$env_file"
    set +a
  else
    echo "Environment file $env_file not found."
  fi
}

# Always load local env from HOME (persists across git pulls)
USER_NAME="${USER:-$(whoami)}"
HOME_DIR="/home/${USER_NAME}"

set_env_variables "${HOME_DIR}/dev.env"
set_env_variables "${HOME_DIR}/prod.env"

# -------------------------
# Repo bootstrap (standardized location)
# -------------------------
BASE_DIR="${HOME_DIR}"

# IMPORTANT:
# Set these to your project.
# For miljøstasjon:
#   REPO_NAME="miljostasjon-device"
# For kioVisitsWebcam:
#   REPO_NAME="kioVisitsWebcam-device"
REPO_NAME="miljostasjon-device"
REPO_URL="https://github.com/oslokommune-reg/${REPO_NAME}.git"

REPO_PATH="${BASE_DIR}/${REPO_NAME}"

mkdir -p "$BASE_DIR"
cd "$BASE_DIR"
echo "BASE_DIR: $PWD"

# Clone if missing (no pull here)
if [ -d "${REPO_PATH}/.git" ]; then
  echo "Repository exists: ${REPO_PATH} (no clone needed)."
else
  echo "Cloning repository ${REPO_URL} -> ${REPO_PATH}"
  git clone "$REPO_URL" "$REPO_PATH"
fi

# Fix git "dubious ownership" for non-sudo git
git config --global --add safe.directory "$REPO_PATH" || true

cd "$REPO_PATH"
echo "REPO_DIR: $PWD"

# Clean apt cache (safe)
sudo apt-get clean || true

# Update all systemctl daemon in case any changes have been made (testing)
sudo systemctl daemon-reload || true

# -------- Conditional rebuild only when code changed --------
git fetch --quiet || true
LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse @{u} 2>/dev/null || echo "$LOCAL")"

# If local repo has uncommitted changes, do NOT pull automatically
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Local changes detected; skipping git pull."
  # Still ensure containers are running
  sudo -E docker compose up -d --remove-orphans
else
  if [ "$LOCAL" != "$REMOTE" ]; then
    echo "Remote has new code. Pulling and rebuilding..."
    git pull --ff-only
    sudo -E docker compose down --remove-orphans || true
    sudo -E docker compose build --pull
    sudo -E docker compose up -d --force-recreate --remove-orphans
  else
    echo "No new code. Ensuring containers are running..."
    sudo -E docker compose up -d --remove-orphans
  fi
fi
# ------------------------------------------------------------

# -------- Auto-cleanup (safe, cache-friendly) ---------------
sudo docker image prune -f || true  # dangling only

DOCKER_DIR="${DOCKER_DIR:-/var/lib/docker}"
FREE_MB="$(df -Pm "$DOCKER_DIR" | awk 'NR==2{print $4}')"
THRESHOLD_MB=2048  # 2 GB threshold

if [ "${FREE_MB:-999999}" -lt "$THRESHOLD_MB" ]; then
  echo "Low disk space detected (${FREE_MB} MB free). Running deeper cleanup..."
  sudo docker image prune -a -f --filter "until=720h" || true
  sudo docker builder prune -f --filter "until=720h" || true
  sudo docker network prune -f || true
fi

if [ "$(date +%d)" = "01" ]; then
  echo "Monthly cleanup..."
  sudo docker image prune -a -f --filter "until=720h" || true
  sudo docker builder prune -f --filter "until=720h" || true
fi
# ------------------------------------------------------------
