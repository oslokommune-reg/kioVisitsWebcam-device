#!/usr/bin/env bash
set -euo pipefail

ARDUINO_VER="1.8.19"
ARCH="$(uname -m)"

echo "[arduino] Installing Arduino IDE ${ARDUINO_VER} for arch: ${ARCH}"

sudo apt-get update
# Avhengigheter for IDE + USB/serial
sudo apt-get install -y --no-install-recommends \
  libx11-6 libxext6 libxrender1 libxtst6 libxi6 libfreetype6 \
  ca-certificates xz-utils udev \
  && sudo rm -rf /var/lib/apt/lists/*

TMP_DIR="$(mktemp -d)"
cd "$TMP_DIR"

# Velg riktig Arduino-tarball for Pi
# Offisielle lenker til 1.8.19 ARM tarballs:
#  - ARM32:  https://downloads.arduino.cc/arduino-1.8.19-linuxarm.tar.xz
#  - ARM64:  https://downloads.arduino.cc/arduino-1.8.19-linuxaarch64.tar.xz
# :contentReference[oaicite:2]{index=2}
if [[ "$ARCH" == "aarch64" ]]; then
  TARBALL="arduino-${ARDUINO_VER}-linuxaarch64.tar.xz"
  URL="https://downloads.arduino.cc/${TARBALL}"
else
  # armv7l / armhf
  TARBALL="arduino-${ARDUINO_VER}-linuxarm.tar.xz"
  URL="https://downloads.arduino.cc/${TARBALL}"
fi

echo "[arduino] Downloading: ${URL}"
curl -fsSLO "${URL}"

echo "[arduino] Extracting..."
tar -xJf "${TARBALL}"

echo "[arduino] Installing to /opt ..."
sudo rm -rf "/opt/arduino-${ARDUINO_VER}"
sudo mv "arduino-${ARDUINO_VER}" "/opt/arduino-${ARDUINO_VER}"

echo "[arduino] Running install.sh (adds desktop entries/udev rules when possible)..."
sudo /opt/arduino-${ARDUINO_VER}/install.sh || true

# Sikre at brukeren kan snakke med /dev/ttyUSB* uten sudo
# (dialout er vanlig gruppe for serial på Debian/RPi OS)
sudo usermod -aG dialout "${SUDO_USER:-$USER}" || true

echo "[arduino] Done."
echo "[arduino] NOTE: You may need to log out/in (or reboot) for group changes to take effect."
