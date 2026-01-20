# LuhutOS Hardware Support Matrix

## Tested Hardware

### GPUs

| Vendor | Series | Driver | Status |
|--------|--------|--------|--------|
| Intel | UHD 620+ | mesa | ✅ Fully Supported |
| Intel | Xe Graphics | mesa | ✅ Fully Supported |
| AMD | RX 500+ | mesa + vulkan-radeon | ✅ Fully Supported |
| AMD | RX 6000/7000 | mesa + vulkan-radeon | ✅ Fully Supported |
| NVIDIA | RTX 20xx+ | nvidia-open | ✅ Fully Supported |
| NVIDIA | GTX 16xx | nvidia-open | ✅ Fully Supported |
| NVIDIA | GTX 10xx | nouveau | ⚠️ Limited (no Vulkan) |
| NVIDIA | GTX 9xx | nouveau | ⚠️ Limited (no Vulkan) |

### NVIDIA Legacy Support

**Important**: As of December 2024, NVIDIA driver 590+ dropped support for Pascal (GTX 10xx) and older GPUs.

For these GPUs, LuhutOS defaults to:
- **nouveau** (open-source) driver
- Basic OpenGL support
- No Vulkan support
- No CUDA support

If you need proprietary drivers for legacy NVIDIA GPUs:
1. Use the nvidia-470xx-dkms package from AUR (unsupported)
2. This requires manual installation and is not recommended

### Hybrid GPU Laptops

For laptops with both integrated and discrete GPUs:
- **switcheroo-control** is installed automatically
- Right-click applications to choose GPU
- Or use `prime-run <application>` for NVIDIA

### Tested Systems

| System | Components | Status |
|--------|------------|--------|
| Generic UEFI VM | VirtIO | ✅ Works |
| ThinkPad X1 Carbon | Intel iGPU | ✅ Works |
| Dell XPS 15 | Intel + NVIDIA | ✅ Works |
| Custom Desktop | AMD GPU | ✅ Works |
| Custom Desktop | NVIDIA RTX 30xx | ✅ Works |

## Known Issues

### NVIDIA Optimus (Hybrid)
- Some applications may not switch GPUs correctly
- Workaround: Use `prime-run` command

### Secure Boot
- Not currently supported
- Disable Secure Boot in BIOS

### Older BIOS Systems
- UEFI required
- Legacy BIOS not supported

## Reporting Hardware Issues

If you encounter hardware compatibility issues:

1. Gather system information:
   ```bash
   lspci -v > hardware-info.txt
   lsusb >> hardware-info.txt
   dmesg | tail -100 >> hardware-info.txt
   ```

2. Open an issue at: https://github.com/luhutos/issues

3. Include:
   - Hardware model
   - Problem description
   - Steps to reproduce
   - hardware-info.txt contents
