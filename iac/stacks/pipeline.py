from typing import Any

import aws_cdk as cdk
from constructs import Construct


class Pipeline(cdk.Stack):
    """
    Build and deployment pipeline.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
        github_repository: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cdk.pipelines.CodePipeline(
            self,
            "Pipeline",
            pipeline_name=domain_name,
            synth=cdk.pipelines.ShellStep(
                "Synthesise",
                commands=[
                    "npm install -g aws-cdk",
                    "pip3 install -r requirements.txt",
                    "cdk synth",
                ],
                input=cdk.pipelines.CodePipelineSource.git_hub(
                    github_repository,
                    "main",
                    trigger=cdk.aws_codepipeline_actions.GitHubTrigger.NONE,
                ),
            ),
        )
