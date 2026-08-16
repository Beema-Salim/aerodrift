from rich.console import Console
from rich.panel import Panel

console = Console()

topology_data = {
    "nodes": 4,
    "edges": 3
}

console.print(
    Panel(
        f"[bold]Nodes:[/bold] {topology_data['nodes']}\n"
        f"[bold]Edges:[/bold] {topology_data['edges']}",
        title="Topology",
        border_style="blue"
    )
)
drift_data = {
    "drift_count": 0,
    "issues": 0
}

console.print(
    Panel(
        f"[bold]Drift Count:[/bold] {drift_data['drift_count']}\n"
        f"[bold]Issues:[/bold] {drift_data['issues']}",
        title="Drift",
        border_style="yellow"
    )
)

remediation_data = {
    "status": "pending",
    "actions": 0
}

console.print(
    Panel(
        f"Status: {remediation_data['status']}\n"
        f"Actions: {remediation_data['actions']}",
        title="Remediation",
        border_style="green"
    )
)