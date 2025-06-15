import aws_cdk as cdk
from pytest import fixture

from iac import stages


@fixture
def stage(app: cdk.App) -> stages.GlobalBootstrap:
    return stages.GlobalBootstrap(
        app,
        "GlobalBootstrap",
        account="000000000",
        domain_name="robert.pringles",
    )


def test_child_count(stage: stages.GlobalBootstrap) -> None:
    assert len(stage.node.children) == 1


def test_has_certificate(stage: stages.GlobalBootstrap) -> None:
    assert stage.node.find_child("GlobalBootstrap-Certificate")
