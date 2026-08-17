import networkx as nx

from .node import Node
from .edge import Edge




class GraphBuilder:
    """Builds and queries the AeroDrift cloud topology graph."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node: Node):
        self.graph.add_node(
            node.id,
            type=node.type,
            name=node.name,
            metadata=node.metadata,
        )

    def add_edge(self, edge: Edge):
        self.graph.add_edge(
            edge.source,
            edge.target,
            relation=edge.relation,
            metadata=edge.metadata,
        )

    def build(self, resources):
        """Build a graph from normalized resource dictionaries.

        Expected relationships:
        - Subnet has vpc_id
        - EC2 has subnet_id
        - EC2 may have security_group_ids
        """
        self.graph.clear()

        for resource in resources:
            node = Node(
                node_id=resource["id"],
                node_type=resource["type"],
                name=resource.get("name"),
                metadata=resource.get("metadata", {}),
            )
            self.add_node(node)

        resource_ids = {r["id"] for r in resources}

        for resource in resources:
            resource_id = resource["id"]
            resource_type = resource["type"]

            if resource_type == "Subnet":
                vpc_id = resource.get("vpc_id")
                if vpc_id in resource_ids:
                    self.add_edge(Edge(vpc_id, resource_id, "contains"))

            elif resource_type == "EC2":
                subnet_id = resource.get("subnet_id")
                if subnet_id in resource_ids:
                    self.add_edge(Edge(subnet_id, resource_id, "contains"))

                for sg_id in resource.get("security_group_ids", []):
                    if sg_id in resource_ids:
                        self.add_edge(Edge(resource_id, sg_id, "uses"))

        return self.graph

    def get_graph(self):
        return self.graph

    def get_nodes(self):
        return list(self.graph.nodes(data=True))

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def to_dict(self):
        return {
            "nodes": [
                {"id": node_id, **data}
                for node_id, data in self.graph.nodes(data=True)
            ],
            "edges": [
                {"source": source, "target": target, **data}
                for source, target, data in self.graph.edges(data=True)
            ],
        }
