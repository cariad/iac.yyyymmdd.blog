from typing import Any

import aws_cdk as cdk
from constructs import Construct

from iac import stacks


class GlobalBootstrap(cdk.Stage):
    """
    Global bootstrap.

    Regardless of any specified environment, this stack will always be deploy
    to us-east-1.

    Args:
        scope: Scope.
        construct_id: Construct ID.
        account: Amazon Web Services account ID.
        domain_name: Domain name.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        account: str,
        domain_name: str,
        **kwargs: Any,
    ) -> None:
        global_environment = cdk.Environment(
            account=account,
            region="us-east-1",
        )

        super().__init__(
            scope,
            construct_id,
            env=global_environment,
            **kwargs,
        )

        stacks.Certificate(
            self,
            "CertificateStack",
            domain_name=domain_name,
        )
