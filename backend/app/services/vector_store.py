import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import logging
from app.core.config import settings
import hashlib

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB vector store for semantic search"""
    
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_data"
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="legal_knowledge",
            metadata={"description": "Legal knowledge base for RAG"}
        )
        
        logger.info("ChromaDB initialized successfully")
    
    def add_document(
        self,
        text: str,
        metadata: Dict[str, Any],
        doc_id: Optional[str] = None
    ) -> str:
        """Add document to vector store"""
        try:
            # Generate ID if not provided
            if not doc_id:
                doc_id = hashlib.md5(text.encode()).hexdigest()
            
            # Add to collection
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info(f"Document added: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search similar documents"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )
            
            # Format results
            documents = []
            if results['documents'] and results['documents'][0]:
                for idx, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'id': results['ids'][0][idx],
                        'text': doc,
                        'metadata': results['metadatas'][0][idx] if results['metadatas'] else {},
                        'distance': results['distances'][0][idx] if results['distances'] else 0,
                    })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise
    
    def delete_document(self, doc_id: str):
        """Delete document from vector store"""
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Document deleted: {doc_id}")
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise
    
    def update_document(
        self,
        doc_id: str,
        text: str,
        metadata: Dict[str, Any]
    ):
        """Update document in vector store"""
        try:
            self.collection.update(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata]
            )
            logger.info(f"Document updated: {doc_id}")
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"error": str(e)}


# Global vector store instance
vector_store = VectorStore()

