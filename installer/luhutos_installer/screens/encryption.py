"""Encryption configuration screen."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from ..config import InstallerConfig


def show_encryption(console: Console, config: InstallerConfig) -> bool:
    """Show encryption configuration screen. Returns True to continue."""
    console.clear()

    console.print(
        Panel(
            "[bold]Disk Encryption (LUKS)[/bold]\n\n"
            "Encryption protects your data if your device is lost or stolen.\n\n"
            "[green]Pros:[/green]\n"
            "  • Data is secure even if disk is removed\n"
            "  • Required for some compliance standards\n\n"
            "[yellow]Cons:[/yellow]\n"
            "  • Slight performance overhead\n"
            "  • Must enter password on every boot\n"
            "  • Recovery is harder if password is forgotten",
            title="[bold cyan]Encryption[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    config.use_encryption = Confirm.ask(
        "\nEnable disk encryption (LUKS)?",
        default=False,
    )

    if config.use_encryption:
        console.print("[green]Disk encryption enabled.[/green]")
    else:
        console.print("[yellow]Disk encryption disabled.[/yellow]")

    input("\nPress Enter to continue...")
    return True
