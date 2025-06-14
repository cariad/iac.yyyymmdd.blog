import aws_cdk as cdk
from pytest import fixture

from iac import stacks


@fixture
def template(app: cdk.App) -> cdk.assertions.Template:
    stack = stacks.Pipeline(
        app,
        "Pipeline",
        domain_name="robert.pringles",
        github_repository="cariad/robert.pringles",
    )

    return cdk.assertions.Template.from_stack(stack)


def test(template: cdk.assertions.Template) -> None:
    template.resource_count_is("AWS::CodePipeline::Pipeline", 1)
