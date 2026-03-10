# LuhutOS [ONGOING PROJECT]

An Arch-based Linux distribution with GNOME Wayland, safe GPU handling, and macOS-like polish.

LuhutOS takes Arch's rolling-release model and wraps it in curated defaults — a WhiteSur desktop theme, a streamlined TUI installer, and automatic GPU driver detection — so you get a usable system without the manual setup.

## Features

- **GNOME Wayland desktop** with WhiteSur GTK theme, icons, Dash to Dock, and Blur my Shell — dark mode by default
- **Safe GPU handling** — detects Intel, AMD, or NVIDIA at install time with manual override. Legacy NVIDIA (Pascal and older) defaults to nouveau
- **TUI installer** — 8-step guided setup built on top of archinstall: disk selection, LUKS encryption, user setup, GPU driver, and optional software bundles
- **Btrfs with subvolumes** — `@`, `@home`, `@log`, `@snapshots` with zstd compression out of the box
- **PipeWire audio** and **NetworkManager** networking, preconfigured
- **System management tools** — `luhutctl` CLI and `luhut-menu` GTK4 GUI for common tasks (graphics repair, Steam fixes, etc.)
- **Optional bundles** — Steam, Docker, and developer tools (Rust, Go, Node.js, clang) installable during setup

## Quick Start

1. Download the latest ISO from [GitHub Releases](https://github.com/Xavrir/luhutos/releases)
2. Flash to USB with `dd`, Rufus, or Etcher
3. Boot from USB (UEFI required)
4. Run the installer — it launches automatically, or run `luhutos-installer` from the terminal

System requirements: UEFI firmware, 2 GB RAM (minimum), 20 GB disk, internet connection.

## Installer

The installer is an 8-step Python TUI using [Rich](https://github.com/Textualize/rich):

| Step | What it does |
|------|-------------|
| Welcome | Overview, Ctrl+C to exit |
| Disk | Detects drives via `lsblk`, pick your target |
| Encryption | Optional LUKS full-disk encryption |
| User | Username + password with validation |
| Hostname | Machine name with RFC-compliant validation |
| Bundles | Checkboxes for Steam, Docker, DevTools |
| GPU | Auto-detects vendor, offers manual override |
| Confirm | Summary table, final approval before install |

The installer generates an archinstall JSON config and runs it. Post-install adds the LuhutOS repo, installs the desktop meta-packages, configures GPU drivers, and enables GDM.

## Directory Structure

```
luhutos/
├── iso/                  # Archiso profile (packages, airootfs overlay, boot config)
├── packages/             # 14 PKGBUILDs for custom packages
│   ├── luhutos-base/     # Core system meta-package
│   ├── luhutos-gnome/    # GNOME desktop + dconf defaults
│   ├── luhutos-theme-whitesur/
│   ├── luhutos-icons-whitesur/
│   ├── luhutos-extension-*/   # Dash to Dock, User Themes, Blur my Shell
│   ├── luhutctl/         # System management CLI
│   ├── luhut-menu/       # System management GUI (GTK4/Libadwaita)
│   ├── luhutos-release/  # OS branding + repo config
│   ├── luhutos-keyring/  # PGP keyring for package signing
│   ├── luhutos-mirrorlist/
│   └── luhutos-devtools/ # Developer tools meta-package
├── installer/            # Python TUI installer (archinstall wrapper)
├── repo/                 # Pre-built package repository
├── docs/                 # Installation guide, hardware support, troubleshooting
└── test-iso.sh           # QEMU boot/test utility
```

## Building the ISO

Requires an Arch Linux host (or container) with `archiso` installed.

```bash
sudo mkarchiso -v -w /tmp/archiso-tmp -o /tmp/archiso-out iso/
```

The CI pipeline (`.github/workflows/build-iso.yml`) does this automatically on push to `main`.

## Testing

Boot the ISO in QEMU with KVM acceleration:

```bash
./test-iso.sh run       # GTK display (default)
./test-iso.sh headless  # VNC mode
./test-iso.sh install   # Boot with a 20GB test disk
```

## Hardware Support

| GPU Vendor | Driver | Notes |
|------------|--------|-------|
| Intel (UHD 620+, Xe) | `mesa` | Works out of the box |
| AMD (RX 500+) | `mesa` + `xf86-video-amdgpu` | Works out of the box |
| NVIDIA (RTX 20xx+) | `nvidia-dkms` | Proprietary, auto-detected |
| NVIDIA (GTX 16xx) | `nvidia-dkms` | Turing, supported |
| NVIDIA (GTX 10xx and older) | `nouveau` | No Vulkan, no CUDA |
| Hybrid (Intel/AMD + NVIDIA) | `switcheroo-control` + `prime-run` | Optimus switching has limitations |

**Requirements**: UEFI firmware only — legacy BIOS is not supported. Secure Boot is not supported.

See [docs/hardware-support.md](docs/hardware-support.md) for the full compatibility matrix.

## Documentation

- [Installation Guide](docs/installation-guide.md) — step-by-step walkthrough
- [Hardware Support](docs/hardware-support.md) — GPU and hardware compatibility
- [Troubleshooting](docs/troubleshooting.md) — black screen, audio, network, Steam, Docker fixes

## License

LuhutOS project code is MIT licensed. See [LICENSE](LICENSE).

Bundled third-party assets (WhiteSur theme/icons, GNOME Shell extensions) retain their upstream licenses (GPL-2.0/GPL-3.0). See their respective `COPYING` files in `packages/`.

## Credits

- [Arch Linux](https://archlinux.org) — base distribution
- [WhiteSur](https://github.com/vinceliuice/WhiteSur-gtk-theme) by vinceliuice — GTK theme and icon theme
- [Dash to Dock](https://micheleg.github.io/dash-to-dock/) — dock extension
- [Blur my Shell](https://github.com/aunetx/blur-my-shell) — blur effects extension
- [archinstall](https://github.com/archlinux/archinstall) — installation framework
