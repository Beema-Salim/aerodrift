class Node:
    """Represents a cloud resource in the AeroDrift topology graph."""

    def __init__(self, node_id, node_type, name=None, metadata=None):
        self.id = node_id
        self.type = node_type
        self.name = name
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "metadata": self.metadata,
        }

    def __repr__(self):
        return f"Node(id={self.id!r}, type={self.type!r}, name={self.name!r})"
