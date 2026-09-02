import json
import sqlite3

from storage.history_db import DB_PATH, initialize_database


def get_snapshot(snapshot_id):
    """
    Load one historical graph snapshot from SQLite.
    """
    initialize_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, timestamp, nodes, edges
        FROM graph_snapshots
        WHERE id = ?
        """,
        (snapshot_id,),
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        raise ValueError(f"Snapshot {snapshot_id} not found")

    return {
        "snapshot_id": row[0],
        "timestamp": row[1],
        "nodes": json.loads(row[2]),
        "edges": json.loads(row[3]),
    }


def compare_graph_snapshots(old_snapshot_id, new_snapshot_id):
    """
    Compare two historical graph snapshots.
    """

    old_snapshot = get_snapshot(old_snapshot_id)
    new_snapshot = get_snapshot(new_snapshot_id)

    old_nodes = {
        node["id"]: node
        for node in old_snapshot["nodes"]
    }

    new_nodes = {
        node["id"]: node
        for node in new_snapshot["nodes"]
    }

    added_nodes = sorted(
        set(new_nodes) - set(old_nodes)
    )

    removed_nodes = sorted(
        set(old_nodes) - set(new_nodes)
    )

    modified_nodes = sorted(
        node_id
        for node_id in set(old_nodes) & set(new_nodes)
        if old_nodes[node_id] != new_nodes[node_id]
    )

    def edge_key(edge):
        return (
            edge["source"],
            edge["target"],
            edge.get("relation"),
        )

    old_edges = {
        edge_key(edge)
        for edge in old_snapshot["edges"]
    }

    new_edges = {
        edge_key(edge)
        for edge in new_snapshot["edges"]
    }

    added_edges = sorted(new_edges - old_edges)
    removed_edges = sorted(old_edges - new_edges)

    return {
        "old_snapshot_id": old_snapshot_id,
        "new_snapshot_id": new_snapshot_id,
        "old_timestamp": old_snapshot["timestamp"],
        "new_timestamp": new_snapshot["timestamp"],
        "added_nodes": added_nodes,
        "removed_nodes": removed_nodes,
        "modified_nodes": modified_nodes,
        "added_edges": added_edges,
        "removed_edges": removed_edges,
    }