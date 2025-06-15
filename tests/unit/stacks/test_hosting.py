from typing import Any

import aws_cdk as cdk
from pytest import fixture, mark

from iac import stacks


def make_template(
    app: cdk.App,
    certificate_arn: str | None = None,
) -> cdk.assertions.Template:
    stack = stacks.Hosting(
        app,
        "Hosting",
        certificate_arn=certificate_arn,
        domain_name="robert.pringles",
    )

    return cdk.assertions.Template.from_stack(stack)


@fixture
def template(app: cdk.App) -> cdk.assertions.Template:
    return make_template(app)


def test_bucket(template: cdk.assertions.Template) -> None:
    template.has_resource(
        "AWS::S3::Bucket",
        {
            "UpdateReplacePolicy": "Delete",
            "DeletionPolicy": "Delete",
        },
    )


def test_bucket_policy(template: cdk.assertions.Template) -> None:
    template.has_resource_properties(
        "AWS::S3::BucketPolicy",
        {
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": "s3:GetObject",
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "cloudfront.amazonaws.com",
                        },
                    }
                ],
            },
        },
    )


@mark.parametrize(
    "certificate_arn",
    [
        None,
        "arn:aws:ssm:us-east-1:000000000000:certificate/foo",
    ],
)
def test_distribution(app: cdk.App, certificate_arn: str | None) -> None:
    template = make_template(app, certificate_arn=certificate_arn)

    aliases = (
        [
            "robert.pringles",
            "www.robert.pringles",
        ]
        if certificate_arn
        else cdk.assertions.Match.absent()
    )

    viewer_certificate = (
        {
            "AcmCertificateArn": certificate_arn,
            "MinimumProtocolVersion": "TLSv1.2_2021",
            "SslSupportMethod": "sni-only",
        }
        if certificate_arn
        else cdk.assertions.Match.absent()
    )

    template.has_resource_properties(
        "AWS::CloudFront::Distribution",
        {
            "DistributionConfig": {
                "Aliases": aliases,
                "DefaultCacheBehavior": {
                    "ViewerProtocolPolicy": "redirect-to-https",
                },
                "DefaultRootObject": "index.html",
                "ViewerCertificate": viewer_certificate,
            },
        },
    )


def test_origin_access_control(template: cdk.assertions.Template) -> None:
    template.has_resource_properties(
        "AWS::CloudFront::OriginAccessControl",
        {
            "OriginAccessControlConfig": {
                "OriginAccessControlOriginType": "s3",
                "SigningBehavior": "always",
                "SigningProtocol": "sigv4",
            },
        },
    )
