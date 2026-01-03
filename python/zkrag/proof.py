"""
ZK Proof generation interface
"""

from typing import List


class ProofGenerator:
    """
    Interface to Rust ZK proof generation.
    Generates proofs that RAG queries were performed correctly.
    """

    def __init__(self):
        self._rust_available = self._check_rust_bindings()

    def _check_rust_bindings(self) -> bool:
        """Check if Rust bindings are available"""
        try:
            import zkrag_rust
            return True
        except ImportError:
            return False

    def generate_proof(
        self,
        document_hashes: List[str],
        query_text: str,
        query_embedding: List[float],
        search_results: List[int],
        document_commitment: str,
        model_hash: str,
        timestamp: int
    ) -> str:
        """
        Generate a ZK proof for a query

        Args:
            document_hashes: Hashes of documents in the query set
            query_text: The query (private input)
            query_embedding: Query embedding vector (private)
            search_results: IDs of retrieved chunks (private)
            document_commitment: Public commitment to documents
            model_hash: Hash of embedding model used (public)
            timestamp: Query timestamp (public)

        Returns:
            Hex-encoded proof
        """
        if not self._rust_available:
            # Return placeholder if Rust bindings not available
            return "0" * 256  # Placeholder proof

        try:
            import zkrag_rust

            proof_hex = zkrag_rust.generate_proof(
                document_hashes,
                query_text,
                query_embedding,
                search_results,
                document_commitment,
                model_hash,
                timestamp
            )

            return proof_hex

        except Exception as e:
            raise RuntimeError(f"Proof generation failed: {e}")

    def is_available(self) -> bool:
        """Check if proof generation is available"""
        return self._rust_available
