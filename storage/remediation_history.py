import sqlite3
from datetime import datetime

from .history_db import DB_PATH


def initialize_remediation_table():
    """
    Create the remediation_logs table if it does not exist.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS remediation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            resource_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT,
            status TEXT NOT NULL,
            report_path TEXT,
            error_message TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def save_remediation_log(
    drift_event,
    status,
    report_path=None,
    error_message=None,
):
    """
    Save a remediation attempt/result into SQLite.
    """
    initialize_remediation_table()

    timestamp = datetime.now().isoformat()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO remediation_logs (
            timestamp,
            resource_id,
            event_type,
            severity,
            status,
            report_path,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            drift_event.get("resource_id"),
            drift_event.get("event_type"),
            drift_event.get("severity"),
            status,
            report_path,
            error_message,
        ),
    )

    log_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "log_id": log_id,
        "timestamp": timestamp,
        "resource_id": drift_event.get("resource_id"),
        "status": status,
    }


def get_remediation_logs(limit=20):
    """
    Return the latest remediation logs.
    """
    initialize_remediation_table()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            timestamp,
            resource_id,
            event_type,
            severity,
            status,
            report_path,
            error_message
        FROM remediation_logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    logs = [
        {
            "log_id": row[0],
            "timestamp": row[1],
            "resource_id": row[2],
            "event_type": row[3],
            "severity": row[4],
            "status": row[5],
            "report_path": row[6],
            "error_message": row[7],
        }
        for row in cursor.fetchall()
    ]

    connection.close()

    return logs