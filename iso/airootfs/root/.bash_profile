# Auto-launch LuhutOS installer on first TTY
if [[ $(tty) == /dev/tty1 ]]; then
    /usr/bin/luhutos-installer
fi
