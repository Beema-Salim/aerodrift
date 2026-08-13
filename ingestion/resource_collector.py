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


def collect_vpcs():
    """
    Collect VPC information from AWS.
    """

    ec2 = get_ec2_client()

    response = ec2.describe_vpcs()

    vpcs = []

    for vpc in response.get("Vpcs", []):

        vpc_data = {
            "resource_type": "VPC",
            "resource_id": vpc.get("VpcId"),
            "region": ec2.meta.region_name,
            "state": vpc.get("State"),
            "cidr_block": vpc.get("CidrBlock"),
            "is_default": vpc.get("IsDefault"),
        }

        vpcs.append(vpc_data)

    return vpcs

def collect_subnets():
    """
    Collect subnet information from AWS.
    """

    ec2 = get_ec2_client()

    response = ec2.describe_subnets()

    subnets = []

    for subnet in response.get("Subnets", []):

        subnet_data = {
            "resource_type": "SUBNET",
            "resource_id": subnet.get("SubnetId"),
            "region": ec2.meta.region_name,
            "state": subnet.get("State"),
            "vpc_id": subnet.get("VpcId"),
            "cidr_block": subnet.get("CidrBlock"),
            "availability_zone": subnet.get("AvailabilityZone"),
        }

        subnets.append(subnet_data)

    return subnets

def collect_security_groups():
    """
    Collect security group information from AWS.
    """

    ec2 = get_ec2_client()

    response = ec2.describe_security_groups()

    security_groups = []

    for group in response.get("SecurityGroups", []):

        security_group_data = {
            "resource_type": "SECURITY_GROUP",
            "resource_id": group.get("GroupId"),
            "region": ec2.meta.region_name,
            "name": group.get("GroupName"),
            "description": group.get("Description"),
            "vpc_id": group.get("VpcId"),
            "inbound_rules": group.get("IpPermissions", []),
            "outbound_rules": group.get("IpPermissionsEgress", []),
        }

        security_groups.append(security_group_data)

    return security_groups

def collect_route_tables():
    """
    Collect route table information from AWS.
    """

    ec2 = get_ec2_client()

    response = ec2.describe_route_tables()

    route_tables = []

    for route_table in response.get("RouteTables", []):

        route_table_data = {
            "resource_type": "ROUTE_TABLE",
            "resource_id": route_table.get("RouteTableId"),
            "region": ec2.meta.region_name,
            "vpc_id": route_table.get("VpcId"),
            "routes": route_table.get("Routes", []),
            "associations": route_table.get("Associations", []),
        }

        route_tables.append(route_table_data)

    return route_tables

def collect_internet_gateways():
    """
    Collect internet gateway information from AWS.
    """

    ec2 = get_ec2_client()

    response = ec2.describe_internet_gateways()

    internet_gateways = []

    for gateway in response.get("InternetGateways", []):

        gateway_data = {
            "resource_type": "INTERNET_GATEWAY",
            "resource_id": gateway.get("InternetGatewayId"),
            "region": ec2.meta.region_name,
            "attachments": gateway.get("Attachments", []),
        }

        internet_gateways.append(gateway_data)

    return internet_gateways