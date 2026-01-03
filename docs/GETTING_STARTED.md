# Getting Started with ZKvsAI

This guide will walk you through setting up and running your first privacy-preserving RAG query.

## Prerequisites

Make sure you have the following installed:

- **Rust** 1.70+ ([install rustup](https://rustup.rs/))
- **Python** 3.9+
- **Poetry** (Python package manager): `pip install poetry`
- **Git**

Optional (for NockApp features):
- **hoonc** (Hoon compiler)
- **nockup** CLI tool

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ZKvsAI.git
cd ZKvsAI
```

### 2. Install Python Dependencies

```bash
# Install Python packages
poetry install

# This will install:
# - sentence-transformers (for embeddings)
# - numpy, pandas (for data processing)
# - click, rich (for CLI)
# - and other dependencies
```

### 3. Build Rust Components

```bash
# Build all Rust crates
cargo build --release

# This builds:
# - zkrag-circuits (ZK circuits)
# - zkrag-prover (proof generation)
# - zkrag-verifier (proof verification)
# - zkrag-bindings (Python FFI)
```

### 4. Build Python Bindings

```bash
# Build Python-Rust bindings
cd rust/bindings
poetry run maturin develop --release
cd ../..
```

### 5. Verify Installation

```bash
# Check that CLI is available
poetry run zkrag --help

# You should see:
# ZKvsAI - Privacy-Preserving AI/RAG Platform
# Commands:
#   index     Index documents from a directory
#   query     Query your private documents
#   register  Register document commitment on Nockchain
#   stats     Show statistics about indexed documents
#   info      Show ZKvsAI system information
```

## Quick Start: Your First Private Query

### Step 1: Prepare Sample Documents

Create a directory with some sample text files:

```bash
# Create documents directory
mkdir -p data/documents

# Create sample documents
cat > data/documents/ai_facts.txt << 'EOF'
Artificial Intelligence (AI) is the simulation of human intelligence by machines.
Machine learning is a subset of AI that enables systems to learn from data.
Neural networks are computing systems inspired by biological neural networks.
EOF

cat > data/documents/privacy_facts.txt << 'EOF'
Zero-knowledge proofs allow one party to prove knowledge without revealing the information.
Homomorphic encryption enables computation on encrypted data.
Differential privacy adds noise to data to protect individual privacy.
EOF
```

### Step 2: Index Your Documents

```bash
poetry run zkrag index ./data/documents
```

**Output:**
```
Indexing documents from: ./data/documents
Loaded: ai_facts.txt (ID: a1b2c3d4e5f6g7h8)
Loaded: privacy_facts.txt (ID: i9j0k1l2m3n4o5p6)
Generating embeddings for 6 chunks...
Indexed 6 chunks
✓ Indexed 2 documents
✓ Created 6 chunks
✓ Commitment: 7a3f9b2e5d8c1a4b...
```

**What happened:**
- Documents were chunked into smaller pieces
- Each chunk was embedded using a local AI model (sentence-transformers)
- All data stayed on your device
- A cryptographic commitment was generated (this can go on-chain)

### Step 3: Query Your Documents

```bash
poetry run zkrag query ./data/documents "What are zero-knowledge proofs?"
```

**Output:**
```
Query: What are zero-knowledge proofs?

Answer:
Based on 1 relevant passages:
[1] Zero-knowledge proofs allow one party to prove knowledge without revealing the information...

Sources:
1. Doc i9j0k1l2m3n4o5p6 (chunk 0)
```

**What happened:**
- Your query was embedded locally
- Vector similarity search found relevant chunks
- All computation happened on your device
- No data was sent anywhere

### Step 4: Query with Proof Generation

```bash
poetry run zkrag query ./data/documents "What is machine learning?" --proof
```

**Output:**
```
Query: What is machine learning?

Answer:
Based on 1 relevant passages:
[1] Machine learning is a subset of AI that enables systems to learn from data...

Sources:
1. Doc a1b2c3d4e5f6g7h8 (chunk 1)

Proof: abc123def456789... (256 characters)
```

**What happened:**
- Same as before, but also generated a ZK proof
- Proof demonstrates: "I correctly queried registered documents"
- Proof doesn't reveal query text or document content
- Proof can be verified by anyone

## Advanced Usage

### View Statistics

```bash
poetry run zkrag stats ./data/documents
```

**Output:**
```
                RAG Statistics
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric               ┃ Value                 ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ Documents            │ 2                     │
│ Chunks               │ 6                     │
│ Embedding Dimension  │ 384                   │
│ Model                │ all-MiniLM-L6-v2      │
│ Model Hash           │ 9f2c4e8a...           │
│ Commitment           │ 7a3f9b2e...           │
└──────────────────────┴───────────────────────┘
```

### Register on Nockchain (Optional)

If you have the NockApp verifier running:

```bash
# Terminal 1: Start verifier
cd nockapp
cargo run --release

# Terminal 2: Register documents
poetry run zkrag register ./data/documents
```

**Output:**
```
Registering documents from: ./data/documents
✓ Commitment: 7a3f9b2e5d8c1a4b6f7e8d9c0a1b2c3d
✓ Saved to: commitment.json

Registering on Nockchain...
✓ Registered successfully!
  Registration ID: 1
```

### Query with Verification

```bash
poetry run zkrag query ./data/documents "What is AI?" --proof --verify
```

**Output:**
```
Query: What is AI?

Answer:
Artificial Intelligence (AI) is the simulation of human intelligence by machines...

Sources:
1. Doc a1b2c3d4e5f6g7h8 (chunk 0)

Proof: abc123def456...

Verifying proof on Nockchain...
✓ Proof verified successfully!
```

## Understanding the Privacy Model

### What Stays Private

✅ **Document Content**: Never leaves your device
✅ **Query Text**: Never revealed
✅ **Embeddings**: Computed and stored locally
✅ **Search Results**: Only you see them

### What Goes Public

📤 **Document Commitment**: Hash of your document collection (goes on-chain)
📤 **Model Hash**: Which AI model you used (public input to proof)
📤 **Timestamp**: When you made the query (public input to proof)
📤 **ZK Proof**: Proves correct computation (reveals nothing about documents or query)

### What is Proven

The ZK proof demonstrates:

1. ✅ "I queried a registered document set" (commitment matches)
2. ✅ "I used an approved AI model" (model hash matches)
3. ✅ "Computation was performed at time T" (timestamp is valid)

The proof does NOT reveal:
- ❌ What documents you have
- ❌ What your query was
- ❌ What results you got

## Troubleshooting

### ImportError: No module named 'zkrag_rust'

**Problem**: Python bindings not built

**Solution**:
```bash
cd rust/bindings
poetry run maturin develop --release
cd ../..
```

### "Proving key not found" error

**Problem**: ZK proving keys not generated

**Solution**: This is expected in the current prototype. The proof generation is using placeholders. Real ZK proof support is coming in future milestones.

### Slow embedding generation

**Problem**: First-time model download

**Solution**: The sentence-transformers model is downloaded on first use (~100MB). Subsequent runs will be faster.

### NockApp verifier not responding

**Problem**: Verifier not running

**Solution**:
```bash
# Start the verifier
cd nockapp
cargo run --release

# In another terminal, check health
curl http://localhost:8080/health
```

## Next Steps

Now that you have the basics working:

1. **Read the Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. **Try the Prototype**: Follow [HELLO_WORLD_PROTOTYPE.md](HELLO_WORLD_PROTOTYPE.md)
3. **Add Your Documents**: Index your own private documents
4. **Explore the Code**: Check out the Python and Rust implementations
5. **Contribute**: See [CONTRIBUTING.md](../CONTRIBUTING.md)

## Common Use Cases

### Private Research Assistant

```bash
# Index your research papers
poetry run zkrag index ~/Documents/research_papers

# Query without sending to cloud
poetry run zkrag query ~/Documents/research_papers "What are the main findings?"
```

### Corporate Knowledge Base

```bash
# Index company documents
poetry run zkrag index ~/company_docs

# Generate proof of query
poetry run zkrag query ~/company_docs "What is our Q4 strategy?" --proof
```

### Personal Knowledge Management

```bash
# Index your personal notes
poetry run zkrag index ~/notes

# Search your second brain privately
poetry run zkrag query ~/notes "Ideas about productivity"
```

## Performance Tips

1. **Use SSD storage** for faster document loading
2. **Start with smaller document sets** for testing
3. **Use GPU** (if available) for faster embeddings: `pip install sentence-transformers[gpu]`
4. **Cache embeddings** (automatic in current implementation)
5. **Limit chunk size** for faster indexing: modify in `documents.py`

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/ZKvsAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ZKvsAI/discussions)
- **Documentation**: See [docs/](.) directory

## What's Next?

This is a **prototype system**. Here's what's coming:

- ✅ Phase 1: Basic RAG with placeholder proofs (current)
- 🚧 Phase 2: Real ZK proof generation
- 📋 Phase 3: On-chain verification
- 🔮 Phase 4: Multi-user, LLM integration, production features

See [HELLO_WORLD_PROTOTYPE.md](HELLO_WORLD_PROTOTYPE.md) for the development roadmap.
