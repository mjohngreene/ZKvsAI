# Hello World Prototype Specification

## Goal

Build a minimal end-to-end demonstration of the privacy-preserving RAG system:
1. User indexes a private document locally
2. User queries the document locally (RAG)
3. System generates a ZK proof of the query
4. System verifies the proof on the NockApp
5. User receives verified response

## Components

### 1. Sample Document
- Create a simple text document: `data/documents/sample.txt`
- Content: "The capital of France is Paris. France is located in Western Europe."

### 2. Local RAG Query (Python)
```python
from zkrag import PrivateRAG

# Initialize with sample document
rag = PrivateRAG(documents_dir="./data/documents")

# Query
response = rag.query("What is the capital of France?", generate_proof=True)

print(f"Answer: {response.answer}")
print(f"Proof: {response.proof[:32]}...")
```

### 3. Proof Generation (Rust)
- Circuit: Simplified DocumentQueryCircuit
- Private inputs:
  - document_hash: Hash of sample.txt
  - query: "What is the capital of France?"
  - result: Chunk containing "Paris"
- Public inputs:
  - document_commitment: Hash of [sample.txt hash]
  - model_hash: Hash of embedding model
  - timestamp: Current time

### 4. Verification (NockApp)
- Submit proof to verifier NockApp
- NockApp checks:
  - Proof is valid (ZK verification)
  - Document commitment matches registered commitment
  - Model hash is in approved list
- Return verification result

## Implementation Steps

### Step 1: Placeholder Implementation (Week 1)
**Goal**: Get the full workflow running with placeholders

- [x] Python RAG engine (simple cosine similarity)
- [ ] Placeholder proof generation (returns dummy bytes)
- [ ] NockApp accepts and "verifies" placeholder proofs
- [ ] CLI can run end-to-end workflow

**Success criteria**:
```bash
zkrag index ./data/documents
zkrag query ./data/documents "What is the capital of France?" --proof --verify
# Output: Answer + verified proof
```

### Step 2: Real Embeddings (Week 2)
**Goal**: Replace embedding placeholders with real models

- [ ] Integrate sentence-transformers
- [ ] Generate actual embeddings
- [ ] Perform real vector similarity search
- [ ] Verify results are semantically correct

**Success criteria**: Queries return relevant results

### Step 3: Real ZK Proofs (Week 3)
**Goal**: Generate actual ZK proofs

- [ ] Implement simplified DocumentQueryCircuit
  - Constraint: hash(documents) == commitment
  - Skip complex search validation initially
- [ ] Run trusted setup (Groth16)
- [ ] Generate real proofs
- [ ] Cache proving keys

**Success criteria**: Real ZK proofs generated and serialized

### Step 4: Real Verification (Week 4)
**Goal**: Verify proofs on NockApp

- [ ] Integrate NockApp with Hoon kernel
- [ ] Implement proof deserialization in Hoon
- [ ] Call Groth16 verifier (or verify in Rust, confirm in Hoon)
- [ ] Store verification results on-chain

**Success criteria**: End-to-end verification with real proofs

## Testing Plan

### Unit Tests
- Document chunking
- Embedding generation
- Vector similarity search
- Proof serialization/deserialization
- Hoon state management

### Integration Tests
- Python → Rust proof generation
- Rust proof → NockApp verification
- End-to-end workflow

### Performance Benchmarks
- Embedding generation time
- Proof generation time
- Verification time
- Total end-to-end latency

## Expected Performance (Prototype)

| Operation | Target | Notes |
|-----------|--------|-------|
| Index 1 document | < 5s | Including embedding generation |
| Query (no proof) | < 1s | Local vector search |
| Proof generation | < 5s | Groth16 with simple circuit |
| Proof verification | < 1s | On NockApp |
| Total (query + prove + verify) | < 10s | End-to-end |

## Limitations (Prototype)

**What we're NOT implementing (yet):**
- ❌ Complex search validation circuits
- ❌ Multiple document support in proofs
- ❌ Merkle tree proofs
- ❌ LLM integration (just return relevant chunks)
- ❌ Multi-user support
- ❌ Production security hardening
- ❌ Optimized proof systems (using basic Groth16)

**What we ARE implementing:**
- ✅ Basic document indexing
- ✅ Simple RAG query
- ✅ Proof that query used registered documents
- ✅ On-chain verification
- ✅ End-to-end workflow demonstration

## Success Metrics

### Functional
- [ ] Can index documents
- [ ] Can query documents
- [ ] Can generate proofs
- [ ] Can verify proofs
- [ ] End-to-end CLI workflow works

### Educational
- [ ] Clear demonstration of privacy properties
- [ ] Shows proof generation and verification
- [ ] Explains what's proven (and what's not)

### Technical
- [ ] Real ZK proofs (not just placeholders)
- [ ] Actual blockchain verification
- [ ] Measurable performance

## Demo Script

```bash
# 1. Setup
cd /home/mini/Projects/ZKvsAI

# 2. Create sample document
mkdir -p data/documents
echo "The capital of France is Paris. France is located in Western Europe." > data/documents/sample.txt

# 3. Install dependencies
poetry install
cargo build --release

# 4. Index documents
poetry run zkrag index ./data/documents

# 5. Query without proof
poetry run zkrag query ./data/documents "What is the capital of France?"

# 6. Query with proof (no verification)
poetry run zkrag query ./data/documents "What is the capital of France?" --proof

# 7. Start NockApp verifier (separate terminal)
cd nockapp
cargo run --release

# 8. Register document commitment
poetry run zkrag register ./data/documents

# 9. Query with proof and verification
poetry run zkrag query ./data/documents "What is the capital of France?" --proof --verify

# Expected output:
# Answer: Based on 1 relevant passage: The capital of France is Paris...
# Proof: abc123def456...
# ✓ Proof verified successfully!
```

## Next Steps After Prototype

1. **Optimize Circuits**: Add proper Merkle tree validation
2. **LLM Integration**: Add local LLM for answer generation
3. **Multi-Document**: Support queries across multiple documents
4. **Web UI**: Build web interface for easier use
5. **Production Ready**: Security audit, optimization, deployment guide

## Timeline

- **Week 1**: Placeholder implementation (done)
- **Week 2**: Real embeddings
- **Week 3**: Real ZK proofs
- **Week 4**: Real verification
- **Week 5**: Polish and documentation

Total: ~5 weeks to working prototype
