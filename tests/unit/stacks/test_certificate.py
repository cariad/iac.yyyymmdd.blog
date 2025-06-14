import aws_cdk as cdk
from pytest import fixture

from iac import stacks
from tests import testing


@fixture
def template(app: cdk.App) -> cdk.assertions.Template:
    stack = stacks.Certificate(
        app,
        "Certificate",
        domain_name="robert.pringles",
        env=testing.test_environment(),
    )

    return cdk.assertions.Template.from_stack(stack)


def test(template: cdk.assertions.Template) -> None:
    template.has_resource_properties(
        "AWS::CertificateManager::Certificate",
        {
            "DomainName": "robert.pringles",
            "SubjectAlternativeNames": [
                "www.robert.pringles",
            ],
            "ValidationMethod": "DNS",
        },
    )
