# Architecture Corrections for ZKvsAI

## Critical Misunderstanding Identified

**Original Design**: Python as core platform with Nockchain for verification
**Correct Design**: NockApp (Hoon/Jock) as core platform, Python for testing only

## What Was Wrong

### Incorrect Assumptions
1. ❌ Python RAG engine as the "platform"
2. ❌ Local Python process doing embeddings and search
3. ❌ Nockchain only for "verification" of external computation
4. ❌ Python manages documents and state
5. ❌ Rust just generates proofs for Python

### Why This Was Wrong
- **Nockchain is not just a verification layer** - it's the entire runtime
- **NockApps run ON Nockchain** - they don't run separately and verify later
- **Python should not be the platform** - for NockApp development
- **State lives in Hoon** - not in Python data structures

## Corrected Understanding

### Core Platform: NockApp
- Written in **Hoon** (current) or **Jock** (future)
- Runs **on Nockchain** (not as separate process)
- Implements **all business logic**
- Manages **all state** (document commitments, queries, etc.)
- **ZK proofs** are generated to verify NockApp computation

### Supporting Infrastructure
- **Rust driver**: HTTP gateway to NockApp (noun serialization)
- **Python tools**: Testing, client SDK, dev utilities (NOT the platform)

## What Needs to Change

### 1. Project Structure

**Current (Incorrect emphasis)**:
```
ZKvsAI/
├── python/zkrag/          ← Incorrectly positioned as "core"
│   ├── rag.py            ← Should NOT be core platform
│   ├── documents.py      ← Should NOT be core state
│   └── embeddings.py     ← Should NOT be core logic
├── nockapp/               ← Incorrectly positioned as "just verification"
│   └── hoon/verifier.hoon ← Should be entire platform
└── rust/                  ← Incorrectly positioned as "just ZK proofs"
```

**Corrected (Proper emphasis)**:
```
ZKvsAI/
├── nockapp/              ← CORE PLATFORM (Hoon/Jock)
│   ├── hoon/
│   │   ├── zkrag.hoon    ← Main platform logic
│   │   ├── documents.hoon ← Document registry
│   │   ├── queries.hoon   ← Query processing
│   │   └── models.hoon    ← Model registry
│   ├── jock/             ← Future Jock implementations
│   │   └── (evaluate periodically)
│   └── src/              ← Rust HTTP driver
│       └── main.rs        ← Gateway to NockApp
├── rust/                 ← ZK circuits & proof generation
│   ├── circuits/          ← Circuits for NockApp computation
│   └── ...
└── tools/                ← Testing & client tools
    ├── python/           ← Python SDK & testing (NOT platform)
    │   ├── tests/        ← NockApp test harness
    │   └── client/       ← HTTP client SDK
    └── scripts/          ← Development utilities
```

### 2. Component Responsibilities

#### NockApp (Hoon/Jock) - Primary
**Implements**:
- ✅ Document commitment registry
- ✅ Model registry
- ✅ Query processing logic
- ✅ State management
- ✅ Access control
- ✅ Proof coordination

**File**: `nockapp/hoon/zkrag.hoon` (not `verifier.hoon`)

#### Rust - Secondary
**Implements**:
- ✅ HTTP REST API
- ✅ Noun serialization/deserialization
- ✅ Kernel communication
- ✅ ZK circuits for NockApp computation
- ✅ Proof generation (of NockApp execution)

#### Python - Tertiary (Tools Only)
**Implements**:
- ✅ Test harness for NockApp
- ✅ Client SDK (HTTP requests to NockApp)
- ✅ Benchmarking tools
- ✅ Development utilities

**Does NOT implement**:
- ❌ Core RAG logic (that's Hoon/Jock)
- ❌ State management (that's NockApp)
- ❌ Document storage (that's NockApp commitments)
- ❌ Production embedding generation (oracle or on-chain)

### 3. Data Flow Corrections

**Incorrect Flow**:
```
User → Python RAG → Generate Response → Rust Proof → Nockchain Verify
```
(This treats Nockchain as just a "verifier" of external computation)

**Correct Flow**:
```
User → HTTP API → Rust Driver → Hoon/Jock NockApp → Process Query
                                      ↓
                              Generate Response + Proof
                                      ↓
                              Store in NockApp State
                                      ↓
                              Return to User
```
(Nockchain **IS** the platform, not just verification)

### 4. File Reorganization Needed

**Rename/Move**:
```bash
# Rename nockapp verifier to zkrag (it's the whole platform)
mv nockapp/hoon/verifier.hoon nockapp/hoon/zkrag.hoon

# Move Python from core to tools
mkdir -p tools
mv python tools/python

# Rename Python package to reflect its role
mv tools/python/zkrag tools/python/zkrag_client

# Create Jock directory for future
mkdir -p nockapp/jock

# Update documentation
mv docs/ARCHITECTURE.md docs/ARCHITECTURE_OLD.md
mv docs/ARCHITECTURE_REVISED.md docs/ARCHITECTURE.md
```

## Revised Development Priorities

### Phase 1: NockApp Foundation (Hoon)
1. **Document Registry** (Hoon)
   - Store commitments
   - Owner permissions
   - Metadata

2. **Model Registry** (Hoon)
   - Approved models
   - Model hashes
   - Verification keys

3. **Query Handler** (Hoon)
   - Receive queries
   - Validate commitments
   - Process logic
   - Return responses

### Phase 2: RAG Logic (Hoon/Jock)
1. **Query Processing**
   - Commitment verification
   - Oracle integration (for embeddings if needed)
   - Response generation

2. **State Management**
   - Query history
   - Access logs
   - Permissions

### Phase 3: ZK Integration
1. **Circuits** (Rust)
   - Prove NockApp execution
   - Verify computation integrity

2. **Proof Generation** (Rust)
   - Coordinate with NockApp
   - Generate proofs of execution

### Phase 4: Jock Evaluation
1. **Monitor** Jock development
2. **Experiment** with sample components
3. **Migrate** if Jock proves superior

### Phase 5: Client Tools (Python)
1. **HTTP Client SDK**
   - Interact with NockApp API
   - Serialize/deserialize responses

2. **Testing Framework**
   - Test NockApp functionality
   - Integration tests
   - Performance benchmarks

## Python's Corrected Role

### What Python CAN Do
- ✅ **Test the NockApp**: Send HTTP requests, verify responses
- ✅ **Client SDK**: Provide easy interface to NockApp API
- ✅ **Development Tools**: Scripts for setup, deployment, etc.
- ✅ **Benchmarking**: Measure NockApp performance
- ✅ **Prototyping**: Experiment with ideas before implementing in Hoon

### What Python CANNOT Do (Must be Hoon/Jock)
- ❌ **Core Platform**: That's the NockApp
- ❌ **Business Logic**: That's Hoon/Jock
- ❌ **State Management**: That's NockApp state
- ❌ **RAG Engine**: That's Hoon/Jock (or oracle)
- ❌ **Production Deployment**: NockApp runs on Nockchain

## Jock's Role

### Current Status
- **Alpha** by Zorp Corp
- **Compiles to Nock**
- **Syntax**: Swift/Python-like
- **Integration**: Works with Hoon stdlib

### Strategy
1. **Start with Hoon** (stable, production-ready)
2. **Monitor Jock** (track development)
3. **Experiment** when Jock hits beta
4. **Migrate** if Jock proves superior

### Evaluation Schedule
- **Monthly**: Check Jock releases
- **Q2 2026**: Evaluate if ready for experiments
- **Q4 2026**: Decide on Hoon-only vs dual-track
- **2027**: Potential migration

## Migration Checklist

### Immediate Actions
- [ ] Rename `verifier.hoon` to `zkrag.hoon`
- [ ] Move Python to `tools/python`
- [ ] Update README to reflect Nockchain-first architecture
- [ ] Rewrite ARCHITECTURE.md (use ARCHITECTURE_REVISED.md)
- [ ] Create Jock evaluation document
- [ ] Update PROJECT_STATUS.md

### Refocused Development
- [ ] Expand Hoon implementation (not Python)
- [ ] Design NockApp state model
- [ ] Implement document registry in Hoon
- [ ] Implement query handler in Hoon
- [ ] Create Python test harness for NockApp
- [ ] Build Python client SDK for HTTP API

### Jock Preparation
- [ ] Bookmark Jock resources
- [ ] Track monthly releases
- [ ] Prepare sample Jock components
- [ ] Create Jock experimentation plan

## Key Takeaways

1. **NockApp IS the platform**, not Python
2. **Hoon/Jock implements business logic**, not Python
3. **Python is for testing and tooling**, not production
4. **Jock should be evaluated periodically**, but don't wait for it
5. **Start with Hoon now**, add Jock later if beneficial

## Documentation Updates Needed

- [x] Create ARCHITECTURE_REVISED.md ✅
- [x] Create JOCK_EVALUATION.md ✅
- [x] Create this corrections document ✅
- [ ] Update README.md
- [ ] Update PROJECT_STATUS.md
- [ ] Update GETTING_STARTED.md
- [ ] Archive old architecture docs

## Questions to Guide Future Development

1. **Where should RAG computation happen?**
   - On-chain in Hoon/Jock? (most private)
   - Via oracle? (more practical)
   - Hybrid?

2. **How should embeddings work?**
   - On-chain model execution?
   - Oracle service?
   - Pre-computed and submitted?

3. **What's the client workflow?**
   - Submit commitment
   - Submit query
   - Receive response + proof
   - Verify proof

4. **When to use Jock?**
   - Monitor monthly
   - Experiment in Q2 2026
   - Migrate if superior

## Conclusion

**The platform is the NockApp, not Python.**

ZKvsAI development should focus on:
1. Hoon implementation (core platform)
2. Jock evaluation (future migration)
3. Rust infrastructure (HTTP gateway + ZK)
4. Python tooling (testing + client SDK)

Python was incorrectly positioned as the "core" - it's actually just a testing and client tool.
