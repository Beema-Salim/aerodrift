from datetime import datetime, timezone


def create_state_snapshot(resources):
    """
    Create a timestamped snapshot of the current
    AWS resource state.
    """

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resources": resources,
    }
def compare_snapshots(previous_snapshot, current_snapshot):
    """
    Compare two AWS resource snapshots and return
    which resource groups changed.
    """

    previous_resources = previous_snapshot.get("resources", {})
    current_resources = current_snapshot.get("resources", {})

    changed_resources = []

    all_resource_types = set(previous_resources) | set(current_resources)

    for resource_type in all_resource_types:
        previous = previous_resources.get(resource_type, [])
        current = current_resources.get(resource_type, [])

        if previous != current:
            changed_resources.append(resource_type)

    return changed_resources