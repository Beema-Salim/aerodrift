from .action_validator import validate_drift_event
from .ast_generator import generate_revoke_ingress_ast


def build_remediation(drift_event):
    """
    Validate a drift event and build the remediation AST.
    """

    if not validate_drift_event(drift_event):
        raise ValueError("Unsupported or unsafe drift event")

    return generate_revoke_ingress_ast(drift_event)