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
        domain_name: Domain name.
        env: Environment. Must have an explicit account.
        pipeline_name: Pipeline name.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
        env: cdk.Environment,
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
            stages.RegionalHosting(self, f"{construct_id}-RegionalHosting")
        )

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
