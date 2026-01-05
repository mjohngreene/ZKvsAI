# ZKvsAI Document Schema Specification

Version: 1.0
Status: Draft

## Overview

This specification defines the format for private documents stored locally and accessed by the ZKvsAI NockApp. Documents contain sensitive personal information that users want to prove claims about without revealing the underlying data.

## Storage Location

Documents are stored on the local filesystem:

```
~/.zkvsai/documents/
├── passport.json
├── drivers_license.json
├── credit_card.json
└── ...
```

## Document Format

### Base Structure

All documents follow this structure:

```json
{
  "id": "<unique_document_id>",
  "type": "<document_type>",
  "version": "1.0",
  "created": "<ISO8601_timestamp>",
  "fields": {
    "<field_name>": "<field_value>",
    ...
  }
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier for this document (e.g., `doc_passport_001`) |
| `type` | string | yes | Document type identifier (e.g., `passport`, `drivers_license`, `credit_card`) |
| `version` | string | yes | Schema version for this document type |
| `created` | string | yes | ISO8601 timestamp of document creation |
| `fields` | object | yes | Flat key-value map of document-specific fields |

### Type Inference

Field value types are inferred from JSON:

| JSON Value | Inferred Type | Example |
|------------|---------------|---------|
| Number (no decimal) | integer | `10000` |
| Number (with decimal) | float | `99.95` |
| String | string | `"USA"` |
| Boolean | boolean | `true` |

Date values are stored as strings in ISO8601 format and parsed contextually:
- Full date: `"1985-03-15"`
- Year-month: `"2027-08"`
- Full timestamp: `"2026-01-05T12:00:00Z"`

## Document Types

### passport

Identity document for international travel.

```json
{
  "id": "doc_passport_001",
  "type": "passport",
  "version": "1.0",
  "created": "2026-01-05T12:00:00Z",
  "fields": {
    "number": "123456789",
    "country": "USA",
    "given_name": "John",
    "surname": "Doe",
    "date_of_birth": "1985-03-15",
    "expiration": "2030-06-20"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `number` | string | Passport number |
| `country` | string | Issuing country (ISO 3166-1 alpha-3 recommended) |
| `given_name` | string | First/given name |
| `surname` | string | Last/family name |
| `date_of_birth` | string | Date of birth (YYYY-MM-DD) |
| `expiration` | string | Expiration date (YYYY-MM-DD) |

### drivers_license

Government-issued driving permit.

```json
{
  "id": "doc_license_001",
  "type": "drivers_license",
  "version": "1.0",
  "created": "2026-01-05T12:00:00Z",
  "fields": {
    "number": "D1234567",
    "state": "CA",
    "given_name": "John",
    "surname": "Doe",
    "date_of_birth": "1985-03-15",
    "expiration": "2028-03-15",
    "class": "C"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `number` | string | License number |
| `state` | string | Issuing state/province |
| `given_name` | string | First/given name |
| `surname` | string | Last/family name |
| `date_of_birth` | string | Date of birth (YYYY-MM-DD) |
| `expiration` | string | Expiration date (YYYY-MM-DD) |
| `class` | string | License class/type |

### credit_card

Payment card information.

```json
{
  "id": "doc_card_001",
  "type": "credit_card",
  "version": "1.0",
  "created": "2026-01-05T12:00:00Z",
  "fields": {
    "card_number": "4111111111114242",
    "last_four": "4242",
    "issuer": "Chase",
    "cardholder": "John Doe",
    "expiration": "2027-08",
    "credit_limit": 10000
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `card_number` | string | Full card number (private, never proven directly) |
| `last_four` | string | Last four digits of card number |
| `issuer` | string | Card issuer/bank |
| `cardholder` | string | Name on card |
| `expiration` | string | Expiration (YYYY-MM) |
| `credit_limit` | integer | Credit limit in cents or whole currency units |

## Adding New Document Types

New document types can be added by:

1. Choosing a unique `type` identifier (lowercase, underscores)
2. Defining the `fields` schema
3. Adding documentation to this spec
4. Updating NockApp handlers if type-specific logic is needed

## Commitments

Each document can be committed to by hashing its canonical JSON representation. The commitment scheme is defined separately in the proof specification.

## Future Considerations

- **Encryption at rest**: Documents may be encrypted with user-controlled keys
- **Document versioning**: Track changes to document contents over time
- **Multi-document bundles**: Group related documents together
- **Schema registry**: On-chain or distributed schema definitions
