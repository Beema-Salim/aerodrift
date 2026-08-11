from .aws_client import get_ec2_client


def collect_ec2_instances():
    """
    Collect EC2 instance information from AWS.
    """

    ec2 = get_ec2_client()

    response = ec2.describe_instances()

    instances = []

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):

            instance_data = {
                "resource_type": "EC2",
                "resource_id": instance.get("InstanceId"),
                "region": ec2.meta.region_name,
                "state": instance.get("State", {}).get("Name"),
            }

            instances.append(instance_data)

    return instances