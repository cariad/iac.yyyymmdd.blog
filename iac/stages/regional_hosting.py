from typing import Any

import aws_cdk as cdk
from constructs import Construct

from iac import stacks


class RegionalHosting(cdk.Stage):
    """
    Regional hosting.

    Args:
        scope: Scope.
        construct_id: Construct ID.
        certificate_parameter_name: Name of the Systems Manager Parameter that
            the ARN of the TLS/HTTPS certificate is recorded in.
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

        stacks.Hosting(
            self,
            "HostingStack",
            certificate_parameter_name=certificate_parameter_name,
            domain_name=domain_name,
        )
