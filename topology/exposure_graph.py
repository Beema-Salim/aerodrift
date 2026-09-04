def add_public_exposure_edges(graph, exposures):
    """
    Enrich the topology graph with Internet -> SecurityGroup
    edges for detected public ingress exposures.
    """

    internet_node = "0.0.0.0/0"

    public_security_groups = {
        exposure.get("security_group_id")
        for exposure in exposures
        if exposure.get("security_group_id")
    }

    if not public_security_groups:
        return graph

    graph.add_node(
        internet_node,
        type="Internet",
        name="Public Internet",
        metadata={
            "cidr": internet_node,
        },
    )

    for security_group_id in public_security_groups:
        if security_group_id not in graph:
            continue

        graph.add_edge(
            internet_node,
            security_group_id,
            relation="public_ingress",
            metadata={
                "severity": "CRITICAL",
            },
        )

    return graph