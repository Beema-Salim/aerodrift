from ingestion.aws_client import get_ec2_client
from remediation.remediation_engine import build_remediation
from remediation.executor import execute_remediation_ast


def handle_drift_event(drift_event, ec2_client=None):
    """
    Handle a validated drift event and execute remediation.
    """

    if ec2_client is None:
        ec2_client = get_ec2_client()

    ast_tree = build_remediation(drift_event)

    execute_remediation_ast(
        ast_tree,
        ec2_client,
    )

    return {
        "status": "remediated",
        "resource_id": drift_event["resource_id"],
        "event_type": drift_event["event_type"],
    }