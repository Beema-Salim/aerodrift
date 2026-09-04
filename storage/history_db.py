import json
import sqlite3
from datetime import datetime


DB_PATH = "storage/aerodrift_history.db"


def initialize_database():
    """
    Create SQLite database and graph_snapshots table.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS graph_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            nodes TEXT NOT NULL,
            edges TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_graph_snapshot(graph):
    """
    Save the current NetworkX graph state into SQLite.
    """
    initialize_database()

    nodes = [
        {
            "id": node_id,
            **data,
        }
        for node_id, data in graph.nodes(data=True)
    ]

    edges = [
        {
            "source": source,
            "target": target,
            **data,
        }
        for source, target, data in graph.edges(data=True)
    ]

    timestamp = datetime.now().isoformat()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO graph_snapshots (
            timestamp,
            nodes,
            edges
        )
        VALUES (?, ?, ?)
        """,
        (
            timestamp,
            json.dumps(nodes, default=str),
            json.dumps(edges, default=str),
        ),
    )

    snapshot_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "snapshot_id": snapshot_id,
        "timestamp": timestamp,
        "node_count": len(nodes),
        "edge_count": len(edges),
    }


def get_all_snapshots():
    """
    Return basic information about all stored snapshots.
    """
    initialize_database()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, timestamp
        FROM graph_snapshots
        ORDER BY id
        """
    )

    snapshots = [
        {
            "snapshot_id": row[0],
            "timestamp": row[1],
        }
        for row in cursor.fetchall()
    ]

    connection.close()

    return snapshots