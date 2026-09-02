from rich.console import Console
from rich.table import Table

from storage.graph_diff import compare_graph_snapshots


console = Console()


def render_graph_diff(old_snapshot_id, new_snapshot_id):
    """
    Display historical topology changes using Rich.
    """

    diff = compare_graph_snapshots(
        old_snapshot_id,
        new_snapshot_id,
    )

    console.print(
        f"\n[bold cyan]AeroDrift Topology Diff[/bold cyan] "
        f"[{old_snapshot_id} -> {new_snapshot_id}]"
    )

    console.print(
        f"[dim]{diff['old_timestamp']} -> "
        f"{diff['new_timestamp']}[/dim]\n"
    )

    table = Table(
        title="Historical Graph Changes",
        show_lines=True,
    )

    table.add_column("Change Type", style="bold")
    table.add_column("Resource / Relationship")

    for node_id in diff["added_nodes"]:
        table.add_row(
            "[green]NODE ADDED[/green]",
            node_id,
        )

    for node_id in diff["removed_nodes"]:
        table.add_row(
            "[red]NODE REMOVED[/red]",
            node_id,
        )

    for node_id in diff["modified_nodes"]:
        table.add_row(
            "[yellow]NODE MODIFIED[/yellow]",
            node_id,
        )

    for source, target, relation in diff["added_edges"]:
        table.add_row(
            "[green]EDGE ADDED[/green]",
            f"{source} --{relation}--> {target}",
        )

    for source, target, relation in diff["removed_edges"]:
        table.add_row(
            "[red]EDGE REMOVED[/red]",
            f"{source} --{relation}--> {target}",
        )

    if (
        not diff["added_nodes"]
        and not diff["removed_nodes"]
        and not diff["modified_nodes"]
        and not diff["added_edges"]
        and not diff["removed_edges"]
    ):
        table.add_row(
            "[green]NO CHANGE[/green]",
            "No topology changes detected",
        )

    console.print(table)

    return diff