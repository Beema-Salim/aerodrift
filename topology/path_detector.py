import networkx as nx


def detect_internet_to_private_path(graph):
    """
    Detect whether a path exists from the Internet node
    to any private database node.
    """

    internet_nodes = [
        node_id
        for node_id, data in graph.nodes(data=True)
        if data.get("type") == "Internet"
        or node_id == "0.0.0.0/0"
    ]

    private_db_nodes = [
        node_id
        for node_id, data in graph.nodes(data=True)
        if data.get("type") == "Database"
        and data.get("metadata", {}).get("private", False)
    ]

    detected_paths = []

    for internet_node in internet_nodes:
        for db_node in private_db_nodes:
            if nx.has_path(graph, internet_node, db_node):
                path = nx.shortest_path(
                    graph,
                    internet_node,
                    db_node,
                )

                detected_paths.append(
                    {
                        "source": internet_node,
                        "target": db_node,
                        "path": path,
                        "severity": "CRITICAL",
                    }
                )

    return detected_paths