import argparse
import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from self_healing import handle_drift_event
from ingestion.async_collector import collect_all_resources_async
from ingestion.topology_adapter import normalize_resources
from ingestion.exposure_detector import find_public_ingress
from ingestion.drift_event import create_drift_events
from topology.graph_builder import GraphBuilder
from topology.rich_dashboard import render_topology
from topology.exposure_graph import add_public_exposure_edges
from topology.path_detector import detect_internet_to_private_path
from storage.history_db import save_graph_snapshot, get_all_snapshots
from storage.rich_diff import render_graph_diff
from storage.rich_remediation import render_remediation_history


console = Console()


async def run_aerodrift_cli(remediate=False):
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
   # Step 4: Detect security drift
    console.print("\n[bold]4. Detecting public ingress drift...[/bold]")

    exposures = find_public_ingress(
    aws_data.get("security_groups", [])
)

# Add Internet -> exposed SecurityGroup relationships
    add_public_exposure_edges(graph, exposures)

# Detect Internet -> private Database attack paths
    critical_paths = detect_internet_to_private_path(graph)

    drift_events = create_drift_events(exposures)
    drifted_nodes = [
        event["resource_id"]
        for event in drift_events
    ]

    console.print("\n[bold]5. Cloud topology[/bold]")

    render_topology(
        graph,
        drifted_nodes=drifted_nodes,
    )
    if critical_paths:
        path_table = Table(
        title="Critical Internet to Private Database Paths"
   )

        path_table.add_column("Source")
        path_table.add_column("Target")
        path_table.add_column("Path")
        path_table.add_column("Severity")

        for detected_path in critical_paths:
           path_table.add_row(
            str(detected_path["source"]),
            str(detected_path["target"]),
            " -> ".join(detected_path["path"]),
            str(detected_path["severity"]),
          )

        console.print(path_table)
    else:
        console.print(
            "[green]No Internet-to-private-database "
            "path detected.[/green]"
      )

    if drift_events:
        drift_table = Table(title="Critical Drift Events")
        drift_table.add_column("Resource")
        drift_table.add_column("Event")
        drift_table.add_column("Severity")
        drift_table.add_column("CIDR")
        drift_table.add_column("Ports")

        for event in drift_events:
            drift_table.add_row(
                str(event["resource_id"]),
                str(event["event_type"]),
                str(event["severity"]),
                str(event["cidr"]),
                f"{event['from_port']} - {event['to_port']}",
            )

        console.print(drift_table)
        if remediate:
            console.print(
                "\n[bold yellow]Remediation mode enabled.[/bold yellow]"
            )

            for event in drift_events:
                try:
                    result = handle_drift_event(event)

                    console.print(
                        f"[green]Remediated:[/green] "
                        f"{result['resource_id']}"
                    )

                    console.print(
                        f"[green]Incident report:[/green] "
                        f"{result['report_path']}"
                    )

                except Exception as error:
                    console.print(
                        f"[bold red]Remediation failed:[/bold red] {error}"
                    )
        else:
            console.print(
                "[yellow]Audit-only mode. "
                "No AWS changes were made.[/yellow]"
            )
    else:
        console.print(
            "[green]No public ingress drift detected.[/green]"
        )

   # Step 6: Save historical snapshot
    console.print("\n[bold]6. Saving topology snapshot...[/bold]")

    snapshot = save_graph_snapshot(graph)

    console.print(
        f"[green]Snapshot saved successfully.[/green]\n"
        f"Snapshot ID: {snapshot['snapshot_id']}\n"
        f"Timestamp: {snapshot['timestamp']}"
    )

        # Step 7: Historical diff
    snapshots = get_all_snapshots()

    if len(snapshots) >= 2:
        previous_snapshot = snapshots[-2]["snapshot_id"]
        current_snapshot = snapshots[-1]["snapshot_id"]

        console.print(
            "\n[bold]7. Historical topology diff[/bold]"
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

    # Step 8: Recent remediation history
    console.print(
        "\n[bold]8. Recent Remediation History[/bold]"
    )

    render_remediation_history(limit=5)

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
    parser = argparse.ArgumentParser(
        description="AeroDrift Cloud Topology & Remediation CLI"
    )

    parser.add_argument(
        "--remediate",
        action="store_true",
        help="Execute validated remediation for detected drift",
    )

    args = parser.parse_args()

    asyncio.run(
        run_aerodrift_cli(remediate=args.remediate)
        )
