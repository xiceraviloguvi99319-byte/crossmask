# Synthetic example

The `input` directory contains fictional identities created only for testing. `people.csv` and `orders.csv` repeat the same names and phone numbers so that users can verify CrossMask produces consistent results across files.

Run:

```bash
crossmask run examples/input --output demo-output --secret "replace-this-demo-secret"
```

Then compare the `full_name` and `phone` columns in both sanitized files. The same source values should produce the same aliases or masks.
