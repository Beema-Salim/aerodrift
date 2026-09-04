from rich.console import Console
from rich.tree import Tree


console = Console()


def render_topology(graph, drifted_nodes=None):
    """
    Render cloud topology in terminal using Rich.
    Drifted nodes are highlighted in red.
    """

    drifted_nodes = set(drifted_nodes or [])

    tree = Tree("[bold cyan]AeroDrift Cloud Topology[/bold cyan]")

    for node_id, data in graph.nodes(data=True):
        node_type = data.get("type", "Unknown")
        node_name = data.get("name") or node_id

        label = f"{node_type}: {node_name}"

        if node_id in drifted_nodes:
            label = f"[bold red]{label} [DRIFT][/bold red]"

        node_branch = tree.add(label)

        for neighbor in graph.successors(node_id):
            edge_data = graph.get_edge_data(node_id, neighbor) or {}
            relation = edge_data.get("relation", "connected")

            neighbor_data = graph.nodes[neighbor]
            neighbor_type = neighbor_data.get("type", "Unknown")
            neighbor_name = neighbor_data.get("name") or neighbor

            neighbor_label = (
                f"{relation} -> {neighbor_type}: {neighbor_name}"
            )

            if neighbor in drifted_nodes:
                neighbor_label = (
                    f"[bold red]{neighbor_label} [DRIFT][/bold red]"
                )

            node_branch.add(neighbor_label)

    console.print(tree)