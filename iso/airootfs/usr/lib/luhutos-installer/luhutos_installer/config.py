"""Installer configuration storage."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class InstallerConfig:
    """Stores all user choices during installation."""

    # Disk configuration
    disk: Optional[str] = None
    use_encryption: bool = False
    encryption_password: str = ""

    # User configuration
    username: str = ""
    password: str = ""
    hostname: str = "luhutos"

    # Optional bundles
    install_steam: bool = False
    install_docker: bool = False
    install_devtools: bool = False

    # GPU driver selection
    # Options: auto, nvidia, amd, intel, nouveau
    gpu_driver: str = "auto"
