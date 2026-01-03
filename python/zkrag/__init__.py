"""
ZKvsAI - Privacy-Preserving AI/RAG Platform

Brings AI computation to your data, not your data to AI.
"""

__version__ = "0.1.0"

from .rag import PrivateRAG
from .documents import DocumentManager
from .embeddings import EmbeddingGenerator
from .proof import ProofGenerator
from .verifier import NockchainVerifier

__all__ = [
    "PrivateRAG",
    "DocumentManager",
    "EmbeddingGenerator",
    "ProofGenerator",
    "NockchainVerifier",
]
