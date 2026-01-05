# CLAUDE.md

This file provides guidance to Claude Code when working with the ZKvsAI codebase.

## Project Overview

**ZKvsAI** is a privacy-preserving AI/RAG platform that inverts the traditional paradigm by bringing AI computation to data rather than sending data to AI services. It uses zero-knowledge proofs for verifiable computation and Nockchain for decentralized verification.

**Critical Architecture Point**: ZKvsAI is a **NockApp** (Nockchain application), NOT a Python application. Python is for testing and client tools only.

## Core Architecture

### Platform Core: NockApp (Hoon/Jock)

The actual ZKvsAI platform runs **on Nockchain** and is implemented in:
- **Hoon** (current implementation language)
- **Jock** (future evaluation/migration - see JOCK_EVALUATION.md)

**Location**: `nockapp/hoon/`

**Implements**:
- Document commitment registry
- Model registry
- Query processing logic
- State management
- All business logic

**IMPORTANT**: Python does NOT implement the platform. The platform is the NockApp.

### Infrastructure: Rust

**Location**: `rust/` and `nockapp/src/`

**Purpose**:
- ZK circuits (prove NockApp computations)
- Proof generation/verification
- HTTP gateway to NockApp (noun serialization)

### Tools: Python (Testing ONLY)

**Location**: `python/` (should be moved to `tools/python/`)

**Purpose**:
- Testing the NockApp
- Client SDK for HTTP API
- Development utilities

**NOT for**:
- Core platform implementation
- Business logic
- Production deployment

### Private Document Storage

**Location**: `~/.zkvsai/documents/` (local filesystem)

**Purpose**: Store private credentials and documents that ZKvsAI generates proofs about.

**Format**: JSON files following the schema in `docs/DOCUMENT_SCHEMA.md`

**Supported document types**:
- `passport` - International travel document
- `drivers_license` - Government-issued driving permit
- `credit_card` - Payment card information

**Data flow**:
1. User stores JSON documents in `~/.zkvsai/documents/`
2. Rust HTTP driver reads files from disk
3. Driver serializes documents to nouns
4. Hoon NockApp processes document data
5. ZK proofs generated about document claims
6. Proofs posted to Nockchain (documents never leave device)

## Technology Stack

### NockApp Development
- **Hoon**: Current stable implementation
- **Jock**: Periodically evaluate (Alpha status as of June 2025)
  - Docs: https://docs.jock.org/
  - GitHub: https://github.com/zorp-corp/jock-lang
  - Monitor monthly, experiment when stable
- **Nock**: Compilation target
- **Nockchain**: Execution environment

### Infrastructure
- **Rust 1.70+**: ZK circuits, HTTP driver
- **Cargo**: Workspace with 4 crates
- **Axum**: HTTP server framework

### Testing & Client Tools
- **Python 3.9+**: Testing harness, client SDK
- **Poetry**: Package management
- **PyO3**: Rust-Python bindings

## Build Commands

### Rust Development

```bash
# Build all workspace members
cargo build --release

# Build specific crate
cargo build -p zkrag-circuits
cargo build -p zkrag-prover
cargo build -p zkrag-verifier
cargo build -p zkrag-bindings

# Run tests
cargo test

# Format and lint
cargo fmt
cargo clippy
```

### Python Development (Testing Tools)

```bash
# Install dependencies
poetry install

# Build Python bindings
cd rust/bindings
poetry run maturin develop --release
cd ../..

# Run tests
poetry run pytest

# Format
poetry run black python/
```

### NockApp Development

```bash
# Compile Hoon to Nock (when hoonc available)
cd nockapp
hoonc hoon/zkrag.hoon -o zkrag.jam

# Build Rust HTTP driver
cargo build --release

# Run NockApp server
cargo run --release
```

## Project Structure

```
ZKvsAI/
├── nockapp/                  # CORE PLATFORM (NockApp)
│   ├── hoon/
│   │   ├── zkrag.hoon       # Main platform logic
│   │   ├── documents.hoon   # Document registry
│   │   ├── queries.hoon     # Query processing
│   │   └── models.hoon      # Model registry
│   ├── jock/                # Future: Jock implementations
│   │   └── (evaluate when stable)
│   └── src/                 # Rust HTTP driver
│       └── main.rs          # Gateway to NockApp
│
├── rust/                    # ZK Circuits & Infrastructure
│   ├── circuits/            # ZK circuit definitions
│   ├── prover/              # Proof generation
│   ├── verifier/            # Proof verification
│   └── bindings/            # Python FFI (for testing)
│
├── python/                  # Testing & Client Tools (NOT platform)
│   └── zkrag/               # Should rename to zkrag_client
│       ├── cli.py           # Testing CLI
│       ├── documents.py     # Test utilities
│       └── ...              # Other test/client code
│
├── docs/
│   ├── ARCHITECTURE_REVISED.md   # Correct architecture (READ THIS)
│   ├── JOCK_EVALUATION.md        # Jock strategy
│   ├── ARCHITECTURE_CORRECTIONS.md # What was wrong
│   └── GETTING_STARTED.md        # Tutorial
│
├── CORRECTIONS_SUMMARY.md   # Key architectural corrections
└── CLAUDE.md               # This file
```

## Critical Architectural Understanding

### ❌ INCORRECT (Initial Mistake)
- Python as core RAG platform
- Nockchain only for verification
- Python manages state and documents
- Separate Python process for queries

### ✅ CORRECT (Current Architecture)
- NockApp as core platform
- Nockchain IS the runtime
- Hoon/Jock manages state
- Everything runs on Nockchain
- Python is testing/client tools only

## Development Priorities

### Phase 1: NockApp Foundation (Hoon) - CURRENT FOCUS
- [ ] Expand `nockapp/hoon/zkrag.hoon`
- [ ] Implement document registry
- [ ] Implement query handler
- [ ] Implement state management
- [ ] Implement model registry

### Phase 2: Jock Evaluation - MONITOR MONTHLY
- [ ] Bookmark Jock resources
- [ ] Check monthly for updates
- [ ] Experiment when Jock hits beta (Q2 2026?)
- [ ] Decide on migration (Q4 2026?)

### Phase 3: Infrastructure
- [ ] Rust HTTP driver (partially done)
- [ ] ZK circuits for NockApp computation
- [ ] Proof generation/verification

### Phase 4: Testing & Client Tools (Python)
- [ ] Reposition Python to `tools/python/`
- [ ] Build NockApp test harness
- [ ] Create HTTP client SDK
- [ ] Development utilities

## Jock Language Notes

**Status**: Alpha (as of June 2025) by Zorp Corp
**Purpose**: Friendly programming language → Nock (like Solidity → EVM)
**Syntax**: Swift/Python-like (easier than Hoon)
**Compiler**: Written in Hoon

### Jock Resources
- Docs: https://docs.jock.org/
- GitHub: https://github.com/zorp-corp/jock-lang
- Blog: https://zorp.io/blog/jock
- Nockchain: https://www.nockchain.org/introducing-jock-a-friendly-programming-language-for-the-nock-ecosystem/

### Jock Strategy
1. **Now**: Implement in Hoon (stable)
2. **Monthly**: Monitor Jock development
3. **Q2 2026**: Experiment if stable
4. **Q4 2026**: Migration decision
5. **Don't wait**: Build with Hoon, add Jock later

### Jock Example
```jock
fn fib(n: Int) -> Int {
    if n <= 1 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}
```

## Common Mistakes to Avoid

### 1. Python's Role
- ❌ Don't implement business logic in Python
- ❌ Don't manage state in Python
- ❌ Don't treat Python as "the platform"
- ✅ Use Python for testing NockApp
- ✅ Use Python for client SDK
- ✅ Use Python for dev tools

### 2. Nockchain Understanding
- ❌ Don't think of Nockchain as "just verification"
- ❌ Don't design separate process + verification
- ✅ NockApp runs ON Nockchain
- ✅ Nockchain is the runtime environment

### 3. Jock Adoption
- ❌ Don't wait for Jock to start development
- ❌ Don't assume Jock is production-ready
- ✅ Monitor Jock monthly
- ✅ Experiment when stable
- ✅ Start with Hoon now

## Testing Strategy

### NockApp Tests (Python)
```bash
poetry run pytest python/tests/
```

Tests should:
- Send HTTP requests to NockApp
- Verify responses
- Test state changes
- Benchmark performance

### Rust Tests
```bash
cargo test
```

Tests should:
- Verify ZK circuits
- Test proof generation
- Test noun serialization

## Key Documentation

**Must Read** (in order):
1. `CORRECTIONS_SUMMARY.md` - What changed and why
2. `docs/ARCHITECTURE_REVISED.md` - Complete architecture
3. `docs/DOCUMENT_SCHEMA.md` - Private document format specification
4. `docs/JOCK_EVALUATION.md` - Jock strategy
5. `ARCHITECTURE_CORRECTIONS.md` - Detailed corrections

**Reference**:
- `README.md` - Project overview
- `docs/GETTING_STARTED.md` - Tutorial
- `PROJECT_STATUS.md` - Current status

## Development Workflow

### Working on NockApp (Primary)
1. Edit Hoon code in `nockapp/hoon/`
2. Compile with `hoonc` (when available)
3. Test via Python test harness
4. Iterate

### Working on Infrastructure (Secondary)
1. Edit Rust code in `rust/` or `nockapp/src/`
2. Run `cargo build`
3. Test with `cargo test`
4. Iterate

### Working on Tools (Tertiary)
1. Edit Python code in `python/` (soon `tools/python/`)
2. Test with `poetry run pytest`
3. Iterate

## Important Files to Modify

When implementing features:

### For NockApp Logic
- `nockapp/hoon/zkrag.hoon` - Main platform
- `nockapp/hoon/documents.hoon` - Document registry
- `nockapp/hoon/queries.hoon` - Query processing
- `nockapp/hoon/models.hoon` - Model registry

### For HTTP Gateway
- `nockapp/src/main.rs` - Rust HTTP driver

### For ZK Circuits
- `rust/circuits/src/document_query.rs` - Main circuit
- `rust/prover/src/lib.rs` - Proof generation
- `rust/verifier/src/lib.rs` - Verification

### For Testing
- `python/zkrag/` - Test harness and client SDK

## Version Control

The project uses Git. Key files:
- `.gitignore` - Excludes build artifacts, keys, etc.
- Remote: `https://github.com/mjohngreene/ZKvsAI.git`

## Future Work

### Near-term
- Expand Hoon implementation
- Build test harness
- Design oracle strategy for embeddings

### Medium-term
- Jock evaluation and experimentation
- ZK circuit implementation
- Full proof generation/verification

### Long-term
- Potential Jock migration
- Multi-user support
- Production deployment

## Questions for Development

1. **Where should RAG computation happen?**
   - On-chain in Hoon/Jock?
   - Via oracle?
   - Hybrid approach?

2. **How should embeddings work?**
   - On-chain model execution?
   - Oracle service?
   - Pre-computed and submitted?

3. **When to adopt Jock?**
   - Monitor monthly
   - Experiment in Q2 2026
   - Migrate if superior

## Summary

**ZKvsAI is a NockApp, not a Python application.**

- **Platform**: Hoon/Jock on Nockchain
- **Infrastructure**: Rust (HTTP gateway + ZK)
- **Tools**: Python (testing + client SDK)
- **Future**: Evaluate Jock for potential migration

Focus development on Hoon implementation in `nockapp/hoon/`, with periodic Jock evaluation and Python only for testing.
