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

## 🏗️ Architecture

### Three-Tier System

```
┌─────────────────────────────────────────────────────────────┐
│  Tier 1: Local Privacy Layer (Your Device)                  │
│  • Document storage (encrypted)                              │
│  • Local embeddings generation                               │
│  • Local vector search                                       │
│  • Local LLM inference                                       │
│  • ZK proof generation                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓ (Only ZK Proofs)
┌─────────────────────────────────────────────────────────────┐
│  Tier 2: Verification Layer (Nockchain)                     │
│  • Proof verification                                        │
│  • Document commitment registry                              │
│  • Model registry                                            │
│  • Usage tracking                                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Tier 3: Developer Layer (SDK & Tools)                      │
│  • Python SDK                                                │
│  • Rust SDK                                                  │
│  • CLI tools                                                 │
│  • Example applications                                      │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Rust 1.70+ ([rustup](https://rustup.rs/))
- Python 3.9+
- Poetry (Python package manager)
- `hoonc` (Hoon compiler)
- `nockup` CLI tool

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ZKvsAI.git
cd ZKvsAI

# Build Rust components
cargo build --release

# Install Python dependencies
poetry install

# Build Python bindings
cd rust/bindings
poetry run maturin develop --release
cd ../..

# Set up NockApp
cd nockapp
nockup project build
cd ..
```

### Usage Example

```python
from zkrag import PrivateRAG, NockchainVerifier

# Initialize with your private documents
rag = PrivateRAG(documents_dir="./my_private_docs")

# Register your document collection (only commitment goes on-chain)
commitment = rag.register_documents()
print(f"Document commitment: {commitment}")

# Query your documents privately
response, proof = rag.query("What are the key findings in the research?")

print(f"Answer: {response}")
print(f"Proof generated: {len(proof)} bytes")

# Verify the computation on Nockchain
verifier = NockchainVerifier(endpoint="http://localhost:8080")
verification = verifier.verify_query(proof)

print(f"Verification: {'✅ Valid' if verification.is_valid else '❌ Invalid'}")
```

## 📖 How It Works

### 1. Document Registration

```bash
# User registers documents (only commitment, not content)
zkrag register ./my_docs/
```

**What happens:**
- Documents are hashed locally
- Merkle tree commitment is created
- Only the commitment hash goes to Nockchain
- Your documents never leave your device

### 2. Private Query with Verification

```bash
# User queries their private documents
zkrag query "What are the key findings?"
```

**What happens:**
1. Query embedding generated locally
2. Vector similarity search in local database
3. Relevant chunks retrieved locally
4. LLM generates response locally
5. ZK proof created proving: "I correctly queried registered documents"
6. Proof submitted to Nockchain for verification
7. Verification receipt returned

**Privacy guarantees:**
- ✅ Query text never revealed
- ✅ Document content never revealed
- ✅ Embeddings never revealed
- ✅ Only proves computation was correct

### 3. Verification on Nockchain

```bash
# Anyone can verify the computation
zkrag verify <proof_id>
```

**What happens:**
- NockApp verifies ZK proof
- Checks document commitment exists
- Checks model hash is approved
- Records verified query
- Returns verification result

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

## 🛠️ Technology Stack

### Local Layer (Rust + Python)
- **Rust**: ZK circuits (arkworks), proof generation
- **Python**: RAG engine, embeddings, vector search
- **Local LLMs**: Ollama, llama.cpp, or similar

### Verification Layer (Nockchain)
- **Hoon**: State management, verification logic
- **Rust**: HTTP API, noun-based messaging
- **Nockchain**: Blockchain settlement

### ZK Proof System
- **Groth16**: Proof system (128-bit security)
- **BN254 Curve**: Elliptic curve
- **arkworks**: Rust ZK library ecosystem

## 📁 Project Structure

```
ZKvsAI/
├── rust/                    # Rust workspace
│   ├── circuits/            # ZK circuit definitions
│   ├── prover/              # Proof generation
│   ├── verifier/            # Proof verification
│   └── bindings/            # Python FFI bindings
│
├── python/                  # Python interface
│   ├── zkrag/               # Main package
│   │   ├── rag.py           # Private RAG engine
│   │   ├── embeddings.py    # Local embeddings
│   │   ├── documents.py     # Document manager
│   │   └── proof.py         # Proof interface
│   ├── tests/               # Python tests
│   ├── scripts/             # Utility scripts
│   └── notebooks/           # Jupyter notebooks
│
├── nockapp/                 # NockApp verifier
│   ├── hoon/                # Hoon kernel
│   ├── src/                 # Rust HTTP driver
│   └── web/                 # Web interface
│
├── hoon/                    # Additional Hoon code
├── data/                    # Data directory
│   ├── documents/           # Sample documents
│   └── proofs/              # Generated proofs
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # System architecture
│   ├── GETTING_STARTED.md   # Tutorial
│   └── API.md               # API reference
│
└── .claude/                 # Claude Code tooling
    ├── skills/              # Development skills
    └── agents/              # Development agents
```

## 🎓 Use Cases

### 1. Private Research Assistant
Query your private research papers without uploading to cloud services.

### 2. Medical Records Analysis
Analyze sensitive health data locally with verifiable computation.

### 3. Corporate Knowledge Base
Enterprise document search without exposing proprietary information.

### 4. Legal Document Review
Query legal documents while maintaining attorney-client privilege.

### 5. Personal Knowledge Management
Build a private second brain with full data sovereignty.

## 🚦 Roadmap

### ✅ Phase 1: Foundation (Current)
- [x] Project structure and tooling
- [x] Architecture design
- [ ] Basic ZK circuits
- [ ] Local RAG engine
- [ ] Simple proof generation

### 🚧 Phase 2: Integration (In Progress)
- [ ] NockApp verifier implementation
- [ ] End-to-end workflow
- [ ] CLI tools
- [ ] Documentation

### 📋 Phase 3: Features (Planned)
- [ ] Model registry
- [ ] Multi-document queries
- [ ] Web interface
- [ ] Example applications

### 🔮 Phase 4: Advanced (Future)
- [ ] Multi-party collaboration
- [ ] Federated learning integration
- [ ] TEE support
- [ ] Production deployment

## 🤝 Contributing

Contributions are welcome! This project combines:
- Zero-knowledge proofs (Rust/arkworks)
- NockApp development (Hoon/Rust)
- Privacy-preserving ML (Python)

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and technical details
- [Getting Started](docs/GETTING_STARTED.md) - Step-by-step tutorial
- [API Reference](docs/API.md) - Complete API documentation
- [Development Guide](docs/DEVELOPMENT.md) - Contributing guide

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

## 📞 Contact

Questions? Issues? Ideas?

- Open an issue: [GitHub Issues](https://github.com/yourusername/ZKvsAI/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/ZKvsAI/discussions)

---

**Built with privacy, verified with math, settled on blockchain.**
