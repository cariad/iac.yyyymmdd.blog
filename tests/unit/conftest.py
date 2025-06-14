import aws_cdk as cdk
from pytest import fixture


@fixture
def app() -> cdk.App:
    return cdk.App()
