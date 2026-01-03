# ZKvsAI - Privacy-Preserving AI/RAG Platform Architecture

## Executive Summary

ZKvsAI is a privacy-preserving AI platform that inverts the traditional RAG paradigm. Instead of sending private data to centralized AI services, we **bring AI computation to the data** and use zero-knowledge proofs to verify correctness without revealing private information.

## Core Concept: Inverted RAG Paradigm

### Traditional RAG (Privacy Risk)
```
User's Private Documents
    ↓
Upload to Cloud AI Service ❌ (Privacy Lost)
    ↓
Embedding Generation
    ↓
Vector Search
    ↓
LLM Response
```

### ZKvsAI (Privacy Preserved)
```
User's Private Documents (Never Leave Device)
    ↓
Local Embedding Generation ✅
    ↓
Local Vector Search ✅
    ↓
Local LLM Inference ✅
    ↓
Generate ZK Proof of Computation ✅
    ↓
Submit Proof to Blockchain (Nockchain) ✅
    ↓
Verifiable Response + Privacy Intact ✅
```

## System Architecture

### Three-Tier Architecture

#### Tier 1: Local Privacy Layer (User's Device)
**Components:**
- Document Storage (encrypted)
- Embedding Generator (local models)
- Vector Database (local)
- RAG Query Engine
- ZK Proof Generator

**Technologies:**
- Python: Document processing, embeddings, RAG queries
- Rust: ZK circuit execution, proof generation
- Local LLMs: Ollama, llama.cpp, or similar

**Privacy Guarantees:**
- Documents never transmitted
- Embeddings never transmitted
- Queries never transmitted
- Only ZK proofs leave the device

#### Tier 2: Verification Layer (NockApp on Nockchain)
**Components:**
- Proof Verifier (Hoon kernel)
- Document Registry (commitment storage)
- Model Registry (approved model hashes)
- Usage Tracker
- API Gateway (Rust driver)

**Technologies:**
- Hoon: State management, verification logic
- Rust: HTTP API, noun-based messaging
- Nockchain: Blockchain settlement

**Functions:**
- Verify ZK proofs of computation
- Maintain registry of document commitments
- Track verified query history
- Coordinate multi-party operations

#### Tier 3: Developer Layer (SDK & Tools)
**Components:**
- Python SDK
- Rust SDK
- CLI Tools
- Example Applications
- Documentation

## Data Flow Diagrams

### Flow 1: Document Registration

```
User
  ↓
1. Hash documents locally
  ↓
2. Generate commitment (Merkle root)
  ↓
3. Submit commitment to NockApp
  ↓
NockApp (Hoon Kernel)
  ↓
4. Store commitment on-chain
  ↓
5. Return registration receipt
  ↓
User stores receipt
```

**Privacy Property:** Only hashes stored on-chain, not documents

### Flow 2: Private RAG Query with Verification

```
User's Device (Local)
  ↓
1. User submits query: "What are the key findings?"
  ↓
2. Generate embeddings locally
  ↓
3. Vector similarity search (local DB)
  ↓
4. Retrieve relevant document chunks
  ↓
5. LLM generates response (local)
  ↓
6. Build ZK Circuit Witness:
   - Private: documents, query, embeddings
   - Public: document commitment, timestamp, model hash
  ↓
7. Generate ZK Proof
   Circuit proves: "I queried the registered document set
                    using approved model M at time T"
  ↓
8. Submit proof + public inputs to NockApp
  ↓
NockApp (Verification Layer)
  ↓
9. Verify ZK proof
  ↓
10. Check document commitment exists
  ↓
11. Check model hash is approved
  ↓
12. Record verified query in state
  ↓
13. Return verification receipt
  ↓
User receives response + proof of correct computation
```

**Privacy Guarantees:**
- ✅ Query text never revealed
- ✅ Document contents never revealed
- ✅ Embeddings never revealed
- ✅ Only proves: "computation was performed correctly"

### Flow 3: Multi-Party Collaborative RAG (Future)

```
Multiple Users (each with private data)
  ↓
1. Each generates local embeddings
  ↓
2. Each creates ZK proof of contribution
  ↓
3. Submit proofs to NockApp coordinator
  ↓
NockApp
  ↓
4. Verify all proofs
  ↓
5. Aggregate without seeing raw data
  ↓
6. Return combined results
  ↓
Users receive collaborative insights
```

**Privacy Property:** No user sees others' data, but all benefit from collective knowledge

## Technical Components

### Component 1: Privacy Circuits (Rust)

**Location:** `rust/circuits/`

**Purpose:** Define ZK circuits that prove properties about private computations

**Circuits:**

1. **Document Query Circuit**
   ```rust
   Circuit: DocumentQueryCircuit {
       // Private inputs (witness)
       documents: Vec<Document>,
       query_embedding: Vec<f64>,
       search_results: Vec<Chunk>,

       // Public inputs
       document_commitment: Hash,
       model_hash: Hash,
       timestamp: u64,

       // Constraints
       constraints: {
           // 1. Documents hash to public commitment
           assert(hash(documents) == document_commitment);

           // 2. Embeddings generated using approved model
           assert(embedding_model.hash() == model_hash);

           // 3. Search was performed correctly
           assert(cosine_similarity(query_embedding, chunk) > threshold);
       }
   }
   ```

2. **Model Execution Circuit** (Future)
   - Proves LLM inference used specific model weights
   - Verifies deterministic computation

**Dependencies:**
- `ark-groth16`: Proof system
- `ark-bn254`: Elliptic curve
- `ark-ff`: Field arithmetic
- `ark-relations`: Constraint systems

### Component 2: Local RAG Engine (Python)

**Location:** `python/zkrag/`

**Modules:**

1. **Document Manager** (`documents.py`)
   ```python
   class DocumentManager:
       def add_document(path: str) -> DocumentID
       def generate_commitment() -> Hash
       def get_chunks(doc_id: DocumentID) -> List[Chunk]
   ```

2. **Embedding Generator** (`embeddings.py`)
   ```python
   class EmbeddingGenerator:
       def __init__(model: str = "sentence-transformers/all-MiniLM-L6-v2")
       def embed_document(text: str) -> np.ndarray
       def embed_query(query: str) -> np.ndarray
   ```

3. **RAG Engine** (`rag.py`)
   ```python
   class PrivateRAG:
       def query(question: str) -> Response:
           # 1. Generate query embedding
           # 2. Search local vector DB
           # 3. Retrieve chunks
           # 4. Generate response
           # 5. Create proof witness
           # 6. Call Rust proof generator
   ```

4. **Proof Interface** (`proof.py`)
   ```python
   class ProofGenerator:
       def generate_query_proof(
           documents: List[Document],
           query: str,
           results: List[Chunk]
       ) -> Proof
   ```

### Component 3: NockApp Verifier (Hoon + Rust)

**Location:** `nockapp/`

**Hoon Kernel** (`nockapp/hoon/verifier.hoon`):

```hoon
::  State Structure
+$  state
  $:  %v1
      documents=(map @ud document-commitment)
      models=(map @ud model-registration)
      queries=(map @ud verified-query)
      next-id=@ud
  ==

+$  document-commitment
  $:  id=@ud
      commitment=@t
      owner=@t
      registered=@da
  ==

+$  verified-query
  $:  id=@ud
      doc-id=@ud
      model-id=@ud
      proof=@t
      timestamp=@da
      status=@tas
  ==

::  Poke handlers
++  poke
  |=  [=cause =bowl:cask]
  ^-  [(list effect:cask) _this]
  ?-  -.cause
    %register-document
      ::  Store document commitment

    %register-model
      ::  Register approved AI model

    %verify-query
      ::  Verify ZK proof of RAG query

    %get-query
      ::  Retrieve verification record
  ==
```

**Rust Driver** (`nockapp/src/main.rs`):

```rust
// REST API Endpoints
POST   /api/v1/document/register
POST   /api/v1/model/register
POST   /api/v1/query/verify
GET    /api/v1/query/:id
GET    /api/v1/documents
```

### Component 4: Python SDK

**Location:** `python/zkrag/`

**High-Level API:**
```python
from zkrag import PrivateRAG, NockchainVerifier

# Initialize
rag = PrivateRAG(documents_dir="./my_docs")
verifier = NockchainVerifier(endpoint="http://localhost:8080")

# Register documents
commitment = rag.register_documents()
receipt = verifier.register_commitment(commitment)

# Private query with verification
response, proof = rag.query("What are the key findings?")
verification = verifier.verify_query(proof)

print(f"Answer: {response}")
print(f"Verified: {verification.is_valid}")
```

## Security Model

### Threat Model

**What We Protect Against:**
✅ Centralized AI service seeing private data
✅ Man-in-the-middle observing queries
✅ Blockchain validators learning document contents
✅ Malicious users claiming false computations

**What We Don't Protect Against:**
❌ Compromised user device (out of scope)
❌ Side-channel attacks on local inference (mitigation: secure enclaves)
❌ Quantum computers (future: lattice-based proofs)

### Privacy Guarantees

1. **Document Privacy**: Documents never transmitted, only commitments
2. **Query Privacy**: Query text never revealed, only proof of execution
3. **Computational Integrity**: ZK proofs ensure correct execution
4. **Model Transparency**: Verify which AI model was used

### Trust Assumptions

**Required Trust:**
- User trusts their local device
- User trusts the ZK proof system (Groth16 soundness)
- User trusts Nockchain consensus

**No Trust Required:**
- Don't trust centralized AI services (eliminated)
- Don't trust NockApp operator (verification is public)
- Don't trust other users (isolated execution)

## Performance Characteristics

### Latency Breakdown

**Local RAG Query:**
- Document embedding: ~10-50ms (cached)
- Vector search: ~1-10ms (HNSW index)
- LLM inference: ~100ms-5s (model dependent)
- **Total:** ~100ms-5s (no network!)

**ZK Proof Generation:**
- Witness generation: ~10ms
- Proof computation: ~100ms-1s (circuit dependent)
- **Total:** ~110ms-1s

**Blockchain Verification:**
- Proof verification: ~5-20ms
- Block confirmation: ~1-10s (Nockchain dependent)
- **Total:** ~1-10s

**End-to-End:**
- Query + Proof + Verification: ~1-15s
- **Advantage:** Privacy + Verifiability for ~10s overhead

### Storage Requirements

**User Device:**
- Documents: User's data size
- Embeddings: ~100MB per 10k documents
- ZK proving keys: ~50MB (cached)

**Blockchain (per query):**
- Proof: ~200 bytes
- Public inputs: ~100 bytes
- Metadata: ~50 bytes
- **Total:** ~350 bytes per verified query

## Deployment Architecture

### Phase 1: Local Development
```
User's Laptop
├── Python RAG engine
├── Local vector DB
├── Rust proof generator
└── Local Nockchain node
```

### Phase 2: Multi-User Network
```
User 1 Device ─┐
User 2 Device ─┼─→ Nockchain Network ─→ Shared Verification
User N Device ─┘
```

### Phase 3: Production System
```
User Devices (edge)
    ↓
Privacy Layer (local)
    ↓
Nockchain Network (global)
    ↓
Developer APIs
    ↓
Applications
```

## Development Roadmap

### Milestone 1: Foundation (Weeks 1-2)
- [x] Project structure
- [x] Copy existing ZK components
- [x] Copy existing NockApp patterns
- [ ] Basic document circuit
- [ ] Local embedding generation
- [ ] Simple proof generation

### Milestone 2: Integration (Weeks 3-4)
- [ ] NockApp verifier implementation
- [ ] End-to-end local RAG → proof → verification
- [ ] CLI tool for testing
- [ ] Documentation

### Milestone 3: Features (Weeks 5-8)
- [ ] Model registry
- [ ] Multi-document queries
- [ ] Optimized circuits
- [ ] Web interface
- [ ] Example applications

### Milestone 4: Advanced (Weeks 9-12)
- [ ] Multi-party collaboration
- [ ] Federated learning integration
- [ ] TEE (Trusted Execution Environment) support
- [ ] Production deployment guide

## Comparison to Existing Solutions

| Feature | Traditional RAG | Federated Learning | ZKvsAI |
|---------|----------------|-------------------|---------|
| Data Privacy | ❌ Upload required | ⚠️ Partial (gradients leak) | ✅ Full privacy |
| Verifiability | ❌ Trust AI service | ❌ No proofs | ✅ ZK proofs |
| Decentralization | ❌ Centralized | ⚠️ Coordinator needed | ✅ Blockchain |
| Performance | ✅ Fast | ⚠️ Slow (many rounds) | ✅ Local speed |
| Cost | $$ API fees | $ Compute + Communication | $ Compute only |

## Key Innovations

1. **Inverted RAG Paradigm**: Computation goes to data, not vice versa
2. **Verifiable Privacy**: ZK proofs ensure correct execution without revealing data
3. **Blockchain Settlement**: Nockchain provides decentralized verification
4. **Developer-Friendly**: Python SDK for easy integration
5. **Composable**: Combine with federated learning, secure enclaves, etc.

## References

- [Nockchain Documentation](https://docs.nockchain.org)
- [Groth16 Paper](https://eprint.iacr.org/2016/260)
- [RAG Survey](https://arxiv.org/abs/2312.10997)
- [ZK-ML](https://github.com/zkML/awesome-zkml)

## License

MIT License - See LICENSE file for details
