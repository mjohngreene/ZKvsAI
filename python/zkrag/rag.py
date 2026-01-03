"""
Private RAG (Retrieval-Augmented Generation) engine

All computation happens locally - documents, queries, and responses never leave the device.
"""

import time
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass

from .documents import DocumentManager, DocumentChunk
from .embeddings import EmbeddingGenerator
from .proof import ProofGenerator
from .vector_store import VectorStore


@dataclass
class RAGResponse:
    """Response from a RAG query"""
    answer: str
    sources: List[DocumentChunk]
    query: str
    proof: Optional[str] = None
    timestamp: float = 0.0


class PrivateRAG:
    """
    Privacy-preserving RAG engine.

    Key features:
    - All documents stay on device
    - All embeddings generated locally
    - All similarity search happens locally
    - Optional: Generate ZK proofs of correct computation
    """

    def __init__(
        self,
        documents_dir: Optional[str] = None,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Initialize private RAG engine

        Args:
            documents_dir: Directory containing documents (optional)
            model_name: Embedding model to use
        """
        self.doc_manager = DocumentManager()
        self.embedding_gen = EmbeddingGenerator(model_name)
        self.vector_store = VectorStore()
        self.proof_gen = ProofGenerator()

        # Load documents if directory provided
        if documents_dir:
            self.load_documents(documents_dir)

    def load_documents(self, directory: str):
        """Load all documents from a directory"""
        from pathlib import Path

        doc_dir = Path(directory)
        if not doc_dir.exists():
            raise ValueError(f"Directory not found: {directory}")

        # Load text files
        for file_path in doc_dir.glob("*.txt"):
            doc_id = self.doc_manager.add_document_from_file(str(file_path))
            print(f"Loaded: {file_path.name} (ID: {doc_id})")

        # Generate embeddings for all chunks
        self._index_documents()

    def add_document(self, content: str, metadata: Optional[Dict] = None) -> str:
        """Add a single document"""
        doc_id = self.doc_manager.add_document(content, metadata)
        self._index_documents()
        return doc_id

    def _index_documents(self):
        """Generate embeddings and index all document chunks"""
        all_chunks = self.doc_manager.get_all_chunks()

        if not all_chunks:
            return

        # Extract text from chunks
        texts = [chunk.content for chunk in all_chunks]

        # Generate embeddings locally
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.embedding_gen.embed_batch(texts)

        # Add to vector store
        self.vector_store.add_embeddings(embeddings, all_chunks)

        print(f"Indexed {len(all_chunks)} chunks")

    def query(
        self,
        question: str,
        top_k: int = 3,
        generate_proof: bool = False
    ) -> RAGResponse:
        """
        Query the private document collection

        Args:
            question: The query text
            top_k: Number of relevant chunks to retrieve
            generate_proof: Whether to generate a ZK proof

        Returns:
            RAGResponse with answer, sources, and optional proof
        """
        timestamp = time.time()

        # 1. Generate query embedding (local)
        query_embedding = self.embedding_gen.embed_text(question)

        # 2. Search vector store (local)
        results = self.vector_store.search(query_embedding, top_k=top_k)

        # 3. Generate response (local - placeholder for now)
        answer = self._generate_answer(question, results)

        # 4. Optionally generate ZK proof
        proof_hex = None
        if generate_proof:
            proof_hex = self._generate_query_proof(
                question,
                query_embedding,
                results,
                timestamp
            )

        return RAGResponse(
            answer=answer,
            sources=results,
            query=question,
            proof=proof_hex,
            timestamp=timestamp
        )

    def _generate_answer(self, question: str, chunks: List[DocumentChunk]) -> str:
        """
        Generate an answer from retrieved chunks.

        TODO: Integrate with local LLM (Ollama, llama.cpp, etc.)
        For now, returns a simple concatenation.
        """
        if not chunks:
            return "No relevant information found."

        # Simple concatenation for now
        context = "\n\n".join([f"[{i+1}] {chunk.content}" for i, chunk in enumerate(chunks)])

        # Placeholder response
        answer = f"Based on {len(chunks)} relevant passages:\n\n{context[:500]}..."

        return answer

    def _generate_query_proof(
        self,
        query: str,
        query_embedding,
        results: List[DocumentChunk],
        timestamp: float
    ) -> str:
        """Generate a ZK proof that the query was performed correctly"""

        # Collect document hashes
        doc_ids = list(set([chunk.doc_id for chunk in results]))
        document_hashes = [
            self.doc_manager.get_document(doc_id).hash
            for doc_id in doc_ids
        ]

        # Get document commitment
        document_commitment = self.doc_manager.generate_commitment()

        # Get model hash
        model_hash = self.embedding_gen.get_model_hash()

        # Generate proof using Rust backend
        proof_hex = self.proof_gen.generate_proof(
            document_hashes=document_hashes,
            query_text=query,
            query_embedding=query_embedding.tolist(),
            search_results=[chunk.chunk_id for chunk in results],
            document_commitment=document_commitment,
            model_hash=model_hash,
            timestamp=int(timestamp)
        )

        return proof_hex

    def register_documents(self) -> str:
        """
        Generate a commitment to the document collection.
        This commitment can be registered on-chain without revealing documents.
        """
        return self.doc_manager.generate_commitment()

    def export_commitment(self, filepath: str):
        """Export commitment data for on-chain registration"""
        self.doc_manager.save_commitment(filepath)

    def get_stats(self) -> Dict:
        """Get statistics about the RAG system"""
        return {
            "num_documents": len(self.doc_manager),
            "num_chunks": len(self.doc_manager.get_all_chunks()),
            "embedding_dimension": self.embedding_gen.get_embedding_dimension(),
            "model_name": self.embedding_gen.model_name,
            "model_hash": self.embedding_gen.get_model_hash(),
            "commitment": self.register_documents()
        }
