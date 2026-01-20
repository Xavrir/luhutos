"""GPU driver selection screen."""

import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from ..config import InstallerConfig


GPU_OPTIONS = ["auto", "nvidia", "amd", "intel", "nouveau"]


def detect_gpu_vendor() -> str:
    """Detect GPU vendor using lspci output."""
    try:
        result = subprocess.run(
            ["lspci"],
            capture_output=True,
            text=True,
        )
        output = result.stdout.lower()
        if "nvidia" in output:
            return "nvidia"
        if "amd" in output or "advanced micro devices" in output:
            return "amd"
        if "intel" in output:
            return "intel"
    except Exception:
        pass
    return "auto"


def show_gpu_selection(console: Console, config: InstallerConfig) -> bool:
    """Show GPU selection screen. Returns True to continue."""
    console.clear()

    detected = detect_gpu_vendor()

    table = Table(title="GPU Driver Options", border_style="cyan")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Driver", style="green")
    table.add_column("Notes", style="dim")

    notes = {
        "auto": "Let LuhutOS pick best driver",
        "nvidia": "Proprietary NVIDIA driver",
        "amd": "Open-source AMD driver",
        "intel": "Open-source Intel driver",
        "nouveau": "Open-source NVIDIA driver",
    }

    for i, option in enumerate(GPU_OPTIONS, 1):
        label = option
        if option == detected:
            label = f"{option} (detected)"
        table.add_row(str(i), option, notes.get(option, ""))

    console.print(
        Panel(
            table,
            title="[bold cyan]GPU Driver[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    while True:
        choice = Prompt.ask("Select driver number", default="1")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(GPU_OPTIONS):
                config.gpu_driver = GPU_OPTIONS[idx]
                console.print(f"\n[green]Selected driver:[/green] {config.gpu_driver}")
                break
        except ValueError:
            pass
        console.print("[red]Invalid selection. Try again.[/red]")

    input("\nPress Enter to continue...")
    return True
