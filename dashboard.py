from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
console = Console()

title = Text("AeroDrift CLI Dashboard", style="bold cyan")
subtitle = Text("Cloud Infrastructure Monitoring", style="dim")

console.print(title, justify="center")
console.print(subtitle, justify="center")

topology_data = {
    "nodes": 4,
    "edges": 3
}

topology_panel = Panel(
        f"[bold]Nodes:[/bold] {topology_data['nodes']}\n"
        f"[bold]Edges:[/bold] {topology_data['edges']}",
        title="Topology",
        border_style="blue"
    )

drift_data = {
    "drift_count": 0,
    "issues": 0
}

drift_panel = Panel(
        f"[bold]Drift Count:[/bold] {drift_data['drift_count']}\n"
        f"[bold]Issues:[/bold] {drift_data['issues']}",
        title="Drift",
        border_style="yellow"
    )


remediation_data = {
    "status": "pending",
    "actions": 0
}

remediation_panel = Panel(
        f"[bold]Status:[/bold] {remediation_data['status']}\n"
        f"[bold]Actions:[/bold] {remediation_data['actions']}",
        title="Remediation",
        border_style="green"
    )
console.print(
    Columns([
        topology_panel,
        drift_panel,
        remediation_panel
    ])
)