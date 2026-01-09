import chromadb
from chromadb.config import Settings as ChromaSettings
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class VectorService:
    def __init__(self):
        try:
            self.client = chromadb.HttpClient(
                host=settings.chroma_host,
                port=settings.chroma_port
            )
            logger.info(f"Connected to ChromaDB at {settings.chroma_host}:{settings.chroma_port}")
        except Exception as e:
            logger.warning(f"HTTP client failed, using persistent client: {e}")
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_directory
            )
    
    def get_or_create_collection(self, collection_name: str):
        return self.client.get_or_create_collection(name=collection_name)
    
    def add_documents(self, collection_name: str, texts: list, embeddings: list, metadatas: list = None):
        try:
            collection = self.get_or_create_collection(collection_name)
            ids = [f"{collection_name}_{i}" for i in range(len(texts))]
            
            collection.add(
                documents=texts,
                embeddings=embeddings,
                ids=ids,
                metadatas=metadatas
            )
            logger.info(f"Added {len(texts)} documents to '{collection_name}'")
        except Exception as e:
            logger.error(f"Failed to add documents: {e}", exc_info=True)
            raise
    
    def query_similar(self, collection_name: str, query_embedding: list, n_results: int = 5):
        try:
            collection = self.client.get_collection(name=collection_name)
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            documents = results.get("documents", [[]])[0] if results.get("documents") else []
            
            logger.info(f"Found {len(documents)} similar documents in '{collection_name}'")
            
            return {
                "documents": documents,
                "metadatas": results.get("metadatas", [[]])[0] if results.get("metadatas") else [],
                "distances": results.get("distances", [[]])[0] if results.get("distances") else []
            }
        except Exception as e:
            logger.error(f"Query failed: {e}", exc_info=True)
            return {"documents": [], "metadatas": [], "distances": []}
    
    def query(self, collection_name: str, query_text: str, n_results: int = 5):

        try:
            from app.service.embedding_service import generate_embeddings
            query_embedding = generate_embeddings([query_text])[0]
            return self.query_similar(collection_name, query_embedding, n_results)
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {"documents": [], "metadatas": [], "distances": []}
    
    def delete_collection(self, collection_name: str):
        try:
            self.client.delete_collection(name=collection_name)
            logger.info(f"Deleted collection '{collection_name}'")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")

vector_service = VectorService()