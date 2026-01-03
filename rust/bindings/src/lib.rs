// Python bindings for ZKvsAI
//
// Provides a Python interface to Rust ZK proof generation and verification

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

use zkrag_prover::{QueryProver, QueryWitness};
use zkrag_verifier::{QueryVerifier, PublicInputs, VerificationResult};

/// Generate a proof for a document query
#[pyfunction]
fn generate_proof(
    document_hashes: Vec<String>,
    query_text: String,
    query_embedding: Vec<f64>,
    search_results: Vec<usize>,
    document_commitment: String,
    model_hash: String,
    timestamp: u64,
) -> PyResult<String> {
    // Create witness
    let witness = QueryWitness::new(
        document_hashes,
        query_text,
        query_embedding,
        search_results,
        document_commitment,
        model_hash,
        timestamp,
    );

    // Generate proof
    let mut prover = QueryProver::new()
        .map_err(|e| PyValueError::new_err(format!("Prover error: {}", e)))?;

    prover.setup()
        .map_err(|e| PyValueError::new_err(format!("Setup error: {}", e)))?;

    let proof_bytes = prover.prove(witness)
        .map_err(|e| PyValueError::new_err(format!("Proof generation error: {}", e)))?;

    // Encode as hex
    Ok(hex::encode(proof_bytes))
}

/// Verify a document query proof
#[pyfunction]
fn verify_proof(
    proof_hex: String,
    document_commitment: String,
    model_hash: String,
    timestamp: u64,
) -> PyResult<bool> {
    // Decode proof
    let proof_bytes = hex::decode(&proof_hex)
        .map_err(|e| PyValueError::new_err(format!("Invalid hex: {}", e)))?;

    // Create public inputs
    let public_inputs = PublicInputs {
        document_commitment,
        model_hash,
        timestamp,
    };

    // Verify
    let verifier = QueryVerifier::new()
        .map_err(|e| PyValueError::new_err(format!("Verifier error: {}", e)))?;

    let result = verifier.verify(&proof_bytes, public_inputs)
        .map_err(|e| PyValueError::new_err(format!("Verification error: {}", e)))?;

    Ok(result.is_valid)
}

/// Get verification result with details
#[pyfunction]
fn verify_proof_detailed(
    proof_hex: String,
    document_commitment: String,
    model_hash: String,
    timestamp: u64,
) -> PyResult<String> {
    // Decode proof
    let proof_bytes = hex::decode(&proof_hex)
        .map_err(|e| PyValueError::new_err(format!("Invalid hex: {}", e)))?;

    // Create public inputs
    let public_inputs = PublicInputs {
        document_commitment,
        model_hash,
        timestamp,
    };

    // Verify
    let verifier = QueryVerifier::new()
        .map_err(|e| PyValueError::new_err(format!("Verifier error: {}", e)))?;

    let result = verifier.verify(&proof_bytes, public_inputs)
        .map_err(|e| PyValueError::new_err(format!("Verification error: {}", e)))?;

    // Serialize result as JSON
    serde_json::to_string(&result)
        .map_err(|e| PyValueError::new_err(format!("JSON error: {}", e)))
}

/// Python module initialization
#[pymodule]
fn zkrag_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_proof, m)?)?;
    m.add_function(wrap_pyfunction!(verify_proof, m)?)?;
    m.add_function(wrap_pyfunction!(verify_proof_detailed, m)?)?;
    Ok(())
}
