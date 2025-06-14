import aws_cdk as cdk
from pytest import fixture

from iac import stacks


@fixture
def template(app: cdk.App) -> cdk.assertions.Template:
    stack = stacks.Pipeline(app, "Pipeline")
    return cdk.assertions.Template.from_stack(stack)


def test(template: cdk.assertions.Template) -> None:
    template.has_resource_properties(
        "AWS::CodePipeline::Pipeline",
        {
            "Stages": [
                {"Name": "Source"},
                {"Name": "Build"},
                {"Name": "UpdatePipeline"},
            ],
        },
    )
