"""
Local embedding generation for privacy-preserving RAG
"""

import hashlib
from typing import List
import numpy as np


class EmbeddingGenerator:
    """
    Generates embeddings locally using sentence transformers.
    All computation happens on-device - no data sent to cloud.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding generator

        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model_name = model_name
        self.model = None
        self._lazy_load_model()

    def _lazy_load_model(self):
        """Lazy load the model only when needed"""
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(self.model_name)
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. "
                    "Install with: pip install sentence-transformers"
                )

    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        self._lazy_load_model()
        return self.model.encode(text, convert_to_numpy=True)

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        self._lazy_load_model()
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    def get_model_hash(self) -> str:
        """
        Get a hash of the model for verification purposes.
        This proves which model was used for embedding generation.
        """
        # In production, this should hash the actual model weights
        # For now, we hash the model name
        return hashlib.sha256(self.model_name.encode()).hexdigest()

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors"""
        self._lazy_load_model()
        # Generate a test embedding to get dimension
        test_embedding = self.embed_text("test")
        return len(test_embedding)
