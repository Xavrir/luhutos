# LuhutOS Troubleshooting Guide

## Common Issues

### Black Screen After Installation

**Symptom**: System boots but shows only a black screen.

**Cause**: Usually GPU driver issues.

**Solution**:
1. Press `Ctrl+Alt+F2` to switch to TTY2
2. Log in with your username and password
3. Reset graphics to safe mode:
   ```bash
   sudo luhutctl repair graphics
   ```
4. Reboot:
   ```bash
   sudo reboot
   ```

### Login Loop (GDM)

**Symptom**: After entering password, returns to login screen.

**Cause**: Often Xorg session issues or permission problems.

**Solution**:
1. Switch to TTY2: `Ctrl+Alt+F2`
2. Log in
3. Check Xorg log:
   ```bash
   cat ~/.local/share/xorg/Xorg.0.log | tail -50
   ```
4. Try resetting GNOME settings:
   ```bash
   rm -rf ~/.config/gnome-*
   rm -rf ~/.local/share/gnome-shell
   ```
5. Reboot

### No Sound

**Symptom**: No audio output.

**Solution**:
1. Check if PipeWire is running:
   ```bash
   systemctl --user status pipewire
   ```
2. If not running:
   ```bash
   systemctl --user enable --now pipewire pipewire-pulse wireplumber
   ```
3. Check audio settings in GNOME Settings → Sound

### No Network

**Symptom**: Cannot connect to internet.

**Solution**:
1. Check NetworkManager status:
   ```bash
   systemctl status NetworkManager
   ```
2. If not running:
   ```bash
   sudo systemctl enable --now NetworkManager
   ```
3. Use nmtui for network configuration:
   ```bash
   nmtui
   ```

### Steam Not Working

**Symptom**: Steam crashes or games don't launch.

**Cause**: Missing 32-bit graphics drivers.

**Solution**:
1. Reinstall Steam with correct drivers:
   ```bash
   sudo luhutctl steam install
   ```
2. Ensure correct lib32 drivers are installed:
   ```bash
   # For AMD
   sudo pacman -S lib32-mesa lib32-vulkan-radeon
   
   # For Intel
   sudo pacman -S lib32-mesa lib32-vulkan-intel
   
   # For NVIDIA
   sudo pacman -S lib32-nvidia-utils
   ```

### Docker Permission Denied

**Symptom**: `docker: Got permission denied while trying to connect...`

**Cause**: User not in docker group.

**Solution**:
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### Package Conflicts During Update

**Symptom**: `pacman -Syu` fails with conflicts.

**Solution**:
1. Try forcing the update:
   ```bash
   sudo pacman -Syu --overwrite '*'
   ```
2. If that fails, check for orphaned packages:
   ```bash
   pacman -Qtdq | sudo pacman -Rns -
   ```

## Recovery Mode

If your system won't boot at all:

1. Boot from the LuhutOS live USB
2. Mount your installed system:
   ```bash
   mount /dev/sda2 /mnt  # Adjust device name
   mount /dev/sda1 /mnt/boot
   ```
3. Chroot into the system:
   ```bash
   arch-chroot /mnt
   ```
4. Fix the issue (reinstall packages, reset configs, etc.)
5. Exit and reboot:
   ```bash
   exit
   umount -R /mnt
   reboot
   ```

## Getting More Help

### System Logs

View system journal:
```bash
journalctl -b  # Current boot
journalctl -b -1  # Previous boot
```

### Debug Mode

Start GDM in debug mode:
```bash
sudo systemctl stop gdm
sudo gdm --debug
```

### Report an Issue

1. Gather information:
   ```bash
   journalctl -b > boot-log.txt
   lspci -v > hardware.txt
   pacman -Q > packages.txt
   ```

2. Open issue at: https://github.com/luhutos/issues

3. Include:
   - LuhutOS version (`cat /etc/luhutos-release`)
   - Problem description
   - Steps to reproduce
   - Relevant log files
