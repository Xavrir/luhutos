#!/bin/bash
set -euo pipefail

LOG_FILE="/var/log/luhutos-post-install.log"

log() {
  local message="$1"
  printf '[%s] %s\n' "$(date -Iseconds)" "$message" | tee -a "$LOG_FILE"
}

run() {
  log "Running: $*"
  "$@"
}

# Arguments passed from installer
INSTALL_STEAM="${1:-false}"
INSTALL_DOCKER="${2:-false}"
INSTALL_DEVTOOLS="${3:-false}"
GPU_DRIVER="${4:-auto}"

log "Starting LuhutOS post-install"
log "INSTALL_STEAM=$INSTALL_STEAM INSTALL_DOCKER=$INSTALL_DOCKER INSTALL_DEVTOOLS=$INSTALL_DEVTOOLS GPU_DRIVER=$GPU_DRIVER"

# Add LuhutOS repository to pacman.conf
log "Configuring pacman repository"
{
  echo ""
  echo "[luhutos]"
  echo "SigLevel = Optional TrustAll"
  echo "Server = https://github.com/luhutos/repo/releases/download/packages/\$arch"
} >> /etc/pacman.conf

# Refresh package databases
run pacman -Sy

# Install core LuhutOS packages
run pacman -S --noconfirm luhutos-base luhutos-gnome luhutctl luhut-menu || true

# GPU driver installation
case "$GPU_DRIVER" in
  nvidia)
    run pacman -S --noconfirm nvidia-open nvidia-utils
    ;;
  amd)
    run pacman -S --noconfirm mesa vulkan-radeon
    ;;
  intel)
    run pacman -S --noconfirm mesa vulkan-intel
    ;;
  nouveau)
    run pacman -S --noconfirm mesa xf86-video-nouveau
    ;;
  auto)
    log "GPU driver set to auto; skipping explicit driver install"
    ;;
  *)
    log "Unknown GPU driver '$GPU_DRIVER'; skipping"
    ;;
esac

# Install Steam if selected
if [[ "$INSTALL_STEAM" == "true" ]]; then
  run pacman -S --noconfirm steam
fi

# Install Docker if selected
if [[ "$INSTALL_DOCKER" == "true" ]]; then
  run pacman -S --noconfirm docker
  run systemctl enable docker.service
fi

if [[ "$INSTALL_DEVTOOLS" == "true" ]]; then
  run pacman -S --noconfirm luhutos-devtools
fi

# Enable GDM
run systemctl enable gdm.service

log "LuhutOS post-install complete!"
