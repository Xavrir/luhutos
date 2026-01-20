"""Welcome screen."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..config import InstallerConfig


def show_welcome(console: Console, config: InstallerConfig) -> bool:
    """Show welcome screen. Returns True to continue, False to exit."""
    console.clear()

    welcome_text = Text()
    welcome_text.append("Welcome to ", style="white")
    welcome_text.append("LuhutOS", style="bold cyan")
    welcome_text.append(" Installer\n\n", style="white")
    welcome_text.append(
        "This installer will guide you through setting up LuhutOS.\n\n", style="dim"
    )
    welcome_text.append("LuhutOS features:\n", style="white")
    welcome_text.append("  • GNOME desktop with Wayland\n", style="green")
    welcome_text.append("  • macOS-like theming (WhiteSur)\n", style="green")
    welcome_text.append("  • Safe GPU driver detection\n", style="green")
    welcome_text.append("  • Optional Steam & Docker\n", style="green")
    welcome_text.append("  • Btrfs with snapshots\n", style="green")

    console.print(
        Panel(
            welcome_text,
            title="[bold cyan]LuhutOS[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    console.print("\n[dim]Press Enter to continue, or Ctrl+C to exit...[/dim]")
    try:
        input()
        return True
    except KeyboardInterrupt:
        return False
