# Contributing to CrossMask

Thank you for helping improve CrossMask. Contributions should strengthen privacy, correctness, documentation, or interoperability without adding real personal data to the repository.

## Before opening a pull request

1. Create or link an issue describing the problem.
2. Use only synthetic fixtures.
3. Add tests for behavior changes.
4. Run `python -m unittest discover -s tests -v`.
5. Update the README or changelog when user-visible behavior changes.

## Privacy requirements

- Never commit real names, phone numbers, identifiers, addresses, account numbers, secrets, or private datasets.
- Use reserved domains such as `example.test` and clearly fictional values.
- Reports and logs must not copy raw sensitive cell values.
- New detectors must include false-positive and false-negative tests.

By participating, contributors agree to follow the repository's code of conduct and security policy.
