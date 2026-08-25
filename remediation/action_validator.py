def validate_drift_event(drift_event):
    """
    Validate whether a drift event is safe and supported
    for automatic remediation.
    """

    required_fields = {
        "event_type",
        "resource_type",
        "resource_id",
        "cidr",
        "protocol",
        "from_port",
        "to_port",
    }

    if not required_fields.issubset(drift_event.keys()):
        return False

    if drift_event["event_type"] != "PUBLIC_INGRESS":
        return False

    if drift_event["resource_type"] != "SECURITY_GROUP":
        return False

    if drift_event["cidr"] not in {"0.0.0.0/0", "::/0"}:
        return False

    if not drift_event["resource_id"].startswith("sg-"):
        return False

    if drift_event["from_port"] is None or drift_event["to_port"] is None:
        return False

    return True
