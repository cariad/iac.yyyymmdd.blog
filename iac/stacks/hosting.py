from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_cloudfront as cf
import aws_cdk.aws_cloudfront_origins as cfo
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_ssm as ssm
from constructs import Construct


class Hosting(cdk.Stack):
    """
    Static site hosting.

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

        certificate_arn = ssm.StringParameter.value_for_string_parameter(
            self,
            certificate_parameter_name,
        )

        certificate = acm.Certificate.from_certificate_arn(
            self,
            f"{construct_id}-Certificate",
            certificate_arn,
        )

        cf.Distribution(
            self,
            f"{construct_id}-Distribution",
            certificate=certificate,
            default_behavior=default_distribution_behavior,
            default_root_object="index.html",
            domain_names=[
                domain_name,
                f"www.{domain_name}",
            ],
        )
