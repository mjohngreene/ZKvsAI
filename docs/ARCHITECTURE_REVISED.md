# ZKvsAI - Revised Architecture (Nockchain-First)

## Critical Architectural Shift

**Previous misconception**: Python as the core platform with Nockchain for verification only.

**Correct architecture**: **Nockchain NockApp as the core platform**, with Python only for testing and client tooling.

## Core Principle

ZKvsAI is a **NockApp** (Nockchain application) that:
1. Runs on Nockchain (not as a separate Python application)
2. Implements privacy-preserving RAG entirely on-chain using Hoon/Jock
3. Uses ZK proofs to verify correct execution
4. Provides APIs for clients to interact with it

## System Architecture (Corrected)

### Layer 1: NockApp Core (On Nockchain)

**Technology**: Hoon/Jock + Nock

**Components**:
- **Document Registry** (Hoon state)
  - Stores document commitments (Merkle roots)
  - Owner permissions
  - Document metadata

- **Model Registry** (Hoon state)
  - Approved embedding models
  - Model hashes
  - Verification keys

- **Query Processor** (Hoon/Jock logic)
  - Receives encrypted queries
  - Processes RAG operations on-chain
  - Generates responses
  - Creates ZK proofs

- **Proof Verifier** (Hoon/Jock logic)
  - Verifies ZK proofs of computation
  - Validates query integrity
  - Records verified queries

### Layer 2: Rust Driver (HTTP Gateway)

**Technology**: Rust + Axum

**Purpose**: HTTP interface to the NockApp

**Components**:
- REST API endpoints
- Noun serialization/deserialization
- Kernel communication
- Static file serving

### Layer 3: Client Tools (Python - Testing/Utilities Only)

**Technology**: Python

**Purpose**: **NOT the platform**, only for:
- Testing the NockApp
- Development utilities
- Client SDKsfor interacting with the NockApp
- Benchmarking tools

**What Python does NOT do**:
- ❌ Does NOT implement the RAG engine (that's in Hoon/Jock)
- ❌ Does NOT run the core platform (that's the NockApp)
- ❌ Does NOT generate embeddings for the platform (happens on-chain or via oracle)
- ❌ Does NOT store documents (managed by NockApp state)

## Data Flow (Corrected)

### Flow 1: Document Registration

```
User (via client)
  ↓
1. Hash documents locally
  ↓
2. Generate Merkle tree commitment
  ↓
3. Submit commitment via HTTP API
  ↓
Rust Driver
  ↓
4. Convert to noun
  ↓
Hoon/Jock Kernel (NockApp)
  ↓
5. Store commitment in state
  ↓
6. Return registration receipt
  ↓
On-chain record created
```

### Flow 2: Private RAG Query (On-Chain Processing)

```
User encrypts query locally
  ↓
Submit encrypted query + commitment
  ↓
Rust Driver → Hoon/Jock Kernel
  ↓
NockApp processes query:
  1. Verify document commitment exists
  2. Decrypt query (if user authorized)
  3. Process RAG query on-chain:
     - Generate embeddings (or use oracle)
     - Search committed documents
     - Generate response
  4. Create ZK proof of computation
  ↓
Return: Response + ZK Proof
  ↓
Client verifies proof locally
```

### Flow 3: Proof Verification

```
Anyone can submit proof for verification
  ↓
NockApp verifies:
  - Proof cryptographically valid
  - Public inputs match (commitment, model hash, timestamp)
  - Document commitment was registered
  ↓
Record verification on-chain
  ↓
Return verification result
```

## Technology Stack (Corrected)

### Core Platform (NockApp)
- **Hoon**: Current implementation language
- **Jock**: Future/experimental (evaluate periodically)
- **Nock**: Compilation target
- **Nockchain**: Execution environment

### Infrastructure
- **Rust**: HTTP driver, noun handling, potentially ZK proof verification
- **Nockchain**: Blockchain consensus and settlement

### Tooling & Testing (Python)
- **Python**: Client SDK, testing tools, development utilities
- **NOT**: Core platform implementation

## Jock Integration Strategy

### Current Status (June 2025+)
- Jock is in **alpha** by Zorp Corp
- Compiles to Nock
- Syntax inspired by Swift/Python
- Integrates with Hoon stdlib

### Evaluation Plan

**Phase 1: Monitoring** (Ongoing)
- Track Jock development at [docs.jock.org](https://docs.jock.org)
- Review [zorp-corp/jock-lang](https://github.com/zorp-corp/jock-lang)
- Monitor feature releases

**Phase 2: Experimentation** (When Jock stabilizes)
- Implement simple NockApp components in Jock
- Compare Hoon vs Jock implementations
- Evaluate developer experience

**Phase 3: Migration** (If Jock proves superior)
- Gradually rewrite Hoon components in Jock
- Maintain parallel implementations during transition
- Full migration if Jock becomes stable

### What to Watch For
- ✅ Type system maturity
- ✅ Performance optimizations
- ✅ Debugging tools
- ✅ Community adoption
- ✅ Stability of syntax

## Revised Component Roles

### NockApp (Hoon/Jock) - CORE PLATFORM
**Implements**:
- Document commitment registry
- Model registry
- Query processing logic
- RAG computation (on-chain or via oracle)
- Proof generation coordination
- State management

**Does NOT do**:
- Direct file system access (uses commitments)
- External API calls (uses oracles if needed)
- Client-side UX (that's for clients)

### Rust Driver - HTTP GATEWAY
**Implements**:
- HTTP REST API
- Noun serialization
- Kernel communication
- CORS, routing, etc.

**Does NOT do**:
- Business logic (that's in Hoon/Jock)
- State management (that's in NockApp)
- RAG processing (that's in NockApp)

### Python Tools - TESTING & CLIENT SDK
**Implements**:
- Test harness for NockApp
- Client SDK for interacting with NockApp
- Development utilities
- Benchmarking tools

**Does NOT do**:
- Platform implementation
- Production RAG engine
- On-chain logic

## Privacy Model (Corrected)

### On-Chain (Public)
- Document commitments (Merkle roots)
- Model hashes
- Verification proofs
- Query timestamps (if public queries)

### Off-Chain (Private)
- Actual document contents (never submitted)
- Query text (encrypted if submitted)
- Intermediate computation results

### How Privacy Works

**Option A: Fully On-Chain RAG** (Future)
- NockApp has oracle access to embedding models
- Processes encrypted queries on-chain
- Uses ZK circuits to prove correct computation
- Most private, but requires oracle infrastructure

**Option B: Hybrid** (More practical short-term)
- User generates embeddings locally
- Submits commitment + encrypted query
- NockApp verifies commitments and records query
- Proof demonstrates query used registered documents

## Comparison to Initial Design

| Aspect | Initial (Incorrect) | Revised (Correct) |
|--------|-------------------|-------------------|
| Core Platform | Python RAG engine | Hoon/Jock NockApp |
| Where RAG runs | Local Python process | On-chain (NockApp) |
| Python's role | Core implementation | Testing & client tools |
| Embeddings | Python sentence-transformers | On-chain or oracle |
| State management | Python DocumentManager | Hoon NockApp state |
| Nockchain role | Just verification | Entire platform runtime |

## Why This Matters

### Incorrect Approach (What I built initially)
- Python as core platform ❌
- Nockchain only for proof verification ❌
- Separate Python process for RAG ❌
- Python manages state ❌

### Correct Approach (What should be built)
- NockApp as core platform ✅
- Nockchain runs everything ✅
- Hoon/Jock implements RAG logic ✅
- NockApp manages state ✅
- Python only for testing/tooling ✅

## Implementation Priorities (Revised)

### Phase 1: NockApp Foundation
- [ ] Document registry in Hoon
- [ ] Model registry in Hoon
- [ ] Basic query handler in Hoon
- [ ] State management

### Phase 2: RAG Logic (Hoon/Jock)
- [ ] Commitment verification
- [ ] Query processing logic
- [ ] Response generation
- [ ] Oracle integration (if needed for embeddings)

### Phase 3: ZK Integration
- [ ] Proof generation coordination
- [ ] Proof verification in Hoon/Jock
- [ ] Circuit design for RAG operations

### Phase 4: Jock Evaluation
- [ ] Implement sample components in Jock
- [ ] Compare Hoon vs Jock
- [ ] Migration plan if Jock is superior

### Phase 5: Client Tools (Python)
- [ ] HTTP client SDK
- [ ] Testing framework
- [ ] Benchmark tools

## Sources

- [Introduction to Jock](https://docs.jock.org/)
- [Introducing Jock: A Friendly Programming Language for the Nock Ecosystem](https://www.nockchain.org/introducing-jock-a-friendly-programming-language-for-the-nock-ecosystem/)
- [Jock and Awe](https://www.nockchain.org/jock-and-awe/)
- [GitHub - zorp-corp/jock-lang](https://github.com/zorp-corp/jock-lang)
- [Jock Language Developer Preview](https://zorp.io/blog/jock)

## Next Steps

1. **Refocus on NockApp** - Hoon implementation first
2. **Evaluate Jock** - Track development, experiment when stable
3. **Reposition Python** - Testing and client SDK only
4. **Design oracle strategy** - For embeddings and external data
5. **ZK circuits** - Prove NockApp computations

## Critical Takeaway

**ZKvsAI is a NockApp, not a Python application.**

The platform runs on Nockchain, implemented in Hoon/Jock, with Rust providing HTTP access and Python providing testing/client tools.
