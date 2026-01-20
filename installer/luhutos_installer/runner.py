"""Run archinstall with generated configuration."""

import shutil
import subprocess
from pathlib import Path

from rich.console import Console

from .config import InstallerConfig
from .archinstall_config import generate_configs


def copy_post_install_script(
    target_path: Path = Path("/mnt/root/luhutos-post-install.sh"),
) -> None:
    """Copy post-install script to target system."""
    script_source = Path(__file__).parent.parent / "scripts" / "post-install.sh"

    # During live ISO, the script will be at /usr/share/luhutos-installer/scripts/
    if not script_source.exists():
        script_source = Path("/usr/share/luhutos-installer/scripts/post-install.sh")

    if script_source.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(script_source, target_path)
        target_path.chmod(0o755)


def run_archinstall(config: InstallerConfig, console: Console) -> bool:
    """Run archinstall with the generated configuration."""

    console.print("\n[bold cyan]Generating installation configuration...[/bold cyan]")

    try:
        # Generate config files
        config_path, creds_path = generate_configs(config)

        console.print(f"  Config: {config_path}")
        console.print(f"  Credentials: {creds_path}")

        # Copy post-install script to the target system before archinstall runs
        console.print("\n[bold cyan]Copying post-install script...[/bold cyan]")
        copy_post_install_script()

        console.print("\n[bold cyan]Starting archinstall...[/bold cyan]")
        console.print("[dim]This may take several minutes. Please wait.[/dim]\n")

        # Run archinstall
        cmd = [
            "archinstall",
            "--config",
            str(config_path),
            "--creds",
            str(creds_path),
            "--silent",
        ]

        result = subprocess.run(
            cmd,
            capture_output=False,  # Let output go to terminal
        )

        if result.returncode != 0:
            console.print(
                f"\n[bold red]archinstall failed with code {result.returncode}[/bold red]"
            )
            return False

        console.print("\n[bold green]Installation complete![/bold green]")
        return True

    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        return False
