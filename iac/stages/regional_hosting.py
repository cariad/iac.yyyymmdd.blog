from typing import Any

import aws_cdk as cdk
from constructs import Construct

from iac import stacks


class RegionalHosting(cdk.Stage):
    """
    Regional hosting.

    The given domain name will be applied only when a certificate is also
    provided. Without a certificate, a random CloudFront domain name will be
    used regardless of any explicitly requested domain name.

    Args:
        scope: Scope.
        construct_id: Construct ID.
        domain_name: Domain name.
        certificate_arn: ARN of the TLS/HTTPS certificate.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
        certificate_arn: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stacks.Hosting(
            self,
            "HostingStack",
            certificate_arn=certificate_arn,
            domain_name=domain_name,
        )
