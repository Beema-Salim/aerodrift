import boto3


def get_ec2_client():
    """
    Create and return a boto3 EC2 client.

    AWS credentials are loaded automatically by boto3
    from the configured AWS environment.
    """
    return boto3.client("ec2")
def get_rds_client():
    """
    Create and return a boto3 RDS client.

    AWS credentials are loaded automatically by boto3
    from the configured AWS environment.
    """
    return boto3.client("rds")