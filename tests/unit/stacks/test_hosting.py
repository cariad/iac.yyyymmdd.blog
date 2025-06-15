import aws_cdk as cdk
from pytest import fixture

from iac import stacks


@fixture
def template(app: cdk.App) -> cdk.assertions.Template:
    stack = stacks.Hosting(app, "Hosting")
    return cdk.assertions.Template.from_stack(stack)


def test_bucket(template: cdk.assertions.Template) -> None:
    template.has_resource_properties("AWS::S3::Bucket", {})
