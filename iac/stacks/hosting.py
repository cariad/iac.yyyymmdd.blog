from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_cloudfront as cf
import aws_cdk.aws_cloudfront_origins as cfo
import aws_cdk.aws_s3 as s3
from constructs import Construct


class Hosting(cdk.Stack):
    """
    Static site hosting.

    Args:
        scope: Scope.
        construct_id: Construct ID.
        domain_name: Domain name. The domain name will be applied to the
            distribution only if the optional certificate ARN is provided.
        certificate_arn: ARN of the TLS/HTTP certificate. The domain name will
            be ignored if this is omitted.
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

        certificate = (
            acm.Certificate.from_certificate_arn(
                self,
                f"{construct_id}-Certificate",
                certificate_arn,
            )
            if certificate_arn
            else None
        )

        # CloudFront won't allow domain aliases without a certificate.
        domain_names = (
            [
                domain_name,
                f"www.{domain_name}",
            ]
            if certificate_arn
            else None
        )

        cf.Distribution(
            self,
            f"{construct_id}-Distribution",
            certificate=certificate,
            default_behavior=default_distribution_behavior,
            default_root_object="index.html",
            domain_names=domain_names,
        )
