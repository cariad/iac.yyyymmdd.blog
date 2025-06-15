import aws_cdk as cdk


def test_environment() -> cdk.Environment:
    return cdk.Environment(
        account="000000000",
        region="sa-west-1",
    )
