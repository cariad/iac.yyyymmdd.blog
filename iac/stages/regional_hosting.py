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
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stacks.Hosting(self, "HostingStack")
