# Privacy Model

CrossMask reduces accidental disclosure when preparing linked tabular data for analysis, testing, or controlled sharing. It is a pseudonymization tool, not a proof of anonymity.

## Protected workflow

- Direct identifiers in configured columns are replaced, masked, redacted, or removed.
- The same normalized value and entity type produce the same alias under the same secret.
- The audit report contains counts and one-way fingerprints, not copied source values.
- A post-run verifier searches for common phone, national-ID, bank-card, and email patterns.

## Out of scope

- Attackers with access to the input dataset or secret.
- Re-identification using rare combinations of indirect attributes.
- Free-form documents, images, audio, databases, or formulas in v0.1.
- Statistical guarantees such as k-anonymity or differential privacy.
- Legal or regulatory certification.

## Operator responsibilities

Use a high-entropy secret, keep it outside version control, customize the rules for the schema, review residual findings, inspect outputs manually, and apply organizational approval controls before sharing data.
