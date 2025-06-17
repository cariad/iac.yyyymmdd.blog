from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct

from iac import stages


class Pipeline(cdk.Stack):
    """
    Build and deployment pipeline.

    The given domain name will be applied only when a certificate is also
    provided. Without a certificate, a random CloudFront domain name will be
    used regardless of any explicitly requested domain name.

    Args:
        scope: Scope.
        construct_id: Construct ID.
        domain_name: Domain name.
        env: Environment. Must have an explicit account.
        certificate_arn: ARN of the TLS/HTTPS certificate.
        pipeline_name: Pipeline name.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
        env: cdk.Environment,
        certificate_arn: str | None = None,
        pipeline_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)

        pipeline = cdk.pipelines.CodePipeline(
            self,
            f"{construct_id}-Pipeline",
            pipeline_name=pipeline_name,
            synth=cdk.pipelines.ShellStep(
                "Synthesise",
                commands=[
                    "npm install -g aws-cdk",
                    "pip3 install -r requirements.txt",
                    "cdk synth",
                ],
                input=cdk.pipelines.CodePipelineSource.git_hub(
                    "cariad/iac.yyyymmdd.blog",
                    "main",
                    trigger=cdk.aws_codepipeline_actions.GitHubTrigger.NONE,
                ),
            ),
        )

        if not env.account:
            raise ValueError("Pipeline `env` must have an explicit account")

        pipeline.add_stage(
            stages.GlobalBootstrap(
                self,
                f"{construct_id}-GlobalBootstrap",
                account=env.account,
                domain_name=domain_name,
            )
        )

        pipeline.add_stage(
            stages.RegionalHosting(
                self,
                f"{construct_id}-RegionalHosting",
                certificate_arn=certificate_arn,
                domain_name=domain_name,
                env=env,
            )
        )

        pipeline.build_pipeline()

        pipeline.synth_project.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "acm:ListCertificates",
                    "route53:ListHostedZonesByName",
                ],
                resources=[
                    "*",
                ],
            ),
        )
