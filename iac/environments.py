import aws_cdk as cdk
from boto3 import Session


def account_id(session: Session) -> str:
    """
    Amazon Web Services account ID.

    Args:
        session: Boto3 session.

    Returns:
        Account ID.
    """

    sts = session.client("sts")
    return sts.get_caller_identity()["Account"]


def local_environment(account_id: str) -> cdk.Environment:
    """
    Environment to deploy hosting infrastructure to. This is the region that
    website files will be held in.

    Args:
        account_id: Amazon Web Services account ID.

    Returns:
        Environment.
    """

    return cdk.Environment(
        account=account_id,
        region="eu-west-1",
    )
