import aws_cdk as cdk
from boto3 import Session

from iac import environments, stacks

session = Session()
account = environments.account_id(session)

app = cdk.App()

stacks.Pipeline(
    app,
    "yyyymmddblog",
    certificate_parameter_name="/yyyymmddblog/certificate",
    domain_name="yyyymmdd.blog",
    env=environments.local_environment(account),
    pipeline_name="yyyymmddblog",
)

app.synth()
