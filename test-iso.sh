#!/bin/bash
# LuhutOS ISO Testing Script
# Run: ./test-iso.sh [option]
#
# Options:
#   run       - Boot ISO in QEMU (default)
#   install   - Install QEMU if not present
#   gui       - Boot with GTK display
#   headless  - Boot headless with VNC on :5900

set -euo pipefail

ISO_PATH="$(dirname "$0")/out/luhutos-2026.01.20-x86_64.iso"
LATEST_ISO=$(ls -t "$(dirname "$0")"/out/*.iso 2>/dev/null | head -1)

# Use latest ISO if specific one doesn't exist
if [[ ! -f "$ISO_PATH" ]] && [[ -n "$LATEST_ISO" ]]; then
    ISO_PATH="$LATEST_ISO"
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║     LuhutOS ISO Testing Utility        ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
    echo
}

check_qemu() {
    if ! command -v qemu-system-x86_64 &>/dev/null; then
        echo -e "${RED}ERROR: QEMU not installed${NC}"
        echo -e "${YELLOW}Install with: sudo pacman -S qemu-desktop${NC}"
        echo -e "${YELLOW}Or run: $0 install${NC}"
        return 1
    fi
    return 0
}

check_kvm() {
    if [[ -r /dev/kvm ]] && [[ -w /dev/kvm ]]; then
        echo "-enable-kvm"
    else
        echo -e "${YELLOW}WARNING: KVM not available, using software emulation (slower)${NC}" >&2
        echo ""
    fi
}

install_qemu() {
    echo -e "${CYAN}Installing QEMU...${NC}"
    if command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm qemu-desktop
    elif command -v apt &>/dev/null; then
        sudo apt install -y qemu-system-x86
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y qemu-system-x86
    else
        echo -e "${RED}Unknown package manager. Install QEMU manually.${NC}"
        exit 1
    fi
    echo -e "${GREEN}QEMU installed successfully!${NC}"
}

run_qemu() {
    local display_mode="${1:-gtk}"
    local kvm_flag
    kvm_flag=$(check_kvm)
    
    if [[ ! -f "$ISO_PATH" ]]; then
        echo -e "${RED}ERROR: ISO not found at $ISO_PATH${NC}"
        echo -e "${YELLOW}Build the ISO first with: sudo mkarchiso -v -w .archiso-work -o out iso/${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Booting ISO: ${ISO_PATH}${NC}"
    echo -e "${CYAN}Press Ctrl+Alt+G to release mouse grab${NC}"
    echo
    
    local display_args
    case "$display_mode" in
        gtk)
            display_args="-display gtk,grab-on-hover=on"
            ;;
        headless|vnc)
            display_args="-display none -vnc :0"
            echo -e "${YELLOW}VNC available at localhost:5900${NC}"
            ;;
        sdl)
            display_args="-display sdl"
            ;;
        *)
            display_args="-display gtk"
            ;;
    esac
    
    # Create a temporary disk for testing installation
    local test_disk="/tmp/luhutos-test-disk.qcow2"
    if [[ ! -f "$test_disk" ]]; then
        echo -e "${CYAN}Creating 20GB test disk...${NC}"
        qemu-img create -f qcow2 "$test_disk" 20G
    fi
    
    qemu-system-x86_64 \
        $kvm_flag \
        -m 4G \
        -cpu host \
        -smp 4 \
        -cdrom "$ISO_PATH" \
        -drive file="$test_disk",format=qcow2,if=virtio \
        -boot d \
        -vga virtio \
        $display_args \
        -nic user,model=virtio-net-pci \
        -usb \
        -device usb-tablet \
        -audio driver=pa,model=hda
}

print_usage() {
    echo "Usage: $0 [command]"
    echo
    echo "Commands:"
    echo "  run       Boot ISO in QEMU with GTK display (default)"
    echo "  gui       Same as 'run'"
    echo "  headless  Boot headless with VNC on :5900"
    echo "  install   Install QEMU package"
    echo "  help      Show this help"
    echo
    echo "Requirements:"
    echo "  - qemu-desktop package (sudo pacman -S qemu-desktop)"
    echo "  - Built ISO in out/ directory"
}

# Main
print_header

case "${1:-run}" in
    install)
        install_qemu
        ;;
    run|gui)
        check_qemu && run_qemu gtk
        ;;
    headless|vnc)
        check_qemu && run_qemu headless
        ;;
    help|--help|-h)
        print_usage
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        print_usage
        exit 1
        ;;
esac
