import networkx as nx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from topology.path_detector import detect_internet_to_private_path

console = Console()


def build_demo_topology():
    graph = nx.DiGraph()

    graph.add_node(
        "0.0.0.0/0",
        type="Internet",
        name="Public Internet",
        metadata={},
    )

    graph.add_node(
        "sg-demo-public",
        type="SecurityGroup",
        name="Public Database SG",
        metadata={
            "public_ingress": True,
            "port": 5432,
        },
    )

    graph.add_node(
        "db-private-demo",
        type="Database",
        name="Private Production DB",
        metadata={
            "private": True,
            "engine": "postgresql",
        },
    )

    graph.add_edge(
        "0.0.0.0/0",
        "sg-demo-public",
        relation="allows",
    )

    graph.add_edge(
        "sg-demo-public",
        "db-private-demo",
        relation="protects",
    )

    return graph


def run_demo():
    console.print(
        Panel.fit(
            "[bold cyan]AeroDrift Security Path Demo[/bold cyan]\n"
            "[yellow]Simulated topology - no AWS resources are modified[/yellow]"
        )
    )

    graph = build_demo_topology()

    detected_paths = detect_internet_to_private_path(graph)

    if not detected_paths:
        console.print(
            "[bold green]No Internet-to-private-database path detected.[/bold green]"
        )
        return []

    table = Table(
        title="Critical Network Paths",
        show_lines=True,
    )

    table.add_column("Severity")
    table.add_column("Source")
    table.add_column("Target")
    table.add_column("Detected Path")

    for result in detected_paths:
        path_text = " -> ".join(result["path"])

        table.add_row(
            f"[bold red]{result['severity']}[/bold red]",
            result["source"],
            result["target"],
            f"[red]{path_text}[/red]",
        )

    console.print(table)

    console.print(
        "\n[bold red]SECURITY DRIFT:[/bold red] "
        "Public Internet can reach a private database."
    )

    return detected_paths


if __name__ == "__main__":
    run_demo()