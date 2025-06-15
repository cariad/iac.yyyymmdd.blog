from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
from constructs import Construct


class Hosting(cdk.Stack):
    """
    Static site hosting.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3.Bucket(
            self,
            f"{construct_id}-Bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
