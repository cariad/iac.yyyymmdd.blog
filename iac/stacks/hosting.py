from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_cloudfront as cf
import aws_cdk.aws_cloudfront_origins as cfo
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

        bucket = s3.Bucket(
            self,
            f"{construct_id}-Bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        distribution_origin = cfo.S3BucketOrigin.with_origin_access_control(
            bucket,
        )

        default_distribution_behavior = cf.BehaviorOptions(
            origin=distribution_origin,
            viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        )

        cf.Distribution(
            self,
            f"{construct_id}-Distribution",
            default_behavior=default_distribution_behavior,
            default_root_object="index.html",
        )
