# Miljostasjon image builder

## Usage

Documentation for the sdm package is found here:
https://github.com/gitbls/sdm/blob/master/Docs/Plugins.md#copyfile

For windows, please install WSL to run following in a linux environment: 
wsl --install -d Ubuntu



Firstly, install SDM so that you can build the image(s):
```
curl -L https://raw.githubusercontent.com/gitbls/sdm/master/EZsdmInstaller | bash
```

Ensure there is an image present in the directory. The script is configured to run for the image `2024-10-22-raspios-bookworm-arm64.img`, this can be changed in the `build_sdm.sh` file.

Now run the below command to customize the image
Paste this into wsl terminal: 

set -euo pipefail

# --- Paths (adjust only if your Windows path changes) ---
WIN_REPO="/mnt/c/Users/REG291812/OneDrive - Oslo kommune/Kode/GitHub/kioVisitsWebcam-device"
WSL_ROOT="$HOME/kio-build"
WSL_REPO="$WSL_ROOT/kioVisitsWebcam-device"

# --- Safety checks ---
if [[ ! -d "$WIN_REPO" ]]; then
  echo "ERROR: Windows repo path not found: $WIN_REPO" >&2
  exit 1
fi

# --- Tools ---
sudo apt-get update
sudo apt-get install -y git rsync dos2unix

# --- Aggressive cleanup (WSL workspace + any stale sdm mounts) ---
sudo umount /mnt/sdm/boot/firmware 2>/dev/null || true
sudo umount /mnt/sdm 2>/dev/null || true

rm -rf "$WSL_ROOT"
mkdir -p "$WSL_ROOT"

# --- Clone latest repo into WSL (from the same origin as your Windows repo) ---
REPO_URL="$(git -C "$WIN_REPO" config --get remote.origin.url || true)"
if [[ -z "${REPO_URL:-}" ]]; then
  echo "ERROR: Could not detect origin URL from $WIN_REPO (is it a git repo?)" >&2
  exit 1
fi

echo "Cloning from: $REPO_URL"
git clone --depth 1 "$REPO_URL" "$WSL_REPO"

# Optional: force main/master to be up-to-date (handles default-branch differences)
DEFAULT_BRANCH="$(git -C "$WSL_REPO" symbolic-ref --short -q HEAD || true)"
git -C "$WSL_REPO" fetch --prune --depth 1 origin
git -C "$WSL_REPO" pull --ff-only || true

# --- Copy local, uncommitted config/assets from Windows repo if you rely on them ---
# (If everything is committed, this is harmless. If you have local-only env/images/scripts, it ensures WSL build matches.)
rsync -a --delete \
  --exclude ".git/" \
  "$WIN_REPO/" "$WSL_REPO/"

# --- Normalize line endings (in case Windows files were copied in) ---
cd "$WSL_REPO/config"
dos2unix build_sdm.sh device.env 2>/dev/null || true
dos2unix *.env 2>/dev/null || true
dos2unix scripts/*.sh 2>/dev/null || true
printf '\n' >> device.env

chmod +x build_sdm.sh
chmod +x scripts/*.sh

# --- Clean any old output image in WSL build folder ---
rm -f kioVisitsWebcam-pi.img

# --- Build image ---
bash ./build_sdm.sh

echo
echo "If you land in: root@sdm:/#  then type: exit"
echo

# --- After build: copy image back to Windows with a unique name ---
OUT_DIR="$WIN_REPO/config/out"
mkdir -p "$OUT_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT_IMG="$OUT_DIR/kioVisitsWebcam-pi-$STAMP.img"

ls -lh "$WSL_REPO/config/kioVisitsWebcam-pi.img"
cp -v "$WSL_REPO/config/kioVisitsWebcam-pi.img" "$OUT_IMG"

echo
echo "Done."
echo "Image copied to: $OUT_IMG"




use Raspberry Pi imager V1.9 (not 2) and edit hostname to an unused one, see created_hostnames.txt.


## Enabling easy access in Teamviewer
The device should auto assign itself using the hostname into the Teamviewer account using the TEAMVIEWER_ASSIGNMENT_ID located in the teamviewer.env directory.

Once this is done, user should find the assigned device (hostname) in the Teamviewer console. Select `Manage Device Attributes`, navigate to `Managers` menu using the sidebar. Select `Dataplattform`, and check the `Easy Access` box. 

