from unittest.mock import Mock

from pytest import mark

from iac import certificates


@mark.parametrize(
    "domain_name, expect",
    [
        ("robert.pringles", "arn:robert.pringles"),
        ("foo", None),
    ],
)
def test_try_get_certificate_arn(
    domain_name: str,
    expect: str | None,
    client: Mock,
    session: Mock,
) -> None:
    paginator = Mock()
    paginator.paginate = Mock(
        return_value=[
            {
                "CertificateSummaryList": [
                    {
                        "CertificateArn": "arn:robert.pringles",
                        "DomainName": "robert.pringles",
                    },
                ],
            },
        ],
    )

    client.get_paginator = Mock(return_value=paginator)

    arn = certificates.try_get_certificate_arn(session, "robert.pringles")
    assert arn == "arn:robert.pringles"
