import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ingestion.async_collector import collect_all_resources_async
from ingestion.topology_adapter import normalize_resources
from topology.graph_builder import GraphBuilder
from topology.rich_dashboard import render_topology
from storage.history_db import save_graph_snapshot, get_all_snapshots
from storage.rich_diff import render_graph_diff


console = Console()


async def run_aerodrift_cli():
    console.print(
        Panel.fit(
            "[bold cyan]AeroDrift[/bold cyan]\n"
            "Cloud Topology & Drift Audit CLI",
            border_style="cyan",
        )
    )

    # Step 1: Collect AWS resources
    console.print("\n[bold]1. Collecting AWS resources...[/bold]")
    aws_data = await collect_all_resources_async()

    resource_table = Table(title="AWS Resource Summary")
    resource_table.add_column("Resource Type")
    resource_table.add_column("Count", justify="right")

    total_resources = 0

    for resource_type, resources in aws_data.items():
        count = len(resources)
        total_resources += count
        resource_table.add_row(resource_type, str(count))

    console.print(resource_table)

    # Step 2: Normalize resources
    console.print("\n[bold]2. Normalizing resources...[/bold]")
    resources = normalize_resources(aws_data)

    console.print(
        f"[green]Normalized {len(resources)} resources successfully.[/green]"
    )

    # Step 3: Build topology graph
    console.print("\n[bold]3. Building cloud topology...[/bold]")

    builder = GraphBuilder()
    graph = builder.build(resources)

    console.print(
        f"[green]Topology created:[/green] "
        f"{graph.number_of_nodes()} nodes, "
        f"{graph.number_of_edges()} edges"
    )

    # Step 4: Render topology
    console.print("\n[bold]4. Cloud topology[/bold]")
    render_topology(graph)

    # Step 5: Save historical snapshot
    console.print("\n[bold]5. Saving topology snapshot...[/bold]")

    snapshot = save_graph_snapshot(graph)

    console.print(
        f"[green]Snapshot saved successfully.[/green]\n"
        f"Snapshot ID: {snapshot['snapshot_id']}\n"
        f"Timestamp: {snapshot['timestamp']}"
    )

    # Step 6: Historical diff
    snapshots = get_all_snapshots()

    if len(snapshots) >= 2:
        previous_snapshot = snapshots[-2]["snapshot_id"]
        current_snapshot = snapshots[-1]["snapshot_id"]

        console.print(
            "\n[bold]6. Historical topology diff[/bold]"
        )

        render_graph_diff(
            previous_snapshot,
            current_snapshot,
        )
    else:
        console.print(
            "\n[yellow]Historical diff unavailable. "
            "At least two snapshots are required.[/yellow]"
        )

    # Final summary
    console.print(
        Panel.fit(
            f"[bold green]AeroDrift scan completed[/bold green]\n"
            f"AWS resources: {total_resources}\n"
            f"Graph nodes: {graph.number_of_nodes()}\n"
            f"Graph edges: {graph.number_of_edges()}\n"
            f"Snapshot ID: {snapshot['snapshot_id']}",
            title="Audit Summary",
        )
    )


if __name__ == "__main__":
    asyncio.run(run_aerodrift_cli())