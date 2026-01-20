"""Confirmation screen."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from ..config import InstallerConfig


def show_confirmation(console: Console, config: InstallerConfig) -> bool:
    """Show confirmation screen. Returns True to continue."""
    console.clear()

    table = Table(title="Installation Summary", border_style="cyan")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Disk", config.disk or "Not selected")
    table.add_row("Encryption", "Yes" if config.use_encryption else "No")
    table.add_row("Username", config.username or "Not set")
    table.add_row("Hostname", config.hostname or "luhutos")
    table.add_row("Steam", "Yes" if config.install_steam else "No")
    table.add_row("Docker", "Yes" if config.install_docker else "No")
    table.add_row("Dev Tools", "Yes" if config.install_devtools else "No")
    table.add_row("GPU Driver", config.gpu_driver)

    console.print(
        Panel(
            table,
            title="[bold cyan]Confirm[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    confirmed = Confirm.ask("Proceed with installation?", default=False)
    if confirmed:
        console.print("[green]Installation confirmed.[/green]")
    else:
        console.print("[yellow]Installation cancelled.[/yellow]")

    input("\nPress Enter to finish...")
    return confirmed
