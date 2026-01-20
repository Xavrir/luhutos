"""User setup screen."""

import re
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from ..config import InstallerConfig


def validate_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r"^[a-z_][a-z0-9_-]*$", username)) and len(username) <= 32


def show_user_setup(console: Console, config: InstallerConfig) -> bool:
    """Show user setup screen. Returns True to continue."""
    console.clear()

    console.print(
        Panel(
            "[bold]User Account Setup[/bold]\n\n"
            "Create your user account for LuhutOS.\n"
            "This account will have sudo privileges.",
            title="[bold cyan]User Setup[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    # Username
    while True:
        username = Prompt.ask("\nEnter username", default="user")
        if validate_username(username):
            config.username = username
            break
        console.print(
            "[red]Invalid username. Use lowercase letters, numbers, underscores, hyphens.[/red]"
        )

    # Password
    while True:
        password = Prompt.ask("Enter password", password=True)
        if len(password) < 4:
            console.print("[red]Password too short. Use at least 4 characters.[/red]")
            continue
        confirm = Prompt.ask("Confirm password", password=True)
        if password == confirm:
            config.password = password
            console.print("[green]User account configured.[/green]")
            break
        console.print("[red]Passwords do not match. Try again.[/red]")

    input("\nPress Enter to continue...")
    return True
