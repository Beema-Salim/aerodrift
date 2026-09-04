from rich.console import Console
from rich.table import Table

from .remediation_history import get_remediation_logs


console = Console()


def render_remediation_history(limit=5):
    """
    Display recent remediation history using a Rich table.
    """

    logs = get_remediation_logs(limit)

    if not logs:
        console.print(
            "[yellow]No remediation history available.[/yellow]"
        )
        return

    table = Table(
        title="Recent Remediation History"
    )

    table.add_column("ID")
    table.add_column("Timestamp")
    table.add_column("Resource")
    table.add_column("Event")
    table.add_column("Severity")
    table.add_column("Status")
    table.add_column("Report")

    for log in logs:
        status = log.get("status", "UNKNOWN")

        if status == "REMEDIATED":
            status_text = "[green]REMEDIATED[/green]"
        elif status == "FAILED":
            status_text = "[red]FAILED[/red]"
        else:
            status_text = f"[yellow]{status}[/yellow]"

        severity = log.get("severity") or "-"
        report_path = log.get("report_path") or "-"

        table.add_row(
            str(log.get("log_id")),
            str(log.get("timestamp")),
            str(log.get("resource_id")),
            str(log.get("event_type")),
            str(severity),
            status_text,
            str(report_path),
        )

    console.print(table)