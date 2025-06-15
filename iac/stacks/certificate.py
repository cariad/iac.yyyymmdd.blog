from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_route53 as route53
import aws_cdk.aws_ssm as ssm
from constructs import Construct


class Certificate(cdk.Stack):
    """
    TLS/HTTPS certificate.

    This stack, or its parent stage, must have an explicit account and region
    specified in its environment to support the Hosted Zone lookup.

    Args:
        scope: Scope.
        construct_id: Construct ID.
        certificate_parameter_name: Name of the Systems Manager Parameter to
            record the certificate ARN in.
        domain_name: Domain name.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        certificate_parameter_name: str,
        domain_name: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hosted_zone = route53.HostedZone.from_lookup(
            self,
            f"{construct_id}-HostedZone",
            domain_name=domain_name,
        )

        certificate = acm.Certificate(
            self,
            f"{construct_id}-Certificate",
            domain_name=domain_name,
            subject_alternative_names=[
                f"www.{domain_name}",
            ],
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        ssm.StringParameter(
            self,
            f"{construct_id}-CertificateParameter",
            parameter_name=certificate_parameter_name,
            string_value=certificate.certificate_arn,
        )
