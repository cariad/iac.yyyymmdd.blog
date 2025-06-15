from unittest.mock import Mock

import aws_cdk as cdk
from pytest import fixture

from iac import stacks


@fixture
def template(app: cdk.App) -> cdk.assertions.Template:
    stack = stacks.Hosting(
        app,
        "Hosting",
        certificate_parameter_name="/pringles/certificate",
        domain_name="robert.pringles",
    )

    return cdk.assertions.Template.from_stack(stack)


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


def test_distribution(template: cdk.assertions.Template) -> None:
    template.has_resource_properties(
        "AWS::CloudFront::Distribution",
        {
            "DistributionConfig": {
                "DefaultCacheBehavior": {
                    "ViewerProtocolPolicy": "redirect-to-https",
                },
                "DefaultRootObject": "index.html",
            }
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
