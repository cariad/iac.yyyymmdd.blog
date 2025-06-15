from unittest.mock import Mock

import aws_cdk as cdk

from iac import environments


def test_account_id(client: Mock, session: Mock) -> None:
    get_caller_identity = Mock(return_value={"Account": "000000000"})
    client.get_caller_identity = get_caller_identity
    account_id = environments.account_id(session)
    assert account_id == "000000000"


def test_local_environment() -> None:
    env = environments.local_environment("000000000")

    assert env == cdk.Environment(
        account="000000000",
        region="eu-west-1",
    )
