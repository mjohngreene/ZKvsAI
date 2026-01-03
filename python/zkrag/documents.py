"""
Document management for privacy-preserving RAG
"""

import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import time


@dataclass
class Document:
    """A private document"""
    id: str
    content: str
    metadata: Dict
    hash: str


@dataclass
class DocumentChunk:
    """A chunk of a document"""
    doc_id: str
    chunk_id: int
    content: str
    start_idx: int
    end_idx: int


class DocumentManager:
    """
    Manages private documents for RAG queries.
    Documents never leave the device.
    """

    def __init__(self, storage_dir: str = "./data/documents"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.documents: Dict[str, Document] = {}
        self.chunks: Dict[str, List[DocumentChunk]] = {}

    def add_document(self, content: str, metadata: Optional[Dict] = None) -> str:
        """Add a document to the collection"""
        if metadata is None:
            metadata = {}

        # Generate document ID and hash
        doc_hash = hashlib.sha256(content.encode()).hexdigest()
        doc_id = doc_hash[:16]

        # Create document
        doc = Document(
            id=doc_id,
            content=content,
            metadata=metadata,
            hash=doc_hash
        )

        self.documents[doc_id] = doc

        # Chunk the document
        self._chunk_document(doc)

        return doc_id

    def add_document_from_file(self, file_path: str) -> str:
        """Add a document from a file"""
        path = Path(file_path)
        content = path.read_text()
        metadata = {
            "filename": path.name,
            "path": str(path),
            "added_at": time.time()
        }
        return self.add_document(content, metadata)

    def _chunk_document(self, doc: Document, chunk_size: int = 512, overlap: int = 50):
        """Split document into overlapping chunks"""
        chunks = []
        content = doc.content
        start = 0

        chunk_id = 0
        while start < len(content):
            end = min(start + chunk_size, len(content))

            chunk = DocumentChunk(
                doc_id=doc.id,
                chunk_id=chunk_id,
                content=content[start:end],
                start_idx=start,
                end_idx=end
            )

            chunks.append(chunk)
            chunk_id += 1

            # Move start position with overlap
            start = end - overlap if end < len(content) else end

        self.chunks[doc.id] = chunks

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get a document by ID"""
        return self.documents.get(doc_id)

    def get_chunks(self, doc_id: str) -> List[DocumentChunk]:
        """Get all chunks for a document"""
        return self.chunks.get(doc_id, [])

    def get_all_chunks(self) -> List[DocumentChunk]:
        """Get all chunks from all documents"""
        all_chunks = []
        for chunks in self.chunks.values():
            all_chunks.extend(chunks)
        return all_chunks

    def generate_commitment(self) -> str:
        """
        Generate a cryptographic commitment to the document collection.
        This is what gets registered on-chain (not the documents themselves).
        """
        # Collect all document hashes
        doc_hashes = sorted([doc.hash for doc in self.documents.values()])

        # Create Merkle root (simplified)
        combined = "".join(doc_hashes)
        commitment = hashlib.sha256(combined.encode()).hexdigest()

        return commitment

    def export_commitment_data(self) -> Dict:
        """Export data needed for commitment verification"""
        return {
            "commitment": self.generate_commitment(),
            "document_count": len(self.documents),
            "document_hashes": [doc.hash for doc in self.documents.values()],
            "generated_at": time.time()
        }

    def save_commitment(self, filepath: str):
        """Save commitment data to file"""
        data = self.export_commitment_data()
        Path(filepath).write_text(json.dumps(data, indent=2))

    def __len__(self) -> int:
        return len(self.documents)

    def __contains__(self, doc_id: str) -> bool:
        return doc_id in self.documents
