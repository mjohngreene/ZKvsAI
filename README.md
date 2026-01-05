# ZKvsAI - Privacy-Preserving AI/RAG Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Nockchain](https://img.shields.io/badge/Built%20with-Nockchain-purple)](https://nockchain.org)
[![Zero-Knowledge](https://img.shields.io/badge/Privacy-Zero--Knowledge-blue)](https://en.wikipedia.org/wiki/Zero-knowledge_proof)

> **Bringing AI to Your Data, Not Your Data to AI**

ZKvsAI is a privacy-preserving AI platform that inverts the traditional RAG (Retrieval-Augmented Generation) paradigm. Instead of uploading your private documents to centralized AI services, ZKvsAI brings AI computation to your local device and uses zero-knowledge proofs to verify correctness—all while keeping your data completely private.

## 🎯 The Problem

Traditional AI/RAG systems require you to:
- ❌ Upload private documents to cloud services
- ❌ Trust centralized AI providers with sensitive data
- ❌ Accept that your queries and documents are visible to the service
- ❌ Have no proof that computation was performed correctly

## ✨ The ZKvsAI Solution

With ZKvsAI:
- ✅ All documents stay on your device (never transmitted)
- ✅ All AI inference runs locally (complete privacy)
- ✅ Zero-knowledge proofs verify correctness (no trust required)
- ✅ Blockchain settlement provides decentralized verification (Nockchain)

## Architecture

### NockApp-Centric Design

**Important**: ZKvsAI is a **NockApp** (Nockchain application). The core platform runs on Nockchain, not as a standalone Python application.

```
┌─────────────────────────────────────────────────────────────┐
│  YOUR DEVICE (Private - Never Leaves)                       │
│                                                             │
│  ~/.zkvsai/documents/                                       │
│  ├── passport.json                                          │
│  ├── drivers_license.json                                   │
│  └── credit_card.json                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Rust driver reads files
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  NockApp (Core Platform - Hoon/Nock)                        │
│  • Document commitment generation                           │
│  • Claim processing                                         │
│  • State management                                         │
│  • ZK proof preparation                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Only: Proofs + Commitments
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Nockchain (Settlement Layer)                               │
│  • Proof verification                                       │
│  • Commitment registry                                      │
│  • Public state                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Roles

| Component | Role | Location |
|-----------|------|----------|
| **Hoon NockApp** | Core platform logic | `nockapp/hoon/` |
| **Rust Driver** | HTTP gateway, file I/O, ZK circuits | `nockapp/src/`, `rust/` |
| **Python Tools** | Testing & development only | `python/` |

## Quick Start

### Prerequisites

- Rust 1.70+ ([rustup](https://rustup.rs/))
- `hoonc` (Hoon compiler - when available)
- Python 3.9+ (for testing tools only)
- Poetry (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/mjohngreene/ZKvsAI.git
cd ZKvsAI

# Build Rust components (HTTP driver + ZK circuits)
cargo build --release

# Set up document storage
mkdir -p ~/.zkvsai/documents

# (Optional) Install Python testing tools
poetry install
```

### Create Your First Document

Create a private document at `~/.zkvsai/documents/passport.json`:

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

### Run the NockApp

```bash
# Start the NockApp HTTP server
cd nockapp
cargo run --release

# In another terminal, test the API
curl http://localhost:8080/health
```

### Generate a Proof (Coming Soon)

```bash
# Request proof that passport exists and isn't expired
curl -X POST http://localhost:8080/prove \
  -H "Content-Type: application/json" \
  -d '{"document_id": "doc_passport_001", "claim": "not_expired"}'
```

## How It Works

### 1. Store Private Documents

Store your private credentials locally in `~/.zkvsai/documents/`:

```
~/.zkvsai/documents/
├── passport.json
├── drivers_license.json
└── credit_card.json
```

**Privacy guarantee**: Documents never leave your device.

### 2. Generate Commitments

The NockApp reads your documents and generates cryptographic commitments:

```bash
curl -X POST http://localhost:8080/commit \
  -d '{"document_id": "doc_passport_001"}'
```

**What happens:**
- NockApp reads document from local storage
- Generates hash commitment of document contents
- Commitment can be published (document stays private)

### 3. Prove Claims About Documents

Generate ZK proofs about your documents without revealing them:

```bash
curl -X POST http://localhost:8080/prove \
  -d '{"document_id": "doc_passport_001", "claim": "not_expired"}'
```

**Example claims:**
- "My passport is not expired"
- "My credit limit exceeds $5,000"
- "I am over 21 years old"

**Privacy guarantees:**
- Document content never revealed
- Only the claim result is proven
- Verifier learns nothing except claim validity

### 4. Verify Proofs on Nockchain

Anyone can verify your proof without seeing your data:

```bash
curl http://localhost:8080/verify/<proof_id>
```

**What happens:**
- ZK proof verified mathematically
- Commitment checked against registry
- Verification result returned
- Your private data remains private

## 🔒 Security & Privacy

### What ZKvsAI Protects

| Threat | Protection |
|--------|-----------|
| Centralized AI service seeing your data | ✅ All computation is local |
| Man-in-the-middle observing queries | ✅ Only encrypted proofs transmitted |
| Blockchain validators learning document content | ✅ Only commitments on-chain |
| Malicious users claiming false computations | ✅ ZK proofs ensure integrity |

### Privacy Guarantees

1. **Document Privacy**: Documents never leave your device
2. **Query Privacy**: Query text is never transmitted
3. **Computational Integrity**: ZK proofs verify correct execution
4. **Model Transparency**: Verify which AI model was used

## Technology Stack

### Core Platform (NockApp)
- **Hoon**: Platform logic, state management, document processing
- **Nock**: Compilation target, deterministic execution
- **Nockchain**: Runtime environment, settlement layer

### Infrastructure (Rust)
- **Rust HTTP Driver**: File I/O, HTTP gateway, noun serialization
- **ZK Circuits**: arkworks-based proof generation
- **Groth16**: Proof system (128-bit security)

### Testing Tools (Python)
- **Python**: Test harness, development utilities
- **Note**: Python is for testing only, not production

## Project Structure

```
ZKvsAI/
├── nockapp/                 # CORE PLATFORM (NockApp)
│   ├── hoon/                # Hoon kernel (platform logic)
│   │   └── zkrag.hoon       # Main platform implementation
│   └── src/                 # Rust HTTP driver
│       └── main.rs          # File I/O, HTTP gateway
│
├── rust/                    # ZK Infrastructure
│   ├── circuits/            # ZK circuit definitions
│   ├── prover/              # Proof generation
│   ├── verifier/            # Proof verification
│   └── bindings/            # Python FFI (for testing)
│
├── python/                  # Testing Tools (NOT platform)
│   └── zkrag/               # Test harness & client SDK
│
├── docs/                    # Documentation
│   ├── DOCUMENT_SCHEMA.md   # Private document format spec
│   ├── ARCHITECTURE_REVISED.md
│   └── ...
│
└── ~/.zkvsai/documents/     # Private document storage (user's device)
    ├── passport.json
    ├── drivers_license.json
    └── credit_card.json
```

## Use Cases

### 1. Travel Booking with Verified Credentials
Prove your passport is valid and not expired to booking agents without revealing passport details.

### 2. Age Verification
Prove you're over 21 without revealing your exact birthdate or ID number.

### 3. Financial Qualification
Prove your credit limit exceeds a threshold without revealing the exact amount.

### 4. Identity Verification for AI Agents
Grant AI agents proof of your credentials so they can act on your behalf with verified authority.

### 5. Privacy-Preserving KYC
Complete know-your-customer requirements with minimal data exposure.

## Roadmap

### Phase 1: NockApp Foundation (Current)
- [x] Project structure and architecture
- [x] Document schema specification
- [ ] Hoon kernel implementation
- [ ] Rust HTTP driver with file I/O
- [ ] Basic commitment generation

### Phase 2: Proof Generation
- [ ] ZK circuits for document claims
- [ ] Expiration date proofs
- [ ] Range proofs (age, credit limit)
- [ ] Proof serialization

### Phase 3: Nockchain Integration
- [ ] On-chain commitment registry
- [ ] Proof verification on-chain
- [ ] Settlement workflow

### Phase 4: AI Agent Integration (Future)
- [ ] Proof handoff to external agents
- [ ] Agent credential verification
- [ ] Multi-claim proofs

## Contributing

Contributions are welcome! This project combines:
- **Hoon/Nock**: NockApp platform development
- **Rust**: HTTP driver, ZK circuits (arkworks)
- **Python**: Testing tools only

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Documentation

- [Document Schema](docs/DOCUMENT_SCHEMA.md) - Private document format specification
- [Architecture](docs/ARCHITECTURE_REVISED.md) - System design
- [Getting Started](docs/GETTING_STARTED.md) - Tutorial
- [CLAUDE.md](CLAUDE.md) - Development guidance

## 🔗 Related Projects

This project builds on:
- [ZKProofBuilder](../ZKProofBuilder) - ZK-SNARK age verification (proof-of-concept)
- [nockup-prover](../nockup-prover) - SNARK submission NockApp
- [Nockchain](https://github.com/nockchain/nockchain) - Blockchain platform

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [Nockchain](https://nockchain.org) - Blockchain infrastructure
- [arkworks](https://github.com/arkworks-rs) - ZK proof libraries
- [Urbit](https://urbit.org) - Hoon language and inspiration

## Contact

Questions? Issues? Ideas?

- Open an issue: [GitHub Issues](https://github.com/mjohngreene/ZKvsAI/issues)
- Discussions: [GitHub Discussions](https://github.com/mjohngreene/ZKvsAI/discussions)

---

**Your data stays yours. Proofs speak for themselves.**
