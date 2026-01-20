"""Disk selection screen."""

import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from ..config import InstallerConfig


def get_available_disks() -> list[dict]:
    """Get list of available disks using lsblk."""
    try:
        result = subprocess.run(
            ["lsblk", "-d", "-n", "-o", "NAME,SIZE,TYPE,MODEL"],
            capture_output=True,
            text=True,
        )
        disks = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split(None, 3)
                if len(parts) >= 3 and parts[2] == "disk":
                    disks.append(
                        {
                            "name": f"/dev/{parts[0]}",
                            "size": parts[1],
                            "model": parts[3] if len(parts) > 3 else "Unknown",
                        }
                    )
        return disks
    except Exception:
        # Fallback for demo/testing
        return [
            {"name": "/dev/sda", "size": "256G", "model": "Demo Disk"},
            {"name": "/dev/nvme0n1", "size": "512G", "model": "NVMe SSD"},
        ]


def show_disk_selection(console: Console, config: InstallerConfig) -> bool:
    """Show disk selection screen. Returns True to continue."""
    console.clear()

    disks = get_available_disks()

    table = Table(title="Available Disks", border_style="cyan")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Device", style="green")
    table.add_column("Size", style="yellow")
    table.add_column("Model", style="dim")

    for i, disk in enumerate(disks, 1):
        table.add_row(str(i), disk["name"], disk["size"], disk["model"])

    console.print(
        Panel(
            table,
            title="[bold cyan]Disk Selection[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    console.print(
        "\n[bold red]WARNING:[/bold red] The selected disk will be COMPLETELY ERASED!\n"
    )

    while True:
        choice = Prompt.ask(
            "Select disk number",
            default="1",
        )
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(disks):
                config.disk = disks[idx]["name"]
                console.print(f"\n[green]Selected:[/green] {config.disk}")
                input("\nPress Enter to continue...")
                return True
        except ValueError:
            pass
        console.print("[red]Invalid selection. Try again.[/red]")
