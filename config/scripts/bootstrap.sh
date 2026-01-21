#!/bin/bash
set -e

# Add startup.sh to boot
USER=$USER
SERVICE_NAME="kioVisitsWebcam-startup"
export SCRIPT_PATH="/home/${USER}/scripts/startup.sh"

# Make all scripts in ./scripts/ executable
chmod u+x /home/${USER}/scripts/*.sh

# ------------------------------------------------------------
# Enable Raspberry Pi watchdog (host-level reboot on hard hang)
# ------------------------------------------------------------
echo "Enabling host watchdog..."

# Load watchdog kernel module at boot (safe if already set)
echo "bcm2835_wdt" | sudo tee /etc/modules-load.d/watchdog.conf >/dev/null

# Configure systemd to use watchdog (best effort)
# If keys exist -> replace, else -> append
if sudo grep -qE '^\s*RuntimeWatchdogSec=' /etc/systemd/system.conf; then
  sudo sed -i 's/^\s*RuntimeWatchdogSec=.*/RuntimeWatchdogSec=15s/' /etc/systemd/system.conf
else
  echo "RuntimeWatchdogSec=15s" | sudo tee -a /etc/systemd/system.conf >/dev/null
fi

if sudo grep -qE '^\s*ShutdownWatchdogSec=' /etc/systemd/system.conf; then
  sudo sed -i 's/^\s*ShutdownWatchdogSec=.*/ShutdownWatchdogSec=15s/' /etc/systemd/system.conf
else
  echo "ShutdownWatchdogSec=15s" | sudo tee -a /etc/systemd/system.conf >/dev/null
fi

# Apply systemd config changes (safe even if not supported)
sudo systemctl daemon-reexec || true

# ------------------------------------------------------------
# Optional: install Arduino IDE (host) if install script exists
# ------------------------------------------------------------
if [ -f "/home/${USER}/scripts/install_arduino_ide.sh" ]; then
  echo "Installing Arduino IDE (host)..."
  /home/${USER}/scripts/install_arduino_ide.sh
else
  echo "Arduino IDE install script not found, skipping."
fi

# ------------------------------------------------------------
# Systemd service to run startup.sh at boot (ONESHOT)
# ------------------------------------------------------------
echo "Creating systemd service..."

sudo tee /etc/systemd/system/kioVisitsWebcam-startup.service >/dev/null <<'EOF'
[Unit]
Description=Startup procedure (kioVisitsWebcam)
After=network-online.target docker.service
Wants=network-online.target
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=kioVisitsWebcam
Group=kioVisitsWebcam
Environment=HOME=/home/kioVisitsWebcam
WorkingDirectory=/home/kioVisitsWebcam
ExecStart=/home/kioVisitsWebcam/scripts/startup.sh
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=graphical.target
EOF

# 2) Reload og restart
sudo systemctl daemon-reload
sudo systemctl enable kioVisitsWebcam-startup
sudo systemctl restart kioVisitsWebcam-startup

# 3) Verifiser at det er riktig nå
systemctl show -p User -p Group -p Type kioVisitsWebcam-startup
sudo journalctl -u kioVisitsWebcam-startup -n 80 --no-pager


# ------------------------------------------------------------
# Daily reboot fallback (same pattern as miljøstasjon)
# ------------------------------------------------------------
echo "Setting up daily reboot..."
(crontab -l 2>/dev/null; echo "0 2 * * * /sbin/shutdown -r now") | crontab -

# # Get Teamviewer ID from file
# source ./home/${USER}/teamviewer.env

# # # Auto-accept Teamviewer EULA
# sudo teamviewer daemon stop
# sudo bash -c 'echo "[int32] EulaAccepted = 1" >> /opt/teamviewer/config/global.conf'
# sudo bash -c 'echo "[int32] EulaAcceptedRevision = 6" >> /opt/teamviewer/config/global.conf'

# # Start TeamViewer daemon and service
# sudo teamviewer daemon start
# sudo teamviewer daemon enable

# # # Use teamviewer CLI to assign using assignment id
# # echo "Assignign device to Teamviewer"
# # sudo teamviewer assignment --id $TEAMVIEWER_ASSIGNMENT_ID

# # echo "Device addition complete!"

# # Final reboot
# # echo "Installation complete. Rebooting system..."
# # sudo reboot now
