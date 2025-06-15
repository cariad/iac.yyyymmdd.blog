import aws_cdk as cdk
from boto3 import Session

from iac import environments, stacks

PROJECT_NAME = "yyyymmddblog"

session = Session()
account = environments.account_id(session)

app = cdk.App()

ssm = session.client("ssm", region_name="us-east-1")
certificate_arn: str | None = None
certificate_parameter_name = f"/{PROJECT_NAME}/certificate"

try:
    certificate_parameter = ssm.get_parameter(Name=certificate_parameter_name)
    certificate_arn = certificate_parameter["Parameter"].get("Value")
except ssm.exceptions.ParameterNotFound:
    pass

stacks.Pipeline(
    app,
    PROJECT_NAME,
    certificate_arn=certificate_arn,
    certificate_parameter_name=certificate_parameter_name,
    domain_name="yyyymmdd.blog",
    env=environments.local_environment(account),
    pipeline_name=PROJECT_NAME,
)

app.synth()
