from unittest.mock import Mock

import aws_cdk as cdk
from pytest import fixture


@fixture
def app() -> cdk.App:
    return cdk.App()


@fixture
def client(session: Mock) -> Mock:
    client = Mock()
    session.client = Mock(return_value=client)
    return client


@fixture
def session() -> Mock:
    return Mock()
