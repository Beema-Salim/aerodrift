from .graph_builder import GraphBuilder


resources = [
    {
        "id": "vpc-001",
        "type": "VPC",
        "name": "main-vpc",
    },
    {
        "id": "subnet-001",
        "type": "Subnet",
        "name": "public-subnet",
        "vpc_id": "vpc-001",
    },
    {
        "id": "ec2-001",
        "type": "EC2",
        "name": "web-server",
        "subnet_id": "subnet-001",
        "security_group_ids": ["sg-001"],
    },
    {
        "id": "sg-001",
        "type": "SecurityGroup",
        "name": "web-sg",
    },
]


if __name__ == "__main__":
    builder = GraphBuilder()
    builder.build(resources)

    print("NODES:")
    for node in builder.get_nodes():
        print(node)

    print("\nEDGES:")
    for edge in builder.get_edges():
        print(edge)

    print("\nGRAPH JSON:")
    print(builder.to_dict())
