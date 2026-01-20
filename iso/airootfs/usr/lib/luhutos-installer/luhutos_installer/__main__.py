#!/usr/bin/env python3
from rich.console import Console

from .config import InstallerConfig
from .runner import run_archinstall
from .screens import (
    show_bundles,
    show_confirmation,
    show_disk_selection,
    show_encryption,
    show_gpu_selection,
    show_hostname,
    show_user_setup,
    show_welcome,
)


def main() -> None:
    console = Console()
    config = InstallerConfig()

    screens = [
        show_welcome,
        show_disk_selection,
        show_encryption,
        show_user_setup,
        show_hostname,
        show_bundles,
        show_gpu_selection,
        show_confirmation,
    ]

    for screen in screens:
        if not screen(console, config):
            console.print("\n[red]Installation aborted.[/red]")
            return

    # Run archinstall with the collected configuration
    console.print("\n[bold cyan]Starting installation...[/bold cyan]")

    success = run_archinstall(config, console)

    if success:
        console.print(
            "\n[bold green]╔════════════════════════════════════════╗[/bold green]"
        )
        console.print(
            "[bold green]║   LuhutOS installation complete!       ║[/bold green]"
        )
        console.print(
            "[bold green]║   Please remove installation media     ║[/bold green]"
        )
        console.print(
            "[bold green]║   and reboot your system.              ║[/bold green]"
        )
        console.print(
            "[bold green]╚════════════════════════════════════════╝[/bold green]"
        )
    else:
        console.print(
            "\n[bold red]Installation failed. Check the logs above.[/bold red]"
        )

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
