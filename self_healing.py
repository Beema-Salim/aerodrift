from ingestion.aws_client import get_ec2_client
from remediation.remediation_engine import build_remediation
from remediation.executor import execute_remediation_ast
from reports.incident_report import generate_incident_report
from storage.remediation_history import save_remediation_log


def handle_drift_event(drift_event, ec2_client=None):
    """
    Handle a validated drift event, execute remediation,
    generate an incident PDF report, and store the result
    in the SQLite remediation history.
    """

    try:
        if ec2_client is None:
            ec2_client = get_ec2_client()

        ast_tree = build_remediation(drift_event)

        execute_remediation_ast(
            ast_tree,
            ec2_client,
        )

        remediation_result = {
            "status": "remediated",
            "resource_id": drift_event["resource_id"],
            "event_type": drift_event["event_type"],
        }

        report_path = generate_incident_report(
            drift_event,
            remediation_result,
        )

        remediation_result["report_path"] = report_path

        log = save_remediation_log(
            drift_event,
            status="REMEDIATED",
            report_path=report_path,
        )

        remediation_result["log_id"] = log["log_id"]

        return remediation_result

    except Exception as error:
        save_remediation_log(
            drift_event,
            status="FAILED",
            error_message=str(error),
        )

        raise