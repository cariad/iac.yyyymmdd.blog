from boto3 import Session


def try_get_certificate_arn(session: Session, domain_name: str) -> str | None:
    """
    Gets the ARN of the certificate for the specified domain name if it exists,
    otherwise `None`.

    Args:
        session: Boto3 session.
        domain_name: Domain name.

    Returns:
        ARN of the certificate if it exists, otherwise `None`.
    """

    # The region is intentionally us-east-1 because certificates are always
    # deployed there.
    acm = session.client("acm", region_name="us-east-1")

    paginator = acm.get_paginator("list_certificates")

    pages = paginator.paginate(CertificateStatuses=["ISSUED"])

    for page in pages:
        for certificate in page["CertificateSummaryList"]:
            if certificate.get("DomainName") == domain_name:
                if arn := certificate.get("CertificateArn"):
                    return arn

    return None
