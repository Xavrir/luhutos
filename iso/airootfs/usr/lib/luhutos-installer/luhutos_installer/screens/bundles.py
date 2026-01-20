"""Optional bundles selection screen."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from ..config import InstallerConfig


def show_bundles(console: Console, config: InstallerConfig) -> bool:
    """Show optional bundles screen. Returns True to continue."""
    console.clear()

    console.print(
        Panel(
            "[bold]Optional Software Bundles[/bold]\n\n"
            "Select optional bundles to install with LuhutOS.\n"
            "You can always install these later.",
            title="[bold cyan]Bundles[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    config.install_steam = Confirm.ask("\nInstall Steam (gaming)", default=False)
    config.install_docker = Confirm.ask("Install Docker (containers)", default=False)
    config.install_devtools = Confirm.ask(
        "Install Developer Tools (git, build tools)", default=False
    )

    console.print("\n[green]Bundle selection saved.[/green]")
    input("\nPress Enter to continue...")
    return True
