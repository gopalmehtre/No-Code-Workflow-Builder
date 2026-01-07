import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional
from app.config import settings
import logging
import uuid

logger = logging.getLogger(__name__)

class VectorService:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIRECTORY
            )
            logger.info("ChromaDB client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}")
            raise
    
    def create_collection(self, collection_name: str) -> chromadb.Collection:
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Collection '{collection_name}' created/retrieved")
            return collection
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise
    
    def add_documents(
        self,
        collection_name: str,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None
    ) -> bool:
        try:
            collection = self.create_collection(collection_name)
            ids = [str(uuid.uuid4()) for _ in texts]
            collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas if metadatas else [{}] * len(texts)
            )
            
            logger.info(f"Added {len(texts)} documents to '{collection_name}'")
            return True
        
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False
    
    def query_similar(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 5
    ) -> Dict:
        try:
            collection = self.client.get_collection(collection_name)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            logger.info(f"Queried '{collection_name}', found {len(results['documents'][0])} results")
            return {
                "documents": results["documents"][0],
                "distances": results["distances"][0],
                "metadatas": results.get("metadatas", [[]])[0]
            }
        
        except Exception as e:
            logger.error(f"Error querying collection: {str(e)}")
            return {"documents": [], "distances": [], "metadatas": []}
    
    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.client.delete_collection(collection_name)
            logger.info(f"Deleted collection '{collection_name}'")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            return False
    
    def list_collections(self) -> List[str]:
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            return []

vector_service = VectorService()