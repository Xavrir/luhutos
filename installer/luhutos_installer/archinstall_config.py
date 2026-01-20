"""Generate archinstall configuration files."""

import json
from pathlib import Path
from typing import Any

from .config import InstallerConfig


def generate_user_configuration(config: InstallerConfig, output_dir: Path) -> Path:
    """Generate user_configuration.json for archinstall."""

    # Base configuration
    user_config: dict[str, Any] = {
        "additional-repositories": ["multilib"] if config.install_steam else [],
        "archinstall-language": "English",
        "audio_config": {"audio": "pipewire"},
        "bootloader": "systemd-bootctl",
        "config_version": "2.8.0",
        "debug": False,
        "disk_config": {
            "config_type": "default_layout",
            "device_modifications": [
                {
                    "device": config.disk,
                    "wipe": True,
                    "partitions": [
                        {
                            "btrfs": [],
                            "dev_path": None,
                            "flags": ["Boot"],
                            "fs_type": "fat32",
                            "mount_options": [],
                            "mountpoint": "/boot",
                            "obj_id": "boot",
                            "size": {"sector_size": None, "unit": "MiB", "value": 512},
                            "start": {"sector_size": None, "unit": "MiB", "value": 1},
                            "status": "create",
                            "type": "primary",
                        },
                        {
                            "btrfs": [
                                {"mountpoint": "/", "name": "@"},
                                {"mountpoint": "/home", "name": "@home"},
                                {"mountpoint": "/var/log", "name": "@log"},
                                {"mountpoint": "/.snapshots", "name": "@snapshots"},
                            ],
                            "dev_path": None,
                            "flags": [],
                            "fs_type": "btrfs",
                            "mount_options": ["compress=zstd", "noatime"],
                            "mountpoint": None,
                            "obj_id": "root",
                            "size": {
                                "sector_size": None,
                                "unit": "Percent",
                                "value": 100,
                            },
                            "start": {"sector_size": None, "unit": "MiB", "value": 513},
                            "status": "create",
                            "type": "primary",
                        },
                    ],
                }
            ],
        },
        "hostname": config.hostname,
        "kernels": ["linux"],
        "locale_config": {"kb_layout": "us", "sys_enc": "UTF-8", "sys_lang": "en_US"},
        "mirror_config": {
            "custom_mirrors": [],
            "mirror_regions": {
                "Worldwide": ["https://geo.mirror.pkgbuild.com/$repo/os/$arch"]
            },
        },
        "network_config": {"type": "nm"},
        "ntp": True,
        "parallel downloads": 5,
        "profile_config": {
            "gfx_driver": None,
            "greeter": "gdm",
            "profile": {"custom_settings": {}, "details": ["Gnome"], "main": "Desktop"},
        },
        "swap": True,
        "timezone": "UTC",
        "uki": False,
        "version": "2.8.0",
    }

    # Add encryption if enabled
    if config.use_encryption:
        user_config["disk_encryption"] = {
            "encryption_type": "luks",
            "partitions": ["root"],
        }

    # Custom commands for post-install
    post_install_args = [
        "true" if config.install_steam else "false",
        "true" if config.install_docker else "false",
        "true" if config.install_devtools else "false",
        config.gpu_driver,
    ]
    user_config["custom_commands"] = [
        f"/root/luhutos-post-install.sh {' '.join(post_install_args)}"
    ]

    output_path = output_dir / "user_configuration.json"
    with open(output_path, "w") as f:
        json.dump(user_config, f, indent=2)

    return output_path


def generate_user_credentials(config: InstallerConfig, output_dir: Path) -> Path:
    """Generate user_credentials.json for archinstall."""

    credentials = {
        "!root-password": None,  # No root password, use sudo
        "!users": [
            {"!password": config.password, "sudo": True, "username": config.username}
        ],
    }

    # Add disk encryption password if enabled
    if config.use_encryption:
        credentials["!encryption-password"] = config.encryption_password

    output_path = output_dir / "user_credentials.json"
    with open(output_path, "w") as f:
        json.dump(credentials, f, indent=2)

    return output_path


def generate_configs(
    config: InstallerConfig, output_dir: Path = Path("/tmp/luhutos-install")
) -> tuple[Path, Path]:
    """Generate both configuration files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = generate_user_configuration(config, output_dir)
    creds_path = generate_user_credentials(config, output_dir)

    return config_path, creds_path
