# iac.yyyymmdd.blog

Amazon Web Services infrastructure as code for [yyyymmdd.blog](https://www.yyyymmdd.blog).

## Developer setup

1. Fork this repository into your GitHub account.
1. Create codespaces secrets `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` that describe an IAM User with appropriate development policies (TBC).
1. Create a GitHub personal access token with permission to read your fork of the repository and record it in Secrets Manager under the name `github-token`.

## Testing

To run unit tests:

```bash
pytest
```
