class Edge:
    """Represents a relationship between two cloud resources."""

    def __init__(self, source, target, relation, metadata=None):
        self.source = source
        self.target = target
        self.relation = relation
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "metadata": self.metadata,
        }

    def __repr__(self):
        return (
            f"Edge(source={self.source!r}, target={self.target!r}, "
            f"relation={self.relation!r})"
        )
