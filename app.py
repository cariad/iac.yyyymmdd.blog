import aws_cdk as cdk
from boto3 import Session

from iac import certificates, environments, stacks

DOMAIN_NAME = "yyyymmdd.blog"

session = Session()
account = environments.account_id(session)
certificate_arn = certificates.try_get_certificate_arn(session, DOMAIN_NAME)

app = cdk.App()

stacks.Pipeline(
    app,
    "yyyymmddblog",
    certificate_arn=certificate_arn,
    domain_name=DOMAIN_NAME,
    env=environments.local_environment(account),
    pipeline_name="yyyymmddblog",
)

app.synth()
