// ZKvsAI Privacy Circuits
//
// This module defines zero-knowledge circuits for privacy-preserving RAG operations.

use ark_bn254::Fr;
use ark_ff::Field;
use ark_r1cs_std::prelude::*;
use ark_relations::r1cs::{ConstraintSynthesizer, ConstraintSystemRef, SynthesisError};

pub mod document_query;
pub mod utils;

pub use document_query::DocumentQueryCircuit;

/// Field element type for BN254 curve
pub type FieldElement = Fr;

/// Common trait for all privacy circuits
pub trait PrivacyCircuit<F: Field>: ConstraintSynthesizer<F> {
    /// Get circuit name
    fn name(&self) -> &str;

    /// Get number of constraints
    fn num_constraints(&self) -> usize;

    /// Get number of public inputs
    fn num_public_inputs(&self) -> usize;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_circuit_basic() {
        // Placeholder test
        assert_eq!(2 + 2, 4);
    }
}
