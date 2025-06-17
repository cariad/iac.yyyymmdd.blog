from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_cloudfront as cf
import aws_cdk.aws_cloudfront_origins as cfo
import aws_cdk.aws_route53 as route53
import aws_cdk.aws_route53_targets as route53_targets
import aws_cdk.aws_s3 as s3
from constructs import Construct


class Hosting(cdk.Stack):
    """
    Static site hosting.

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

        distribution = cf.Distribution(
            self,
            f"{construct_id}-Distribution",
            certificate=certificate,
            default_behavior=default_distribution_behavior,
            default_root_object="index.html",
            domain_names=domain_names,
        )

        distribution_target = route53_targets.CloudFrontTarget(distribution)
        record_target = route53.RecordTarget.from_alias(distribution_target)

        hosted_zone = route53.HostedZone.from_lookup(
            self,
            f"{construct_id}-HostedZone",
            domain_name=domain_name,
        )

        self._add_dns(hosted_zone, record_target)
        self._add_dns(hosted_zone, record_target, subdomain="www")

    def _add_dns(
        self,
        hosted_zone: route53.IHostedZone,
        target: route53.RecordTarget,
        subdomain: str | None = None,
    ) -> None:
        """
        Adds IPv4 and IPv6 domain records for a given target.

        Args:
            hosted_zone: Hosted Zone.
            target: Record target.
            subdomain: Optional subdomain.
        """

        name = subdomain.capitalize() if subdomain else "Root"

        route53.ARecord(
            self,
            f"{self.node.id}-{name}ARecord",
            record_name=subdomain,
            target=target,
            zone=hosted_zone,
        )

        route53.AaaaRecord(
            self,
            f"{self.node.id}-{name}AaaaRecord",
            record_name=subdomain,
            target=target,
            zone=hosted_zone,
        )
