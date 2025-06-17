import aws_cdk as cdk
from pytest import fixture

from iac import stages
from tests import testing


@fixture
def stage(app: cdk.App) -> stages.RegionalHosting:
    return stages.RegionalHosting(
        app,
        "RegionalHosting",
        domain_name="robert.pringles",
        env=testing.test_environment(),
    )


def test_child_count(stage: stages.RegionalHosting) -> None:
    assert len(stage.node.children) == 1


def test_has_hosting_stack(stage: stages.RegionalHosting) -> None:
    assert stage.node.find_child("HostingStack")
