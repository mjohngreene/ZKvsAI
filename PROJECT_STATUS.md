# ZKvsAI Project Status

**Last Updated**: 2026-01-05

## Project Overview

ZKvsAI is a privacy-preserving credential verification platform built as a **NockApp** (Nockchain application). Users store private documents (passport, driver's license, credit cards) locally and generate zero-knowledge proofs about those documents without revealing the underlying data.

**Critical Note**: ZKvsAI is a NockApp, NOT a Python application. Python code exists for testing only.

## Current Status: Phase 1 In Progress - NockApp Foundation

### What's Been Completed

#### 1. ✅ Project Structure & Architecture
- [x] Directory structure created
- [x] Rust workspace configured (circuits, prover, verifier, bindings)
- [x] NockApp structure in place
- [x] Architecture documentation corrected (NockApp-first)
- [x] Git repository initialized and pushed to GitHub

#### 2. ✅ Document Schema Specification
- [x] **docs/DOCUMENT_SCHEMA.md** - Private document format
- [x] Defined document types: passport, drivers_license, credit_card
- [x] JSON schema with type inference rules
- [x] Storage location: `~/.zkvsai/documents/`

#### 3. ✅ Documentation
- [x] **CLAUDE.md** - Development guidance (updated)
- [x] **README.md** - Project overview (updated for NockApp-first)
- [x] **CORRECTIONS_SUMMARY.md** - Architecture corrections

#### 4. Scaffolding (Exists but needs implementation)

**Rust** (`rust/`):
- [x] Circuit structure exists (needs real constraints)
- [x] Prover structure exists (placeholder implementation)
- [x] Verifier structure exists (placeholder implementation)

**Hoon** (`nockapp/hoon/`):
- [x] `verifier.hoon` exists (needs rename to `zkrag.hoon`)
- [ ] Document type handling not implemented
- [ ] Local file access not implemented

**Rust HTTP Driver** (`nockapp/src/`):
- [x] HTTP server structure with Axum
- [ ] File I/O for `~/.zkvsai/documents/` not implemented
- [ ] JSON parsing for document schema not implemented

#### 5. Testing Tools (Python) - FOR TESTING ONLY
**Note**: Python code is for testing the NockApp, NOT the platform itself.

- [x] Package structure exists
- [x] CLI structure exists
- [ ] Needs repositioning to `tools/python/`
- [ ] Needs refactoring to test NockApp HTTP API

## File Structure

```
ZKvsAI/
├── nockapp/                      # CORE PLATFORM (NockApp)
│   ├── hoon/
│   │   └── verifier.hoon         # (rename to zkrag.hoon)
│   └── src/
│       └── main.rs               # Rust HTTP driver
│
├── rust/                         # ZK Infrastructure
│   ├── circuits/                 # ZK circuits (scaffolding)
│   ├── prover/                   # Proof generation (scaffolding)
│   ├── verifier/                 # Proof verification (scaffolding)
│   └── bindings/                 # Python FFI (for testing)
│
├── python/                       # Testing Tools (NOT platform)
│   └── zkrag/                    # Test harness
│
├── docs/
│   ├── DOCUMENT_SCHEMA.md        # Document format spec
│   ├── ARCHITECTURE_REVISED.md   # System architecture
│   └── ...
│
└── ~/.zkvsai/documents/          # Private documents (user's device)
    ├── passport.json
    ├── drivers_license.json
    └── credit_card.json
```

## What Works Right Now

### ✅ Complete
1. **Architecture & Documentation**
   - NockApp-first architecture defined
   - Document schema specification complete
   - Development guidance (CLAUDE.md) updated

2. **Project Structure**
   - All directories in place
   - Rust workspace configured
   - Git repository on GitHub

### ⚠️ Scaffolding Only (Needs Implementation)
1. **Hoon NockApp** (`nockapp/hoon/`)
   - Basic structure exists
   - Document type handling needed
   - State management needed

2. **Rust HTTP Driver** (`nockapp/src/`)
   - HTTP server runs
   - File I/O for documents needed
   - JSON schema validation needed

3. **ZK Circuits** (`rust/circuits/`)
   - Structure exists
   - Real constraints needed
   - Trusted setup needed

### ❌ Not Started
1. Proof generation for document claims
2. Nockchain integration
3. End-to-end workflow

## Next Steps

### Immediate Priority
1. **Rename Hoon file**
   ```bash
   mv nockapp/hoon/verifier.hoon nockapp/hoon/zkrag.hoon
   ```

2. **Create sample documents**
   ```bash
   mkdir -p ~/.zkvsai/documents
   # Create passport.json, drivers_license.json per DOCUMENT_SCHEMA.md
   ```

3. **Test NockApp server**
   ```bash
   cd nockapp && cargo run --release
   curl http://localhost:8080/health
   ```

### Phase 1: NockApp Foundation
- [ ] Rename `verifier.hoon` to `zkrag.hoon`
- [ ] Add document type handling to Hoon kernel
- [ ] Implement file I/O in Rust driver
- [ ] Add JSON parsing for document schema
- [ ] Basic commitment generation

### Phase 2: Proof Generation
- [ ] Design claim types (expiration, age, range)
- [ ] Implement ZK circuits for claims
- [ ] Proof serialization
- [ ] API endpoints for proof requests

### Phase 3: Integration
- [ ] End-to-end proof workflow
- [ ] Nockchain commitment registry
- [ ] Verification on-chain

## Resources Leveraged

Existing projects provided patterns:
- **ZKProofBuilder**: Rust ZK architecture, Groth16 patterns
- **nockup-prover**: NockApp structure, Hoon patterns, HTTP driver
- **NockappBuilder**: nockapp-developer agent

## Development Tools Available

### Claude Code Skills (`.claude/skills/`)
- **hoon-development** - Hoon programming guide
- **nockapp-api-design** - NockApp endpoint creation
- **snark-testing** - Proof testing workflows

### Claude Code Agent (`.claude/agents/`)
- **nockapp-developer** - Expert NockApp development

## Known Limitations

### Current State
- ❌ ZK proofs are placeholders
- ❌ No actual on-chain settlement
- ❌ File I/O not implemented in driver
- ❌ Document type handling not in Hoon

### By Design (Privacy-First)
- ✅ Documents stored locally only
- ✅ No cloud dependencies
- ✅ All computation local to user

## Quick Commands Reference

```bash
# Build Rust components
cargo build --release

# Start NockApp server
cd nockapp && cargo run --release

# Test health endpoint
curl http://localhost:8080/health

# (Future) Create sample documents
mkdir -p ~/.zkvsai/documents
# Add JSON files per docs/DOCUMENT_SCHEMA.md
```

## Testing Checklist

- [ ] Rust workspace builds
- [ ] NockApp HTTP server starts
- [ ] Health endpoint responds
- [ ] Sample documents created in ~/.zkvsai/documents/
- [ ] (Future) Document endpoints work
- [ ] (Future) Proof generation works

## Success Criteria

### Phase 1: NockApp Foundation (Current)
- [x] Architecture documented
- [x] Document schema defined
- [ ] Hoon kernel handles document types
- [ ] Rust driver reads local files
- [ ] Basic commitment generation

### Phase 2: Proof Generation
- [ ] Claim types defined
- [ ] ZK circuits implemented
- [ ] Proofs generated and serialized

### Phase 3: Integration
- [ ] End-to-end workflow
- [ ] Nockchain settlement
- [ ] Demo complete

## Getting Help

- **Development Guide**: `CLAUDE.md`
- **Document Format**: `docs/DOCUMENT_SCHEMA.md`
- **Architecture**: `docs/ARCHITECTURE_REVISED.md`

## Summary

ZKvsAI is a **NockApp** for privacy-preserving credential verification:

- **Platform**: Hoon NockApp on Nockchain
- **Documents**: Stored locally at `~/.zkvsai/documents/`
- **Proofs**: ZK proofs about document claims
- **Python**: Testing tools only (not the platform)

**Current focus**: Implement Hoon kernel and Rust driver for document handling.

---

**Project initialized**: 2026-01-03
**Last updated**: 2026-01-05
**Repository**: https://github.com/mjohngreene/ZKvsAI
**License**: MIT
