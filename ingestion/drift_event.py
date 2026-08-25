def create_drift_events(exposures):
    """
    Convert detected public ingress exposures into
    standard AeroDrift drift events.
    """

    drift_events = []

    for exposure in exposures:
        drift_event = {
            "event_type": "PUBLIC_INGRESS",
            "resource_type": "SECURITY_GROUP",
            "resource_id": exposure.get("security_group_id"),
            "severity": "CRITICAL",
            "cidr": exposure.get("cidr"),
            "protocol": exposure.get("protocol"),
            "from_port": exposure.get("from_port"),
            "to_port": exposure.get("to_port"),
        }

        drift_events.append(drift_event)

    return drift_events