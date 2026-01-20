# LuhutOS Installation Guide

## Requirements

- 64-bit x86 processor
- 2 GB RAM minimum (4 GB recommended)
- 20 GB disk space minimum
- UEFI firmware
- Internet connection

## Downloading

Download the latest LuhutOS ISO from the releases page.

## Creating Installation Media

### Using dd (Linux)
```bash
sudo dd if=luhutos-*.iso of=/dev/sdX bs=4M status=progress
sync
```

### Using Rufus (Windows)
1. Download Rufus from https://rufus.ie
2. Select the LuhutOS ISO
3. Select your USB drive
4. Click Start

### Using Etcher
1. Download Etcher from https://www.balena.io/etcher
2. Select the LuhutOS ISO
3. Select your USB drive
4. Click Flash

## Booting

1. Insert the USB drive
2. Restart your computer
3. Enter BIOS/UEFI settings (usually F2, F12, Del, or Esc)
4. Set USB as first boot device
5. Save and restart

## Installation

The installer will start automatically when you boot from the USB.

### Step 1: Welcome
Press Enter to continue or Ctrl+C to exit.

### Step 2: Disk Selection
Select the target disk for installation.
**WARNING: All data on the selected disk will be erased!**

### Step 3: Encryption (Optional)
Choose whether to encrypt your disk with LUKS.
If enabled, you'll need to enter the password on every boot.

### Step 4: User Setup
Enter your username and password.
This account will have sudo privileges.

### Step 5: Hostname
Enter a name for your computer.

### Step 6: Optional Bundles
Select additional software to install:
- **Steam**: Gaming platform
- **Docker**: Container platform
- **Developer Tools**: Git, build tools, editors

### Step 7: GPU Driver
Select your GPU driver:
- **auto**: Recommended - automatically detects your GPU
- **nvidia**: NVIDIA proprietary (RTX 20xx and newer)
- **nouveau**: NVIDIA open-source (older cards)
- **amd**: AMD Mesa + Vulkan
- **intel**: Intel Mesa + Vulkan

### Step 8: Confirmation
Review your choices and confirm to start installation.

## Post-Installation

After installation completes:
1. Remove the USB drive
2. Restart your computer
3. Log in with your username and password

## First Boot

On first boot, you'll be greeted by the GNOME desktop with:
- WhiteSur theme (macOS-like appearance)
- Dash to Dock (dock at bottom)
- Blur my Shell (blur effects)

Press **Super+Alt+Space** to open the Luhut Menu for system management.

## Troubleshooting

### Black Screen After Boot
If you experience a black screen after installation:
1. Press Ctrl+Alt+F2 to switch to TTY2
2. Log in with your username
3. Run: `luhutctl repair graphics`
4. Restart: `sudo reboot`

### NVIDIA Issues
For NVIDIA Pascal (GTX 10xx) and older GPUs:
- The open-source nouveau driver is used by default
- Proprietary drivers (590+) don't support these GPUs
- If you experience issues, run: `luhutctl repair graphics`

### Network Issues
If network isn't working:
```bash
sudo systemctl start NetworkManager
nmtui
```

## Getting Help

- GitHub Issues: https://github.com/luhutos/issues
- Documentation: https://github.com/luhutos/docs
