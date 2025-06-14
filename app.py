from os import environ

import aws_cdk as cdk

from iac import stacks

app = cdk.App()

local_environment = cdk.Environment(
    account=environ["AWS_ACCOUNT_ID"],
    region=app.node.get_context("@iac/region"),
)

stacks.Pipeline(
    app,
    "Pipeline",
    domain_name=app.node.get_context("@iac/domain-name"),
    env=local_environment,
    github_repository=app.node.get_context("@iac/github-repository"),
)

app.synth()
