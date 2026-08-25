def find_public_ingress(security_groups):
    """
    Find security group inbound rules that allow traffic
    from the public IPv4 internet.
    """

    exposures = []

    for security_group in security_groups:
        security_group_id = security_group.get("resource_id")

        for rule in security_group.get("inbound_rules", []):
            for ip_range in rule.get("IpRanges", []):

                if ip_range.get("CidrIp") == "0.0.0.0/0":
                    exposures.append(
                        {
                            "security_group_id": security_group_id,
                            "protocol": rule.get("IpProtocol"),
                            "from_port": rule.get("FromPort"),
                            "to_port": rule.get("ToPort"),
                            "cidr": "0.0.0.0/0",
                        }
                    )

    return exposures