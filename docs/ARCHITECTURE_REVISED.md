# ZKvsAI - Architecture

## Overview

ZKvsAI is a **NockApp** (Nockchain application) for privacy-preserving credential verification. Users store private documents locally and generate zero-knowledge proofs about those documents without revealing the underlying data.

## Core Principle

**Your data stays on your device. Only proofs leave.**

ZKvsAI enables:
1. Local storage of private credentials (passport, license, credit cards)
2. Generation of cryptographic commitments to those documents
3. ZK proofs about document claims ("passport not expired", "age > 21")
4. Verification of proofs without revealing document contents

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  USER'S DEVICE (Private - Off-Chain)                        │
│                                                             │
│  ~/.zkvsai/documents/                                       │
│  ├── passport.json                                          │
│  ├── drivers_license.json                                   │
│  └── credit_card.json                                       │
│                                                             │
│  Format: See docs/DOCUMENT_SCHEMA.md                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Rust driver reads local files
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  RUST HTTP DRIVER (nockapp/src/main.rs)                     │
│  • Reads documents from ~/.zkvsai/documents/                │
│  • Parses JSON according to document schema                 │
│  • Serializes to nouns for Hoon kernel                      │
│  • Exposes HTTP API for proof requests                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Noun data
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  HOON NOCKAPP (nockapp/hoon/zkrag.hoon)                     │
│  • Processes document data                                  │
│  • Generates commitments (hashes)                           │
│  • Validates claim requests                                 │
│  • Prepares data for ZK proof generation                    │
│  • Manages state (registered commitments)                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Commitment + Claim data
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  ZK PROOF GENERATION (rust/circuits/)                       │
│  • Takes private document data + public claim               │
│  • Generates ZKP proving claim is true                      │
│  • Outputs: proof + public inputs                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Only: Proof + Commitment
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  NOCKCHAIN (Settlement Layer)                               │
│  • Stores commitments (not documents)                       │
│  • Verifies proofs                                          │
│  • Public verification record                               │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Local Document Storage

**Location**: `~/.zkvsai/documents/`

**Format**: JSON files per `docs/DOCUMENT_SCHEMA.md`

**Document Types**:
- `passport` - International travel document
- `drivers_license` - Government-issued ID
- `credit_card` - Payment card info

**Privacy**: Documents NEVER leave the user's device.

### Layer 2: Rust HTTP Driver

**Location**: `nockapp/src/main.rs`

**Responsibilities**:
- Read documents from local filesystem
- Parse JSON according to document schema
- Serialize document data to nouns
- Communicate with Hoon kernel
- Expose HTTP API for clients

### Layer 3: Hoon NockApp

**Location**: `nockapp/hoon/zkrag.hoon`

**Responsibilities**:
- Process document data from driver
- Generate cryptographic commitments
- Validate claim requests
- Manage registered commitment state
- Coordinate with ZK proof generation

### Layer 4: ZK Circuits

**Location**: `rust/circuits/`

**Responsibilities**:
- Define constraints for document claims
- Generate proofs that claims are true
- Output proofs without revealing private data

### Layer 5: Python Tools (Testing Only)

**Location**: `python/`

**Purpose**: Testing and development utilities only.

**NOT for**: Core platform implementation.

## Data Flows

### Flow 1: Store Private Document

```
User creates document file
  ↓
~/.zkvsai/documents/passport.json
  ↓
{
  "id": "doc_passport_001",
  "type": "passport",
  "version": "1.0",
  "fields": {
    "number": "123456789",
    "expiration": "2030-06-20",
    ...
  }
}
  ↓
Document stays on user's device (never transmitted)
```

### Flow 2: Generate Commitment

```
User requests commitment
  ↓
POST /commit {"document_id": "doc_passport_001"}
  ↓
Rust Driver:
  1. Read document from ~/.zkvsai/documents/passport.json
  2. Validate against schema
  3. Serialize to noun
  ↓
Hoon NockApp:
  4. Hash document contents
  5. Generate commitment
  6. Store commitment in state
  ↓
Return: commitment hash
  ↓
Commitment can be published (document remains private)
```

### Flow 3: Prove Claim About Document

```
User requests proof of claim
  ↓
POST /prove {
  "document_id": "doc_passport_001",
  "claim": "not_expired",
  "params": {"as_of": "2026-01-05"}
}
  ↓
Rust Driver:
  1. Read document from disk
  2. Parse claim request
  ↓
Hoon NockApp:
  3. Validate document commitment exists
  4. Extract relevant fields (expiration date)
  5. Prepare witness for ZK circuit
  ↓
ZK Circuit:
  6. Private input: document data, expiration date
  7. Public input: commitment, claim type, current date
  8. Constraint: expiration > current_date
  9. Generate proof
  ↓
Return: {
  "proof": "...",
  "public_inputs": {
    "commitment": "abc123...",
    "claim": "not_expired",
    "result": true
  }
}
  ↓
Proof can be shared (document never revealed)
```

### Flow 4: Verify Proof

```
Anyone with proof can verify
  ↓
POST /verify {"proof": "...", "public_inputs": {...}}
  ↓
Verification:
  1. Check proof cryptographically valid
  2. Check commitment was registered
  3. Validate public inputs
  ↓
Return: {"valid": true, "verified_at": "..."}
  ↓
Verifier learns: "claim is true"
Verifier does NOT learn: document contents
```

## Claim Types

Claims are assertions about document contents that can be proven without revealing the data.

### Expiration Claims

| Claim | Description | Example |
|-------|-------------|---------|
| `not_expired` | Document expiration > current date | Passport valid for travel |
| `expires_after` | Expiration > specified date | License valid through trip |

### Range Claims

| Claim | Description | Example |
|-------|-------------|---------|
| `age_over` | Birth date implies age > N | Over 21 for alcohol |
| `credit_above` | Credit limit > threshold | Qualifies for rental |

### Existence Claims

| Claim | Description | Example |
|-------|-------------|---------|
| `has_field` | Document contains field | Has passport number |
| `field_matches` | Field equals value | Country is "USA" |

### Future Claim Types

- Composite claims (AND/OR of multiple claims)
- Cross-document claims (same name on passport and license)
- Delegation claims (authorize agent to use proof)

## Technology Stack

### Core Platform
- **Hoon**: NockApp logic (`nockapp/hoon/zkrag.hoon`)
- **Nock**: Execution target
- **Nockchain**: Runtime and settlement

### Infrastructure
- **Rust**: HTTP driver, file I/O, ZK circuits
- **arkworks**: ZK proof library
- **Groth16**: Proof system

### Testing
- **Python**: Test harness and utilities (not platform)

## Jock Integration Strategy

Jock is a new language for Nock (like Hoon but with Swift/Python-like syntax).

**Current Status**: Alpha (as of 2025)

**Strategy**:
1. **Now**: Build with Hoon (stable)
2. **Monitor**: Check Jock monthly at [docs.jock.org](https://docs.jock.org)
3. **Experiment**: When Jock reaches beta
4. **Migrate**: If Jock proves superior

See `docs/JOCK_EVALUATION.md` for detailed evaluation plan.

## Privacy Model

### What Stays Private (Off-Chain)

| Data | Location | Never Transmitted |
|------|----------|-------------------|
| Document contents | `~/.zkvsai/documents/` | ✅ |
| Field values | User's device | ✅ |
| Raw credentials | User's device | ✅ |

### What Can Be Public (On-Chain)

| Data | Purpose |
|------|---------|
| Document commitment (hash) | Proves document exists |
| Claim type | What was proven |
| Proof result (true/false) | Claim validity |
| ZK proof | Cryptographic verification |

### Privacy Guarantees

1. **Document Privacy**: Contents never leave device
2. **Selective Disclosure**: Prove specific claims without revealing all data
3. **Unlinkability**: Different proofs can't be linked to same document (future)
4. **Verifier Privacy**: Verifier learns only claim result, nothing else

## API Reference

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/documents` | List document IDs |
| GET | `/documents/:id` | Get document metadata (not contents) |
| POST | `/commit` | Generate commitment for document |
| POST | `/prove` | Generate proof for claim |
| POST | `/verify` | Verify a proof |

### Example Requests

**Generate Commitment:**
```bash
curl -X POST http://localhost:8080/commit \
  -H "Content-Type: application/json" \
  -d '{"document_id": "doc_passport_001"}'
```

**Prove Claim:**
```bash
curl -X POST http://localhost:8080/prove \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc_passport_001",
    "claim": "not_expired",
    "params": {"as_of": "2026-01-05"}
  }'
```

**Verify Proof:**
```bash
curl -X POST http://localhost:8080/verify \
  -H "Content-Type: application/json" \
  -d '{"proof": "...", "public_inputs": {...}}'
```

## Implementation Phases

### Phase 1: Foundation (Current)
- [x] Document schema specification
- [x] Architecture documentation
- [ ] Rust driver file I/O
- [ ] Hoon document handling
- [ ] Basic commitment generation

### Phase 2: Proof Generation
- [ ] Expiration claim circuits
- [ ] Range claim circuits (age, credit)
- [ ] Proof serialization

### Phase 3: Integration
- [ ] End-to-end workflow
- [ ] Nockchain settlement
- [ ] Verification on-chain

### Phase 4: Advanced (Future)
- [ ] AI agent proof handoff
- [ ] Multi-document proofs
- [ ] Delegation claims

## Related Documents

- `docs/DOCUMENT_SCHEMA.md` - Document format specification
- `docs/JOCK_EVALUATION.md` - Jock language evaluation
- `CLAUDE.md` - Development guidance
- `PROJECT_STATUS.md` - Current implementation status

## Summary

**ZKvsAI Architecture:**

```
Documents (local) → Rust Driver → Hoon NockApp → ZK Proofs → Nockchain
     │                                              │
     └──────────── Never transmitted ───────────────┘
```

Your credentials stay on your device. Only cryptographic proofs leave.
