import aws_cdk as cdk

from iac import stacks

app = cdk.App()

local_environment = cdk.Environment(
    region="eu-west-1",
)

stacks.Pipeline(
    app,
    "yyyymmddblog",
    env=local_environment,
    pipeline_name="yyyymmddblog",
)

app.synth()
