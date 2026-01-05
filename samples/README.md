# Sample Documents

Sample documents for testing ZKvsAI.

## Usage

Copy sample documents to your local ZKvsAI directory:

```bash
mkdir -p ~/.zkvsai/documents
cp samples/documents/*.json ~/.zkvsai/documents/
```

## Documents

| File | Type | Description |
|------|------|-------------|
| `passport.json` | passport | Sample US passport |
| `drivers_license.json` | drivers_license | Sample CA driver's license |
| `credit_card.json` | credit_card | Sample credit card |

## Test Data

All sample documents use fictional data:

- **Name**: John Doe
- **DOB**: 1985-03-15 (age ~40)
- **Passport expiration**: 2030-06-20 (valid)
- **License expiration**: 2028-03-15 (valid)
- **Card expiration**: 2027-08 (valid)
- **Credit limit**: $10,000

## Example Claims

With these samples you can test:

| Claim | Document | Expected Result |
|-------|----------|-----------------|
| `not_expired` | passport | true |
| `not_expired` | drivers_license | true |
| `age_over(21)` | passport | true |
| `age_over(21)` | drivers_license | true |
| `credit_above(5000)` | credit_card | true |
| `credit_above(15000)` | credit_card | false |

## Schema

See `docs/DOCUMENT_SCHEMA.md` for the full document format specification.
