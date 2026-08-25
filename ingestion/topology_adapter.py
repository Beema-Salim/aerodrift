def normalize_resources(data):
    """
    Convert AWS ingestion data into the format expected by
    the AeroDrift topology engine.
    """

    resources = []

    for resource_group in data.values():
        for resource in resource_group:

            resource_type = resource.get("resource_type")
            resource_id = resource.get("resource_id")

            if not resource_id:
                continue

            normalized = {
                "id": resource_id,
                "type": resource_type,
                "name": resource.get("name"),
                "metadata": resource.copy(),
            }

            # Topology relationships
            if resource_type == "SUBNET":
                normalized["type"] = "Subnet"
                normalized["vpc_id"] = resource.get("vpc_id")

            elif resource_type == "EC2":
                normalized["type"] = "EC2"

                if resource.get("subnet_id"):
                    normalized["subnet_id"] = resource.get("subnet_id")

                if resource.get("security_group_ids"):
                    normalized["security_group_ids"] = resource.get(
                        "security_group_ids"
                    )

            elif resource_type == "SECURITY_GROUP":
                normalized["type"] = "SecurityGroup"

            elif resource_type == "VPC":
                normalized["type"] = "VPC"

            resources.append(normalized)

    return resources