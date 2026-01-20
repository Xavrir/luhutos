"""Hostname configuration screen."""

import re
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from ..config import InstallerConfig


def validate_hostname(hostname: str) -> bool:
    """Validate hostname format."""
    if len(hostname) > 63 or len(hostname) < 1:
        return False
    return bool(re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$", hostname))


def show_hostname(console: Console, config: InstallerConfig) -> bool:
    """Show hostname configuration screen. Returns True to continue."""
    console.clear()

    console.print(
        Panel(
            "[bold]Hostname Configuration[/bold]\n\n"
            "The hostname identifies your computer on the network.\n"
            "Use letters, numbers, and hyphens (no spaces).",
            title="[bold cyan]Hostname[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    while True:
        hostname = Prompt.ask("\nEnter hostname", default="luhutos")
        if validate_hostname(hostname):
            config.hostname = hostname
            console.print(f"[green]Hostname set to:[/green] {hostname}")
            break
        console.print(
            "[red]Invalid hostname. Use letters, numbers, hyphens only.[/red]"
        )

    input("\nPress Enter to continue...")
    return True
