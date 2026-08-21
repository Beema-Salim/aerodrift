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

topology_panel = Panel(
        f"[bold]Nodes:[/bold] {dashboard_data['topology']['nodes']}\n"
        f"[bold]Edges:[/bold] {dashboard_data['topology']['edges']}",
        title="Topology",
        border_style="blue"
    )



drift_panel = Panel(
        f"[bold]Drift Count:[/bold] {dashboard_data['drift']['drift_count']}\n"
        f"[bold]Issues:[/bold] {dashboard_data['drift']['issues']}",
        title="Drift",
        border_style="yellow"
    )




remediation_panel = Panel(
        f"[bold]Status:[/bold] {dashboard_data['remediation']['status']}\n"
        f"[bold]Actions:[/bold] {dashboard_data['remediation']['actions']}",
        title="Remediation",
        border_style="green"
    )

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