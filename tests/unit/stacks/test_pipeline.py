import aws_cdk as cdk
from pytest import fixture

from iac import stacks
from tests import testing


@fixture
def template(app: cdk.App) -> cdk.assertions.Template:
    stack = stacks.Pipeline(
        app,
        "Pipeline",
        domain_name="robert.pringles",
        env=testing.test_environment(),
    )

    return cdk.assertions.Template.from_stack(stack)


def test_pipeline(template: cdk.assertions.Template) -> None:
    template.has_resource_properties(
        "AWS::CodePipeline::Pipeline",
        {
            "Stages": [
                {
                    "Actions": [
                        {
                            "Configuration": {
                                "Branch": "main",
                            },
                        }
                    ],
                    "Name": "Source",
                },
                {"Name": "Build"},
                {"Name": "UpdatePipeline"},
                {"Name": "Pipeline-GlobalBootstrap"},
                {"Name": "Pipeline-RegionalHosting"},
            ],
        },
    )


def test_synthesis_policy(template: cdk.assertions.Template) -> None:
    template.has_resource_properties(
        "AWS::IAM::Policy",
        {
            "PolicyDocument": {
                "Statement": cdk.assertions.Match.array_with(
                    [
                        {
                            "Action": [
                                "acm:ListCertificates",
                                "route53:ListHostedZonesByName",
                            ],
                            "Effect": "Allow",
                            "Resource": "*",
                        },
                    ],
                ),
            },
        },
    )
