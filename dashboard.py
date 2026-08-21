from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
console = Console()

environment_data = {
    "name": "Development",
    "region": "ap-south-1",
    "last_updated": "Week 1 Mock Run"
}

title = Text("AeroDrift CLI Dashboard", style="bold cyan")
subtitle = Text("Cloud Infrastructure Monitoring", style="dim")

console.print(title, justify="center")
console.print(subtitle, justify="center")

dashboard_data = {
    "topology": {
        "nodes": 4,
        "edges": 3
    },
    "drift": {
        "drift_count": 0,
        "issues": 0
    },
    "remediation": {
        "status": "pending",
        "actions": 0
    }
}

def create_topology_panel(data):
    return Panel(
        f"[bold]Nodes:[/bold] {data['nodes']}\n"
        f"[bold]Edges:[/bold] {data['edges']}",
        title="Topology",
        border_style="blue"
    )


def create_drift_panel(data):
    return Panel(
        f"[bold]Drift Count:[/bold] {data['drift_count']}\n"
        f"[bold]Issues:[/bold] {data['issues']}",
        title="Drift",
        border_style="yellow"
    )


def create_remediation_panel(data):
    return Panel(
        f"[bold]Status:[/bold] {data['status']}\n"
        f"[bold]Actions:[/bold] {data['actions']}",
        title="Remediation",
        border_style="green"
    )

topology_panel = create_topology_panel(dashboard_data["topology"])
drift_panel = create_drift_panel(dashboard_data["drift"])
remediation_panel = create_remediation_panel(dashboard_data["remediation"])

summary_panel = Panel(
    f"Cloud State: Mock Data\n"
    f"Environment: {environment_data['name']}\n"
    f"Region: {environment_data['region']}\n"
    f"Last Updated: {environment_data['last_updated']}\n"
    f"Resources: {dashboard_data['topology']['nodes']}\n"
    f"Status: Ready",
    title="System Status",
    border_style="magenta"
)

console.print(
    Columns([
        topology_panel,
        drift_panel,
        remediation_panel
    ])
)
console.print(summary_panel)