from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct

from iac import stages


class Pipeline(cdk.Stack):
    """
    Build and deployment pipeline.

    Args:
        scope: Scope.
        construct_id: Construct ID.
        certificate_parameter_name: Name of the Systems Manager Parameter to
            record the certificate ARN in.
        domain_name: Domain name.
        env: Environment. Must have an explicit account.
        certificate_arn: ARN of the TLS/HTTPS certificate.
        pipeline_name: Pipeline name.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        certificate_parameter_name: str,
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
                    "share-certificate",
                    trigger=cdk.aws_codepipeline_actions.GitHubTrigger.NONE,
                ),
            ),
        )

        if not env.account:
            raise ValueError("Pipeline `env` must have an explicit account")

        bootstrap_stage = stages.GlobalBootstrap(
            self,
            f"{construct_id}-GlobalBootstrap",
            account=env.account,
            certificate_parameter_name=certificate_parameter_name,
            domain_name=domain_name,
        )

        pipeline.add_stage(bootstrap_stage)

        regional_hosting_stage = stages.RegionalHosting(
            self,
            f"{construct_id}-RegionalHosting",
            certificate_arn=certificate_arn,
            domain_name=domain_name,
        )

        pipeline.add_stage(regional_hosting_stage)

        pipeline.build_pipeline()

        pipeline.synth_project.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "route53:ListHostedZonesByName",
                ],
                resources=[
                    "*",
                ],
            ),
        )
