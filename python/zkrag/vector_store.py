"""
Local vector store for semantic search
"""

from typing import List
import numpy as np


class VectorStore:
    """
    Simple in-memory vector store using cosine similarity.
    For production, could use FAISS or ChromaDB.
    """

    def __init__(self):
        self.embeddings = []
        self.chunks = []

    def add_embeddings(self, embeddings: np.ndarray, chunks: List):
        """Add embeddings and their corresponding chunks"""
        if len(embeddings) != len(chunks):
            raise ValueError("Embeddings and chunks must have same length")

        self.embeddings = embeddings
        self.chunks = chunks

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List:
        """
        Search for most similar chunks using cosine similarity

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return

        Returns:
            List of most similar DocumentChunks
        """
        if len(self.embeddings) == 0:
            return []

        # Compute cosine similarity
        similarities = self._cosine_similarity(query_embedding, self.embeddings)

        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Return corresponding chunks
        return [self.chunks[i] for i in top_indices]

    def _cosine_similarity(self, query: np.ndarray, vectors: np.ndarray) -> np.ndarray:
        """Compute cosine similarity between query and all vectors"""
        # Normalize query
        query_norm = query / (np.linalg.norm(query) + 1e-8)

        # Normalize vectors
        vectors_norm = vectors / (np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-8)

        # Compute dot product (cosine similarity for normalized vectors)
        similarities = np.dot(vectors_norm, query_norm)

        return similarities

    def __len__(self) -> int:
        return len(self.embeddings)
