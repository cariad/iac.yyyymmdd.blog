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
def get_parameter(client: Mock) -> Mock:
    func = Mock(side_effect=Exception())
    client.get_parameter = func

    exceptions = Mock()
    exceptions.ParameterNotFound = Exception
    client.exceptions = exceptions

    return func


@fixture
def session() -> Mock:
    return Mock()
