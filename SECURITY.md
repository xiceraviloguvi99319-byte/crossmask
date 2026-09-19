# Security Policy

## Supported versions

CrossMask is currently an alpha project. Security fixes are applied to the latest release only.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting feature when it is enabled for this repository. Do not open a public issue containing an exploit, secret, raw dataset, or personal information.

## Sensitive-data handling

- CrossMask is designed to run locally and does not send files over the network.
- Keep `CROSSMASK_SECRET` outside the repository and shell scripts.
- Treat sanitized output as sensitive until it has passed automated verification and manual review.
- Never rely on CrossMask as the only control for regulatory compliance or publication approval.
- Do not commit input data, output data, mapping tables, or audit reports generated from real data.

## Cryptographic scope

CrossMask v0.1 uses HMAC-SHA-256 to derive stable pseudonyms. Pseudonymization is not the same as anonymization: possession of the source data and secret may still allow linkage. Key management and disclosure decisions remain the operator's responsibility.
