"""
Nockchain verifier interface
"""

import requests
from typing import Optional
from dataclasses import dataclass


@dataclass
class VerificationResult:
    """Result of proof verification"""
    is_valid: bool
    query_id: Optional[int] = None
    message: str = ""


class NockchainVerifier:
    """
    Interface to Nockchain NockApp for proof verification
    """

    def __init__(self, endpoint: str = "http://localhost:8080"):
        """
        Initialize verifier

        Args:
            endpoint: URL of the NockApp verification service
        """
        self.endpoint = endpoint.rstrip("/")

    def register_commitment(self, commitment: str, owner: str = "local") -> dict:
        """
        Register a document commitment on-chain

        Args:
            commitment: Document collection commitment hash
            owner: Owner identifier

        Returns:
            Registration receipt
        """
        try:
            response = requests.post(
                f"{self.endpoint}/api/v1/document/register",
                json={
                    "commitment": commitment,
                    "owner": owner
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    def verify_query(
        self,
        proof: str,
        document_commitment: str,
        model_hash: str,
        timestamp: int
    ) -> VerificationResult:
        """
        Verify a query proof on-chain

        Args:
            proof: Hex-encoded ZK proof
            document_commitment: Document commitment (public input)
            model_hash: Model hash (public input)
            timestamp: Query timestamp (public input)

        Returns:
            VerificationResult
        """
        try:
            response = requests.post(
                f"{self.endpoint}/api/v1/query/verify",
                json={
                    "proof": proof,
                    "document_commitment": document_commitment,
                    "model_hash": model_hash,
                    "timestamp": timestamp
                },
                timeout=30  # Proof verification can take time
            )

            response.raise_for_status()
            data = response.json()

            return VerificationResult(
                is_valid=data.get("valid", False),
                query_id=data.get("query_id"),
                message=data.get("message", "")
            )

        except requests.RequestException as e:
            return VerificationResult(
                is_valid=False,
                message=f"Verification failed: {e}"
            )

    def get_query(self, query_id: int) -> dict:
        """
        Get details of a verified query

        Args:
            query_id: ID of the query

        Returns:
            Query details
        """
        try:
            response = requests.get(
                f"{self.endpoint}/api/v1/query/{query_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    def health_check(self) -> bool:
        """Check if verifier service is available"""
        try:
            response = requests.get(f"{self.endpoint}/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
