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

def find_changed_resources(previous_snapshot, current_snapshot):
    """
    Find the exact AWS resources that changed between
    two snapshots.
    """

    previous_resources = previous_snapshot.get("resources", {})
    current_resources = current_snapshot.get("resources", {})

    changes = []

    all_resource_types = set(previous_resources) | set(current_resources)

    for resource_type in all_resource_types:
        previous_list = previous_resources.get(resource_type, [])
        current_list = current_resources.get(resource_type, [])

        previous_map = {
            resource.get("resource_id"): resource
            for resource in previous_list
            if resource.get("resource_id")
        }

        current_map = {
            resource.get("resource_id"): resource
            for resource in current_list
            if resource.get("resource_id")
        }

        all_ids = set(previous_map) | set(current_map)

        for resource_id in all_ids:
            previous = previous_map.get(resource_id)
            current = current_map.get(resource_id)

            if previous != current:
                changes.append(
                    {
                        "resource_type": resource_type,
                        "resource_id": resource_id,
                        "change_type": (
                            "ADDED"
                            if previous is None
                            else "REMOVED"
                            if current is None
                            else "MODIFIED"
                        ),
                    }
                )

    return changes