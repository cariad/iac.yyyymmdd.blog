from os import environ

import aws_cdk as cdk

from iac import stacks

app = cdk.App()

local_environment = cdk.Environment(
    account=environ["AWS_ACCOUNT_ID"],
    region="eu-west-1",
)

stacks.Pipeline(
    app,
    "yyyymmddblog",
    env=local_environment,
    pipeline_name="yyyymmddblog",
)

app.synth()
