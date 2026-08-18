import asyncio

from .resource_collector import (
    collect_ec2_instances,
    collect_vpcs,
    collect_subnets,
    collect_security_groups,
    collect_route_tables,
    collect_internet_gateways,
    collect_network_acls,
)


async def collect_all_resources_async():
    """
    Collect all AWS resources concurrently.
    """

    (
        ec2,
        vpcs,
        subnets,
        security_groups,
        route_tables,
        internet_gateways,
        network_acls,
    ) = await asyncio.gather(
        asyncio.to_thread(collect_ec2_instances),
        asyncio.to_thread(collect_vpcs),
        asyncio.to_thread(collect_subnets),
        asyncio.to_thread(collect_security_groups),
        asyncio.to_thread(collect_route_tables),
        asyncio.to_thread(collect_internet_gateways),
        asyncio.to_thread(collect_network_acls),
    )

    return {
        "ec2": ec2,
        "vpcs": vpcs,
        "subnets": subnets,
        "security_groups": security_groups,
        "route_tables": route_tables,
        "internet_gateways": internet_gateways,
        "network_acls": network_acls,
    }