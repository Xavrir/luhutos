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
        # Collect encryption password
        while True:
            password = Prompt.ask("Enter encryption password", password=True)
            if len(password) < 8:
                console.print(
                    "[red]Password too short. Use at least 8 characters.[/red]"
                )
                continue
            confirm = Prompt.ask("Confirm encryption password", password=True)
            if password == confirm:
                config.encryption_password = password
                console.print("[green]Disk encryption enabled.[/green]")
                break
            console.print("[red]Passwords do not match. Try again.[/red]")
    else:
        console.print("[yellow]Disk encryption disabled.[/yellow]")

    input("\nPress Enter to continue...")
    return True
