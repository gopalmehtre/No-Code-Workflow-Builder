from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ComponentType(str, Enum):
    USER_QUERY = "user_query"
    KNOWLEDGE_BASE = "knowledge_base"
    LLM_ENGINE = "llm_engine"
    OUTPUT = "output"

class BaseComponent(ABC):
    
    def __init__(self, node_id: str, config: Dict[str, Any]):
        self.node_id = node_id
        self.config = config
        self.type = None
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def validate_config(self) -> bool:
        return True

class UserQueryComponent(BaseComponent):
    
    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, config)
        self.type = ComponentType.USER_QUERY
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query", "")
        
        logger.info(f"UserQueryComponent [{self.node_id}]: Processing query")
        
        return {
            "query": query,
            "component": self.type,
            "node_id": self.node_id
        }
    
    def validate_config(self) -> bool:
        # User query component doesn't need special config
        return True

class KnowledgeBaseComponent(BaseComponent):
    
    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, config)
        self.type = ComponentType.KNOWLEDGE_BASE
        self.collection_name = config.get("collection_name")
        self.top_k = config.get("top_k", 3)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        from app.service.vector_service import vector_service
        from app.service.embedding_service import generate_embeddings
        
        query = input_data.get("query", "")
        
        logger.info(f"KnowledgeBaseComponent [{self.node_id}]: Retrieving context")
        
        try:
            query_embedding = generate_embeddings([query])[0]
            results = vector_service.query_similar(
                collection_name=self.collection_name,
                query_embedding=query_embedding,
                n_results=self.top_k
            )
            
            context = "\n\n".join(results.get("documents", []))
            
            logger.info(f"Retrieved {len(results.get('documents', []))} documents")
            
            return {
                "query": query,
                "context": context,
                "retrieved_docs": len(results.get("documents", [])),
                "component": self.type,
                "node_id": self.node_id
            }
        
        except Exception as e:
            logger.error(f"Error in KnowledgeBaseComponent: {str(e)}")
            return {
                "query": query,
                "context": "",
                "error": str(e),
                "component": self.type,
                "node_id": self.node_id
            }
    
    def validate_config(self) -> bool:
        return bool(self.collection_name)

class LLMEngineComponent(BaseComponent):
    
    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, config)
        self.type = ComponentType.LLM_ENGINE
        self.model = config.get("model")
        self.system_prompt = config.get("system_prompt")
        self.use_web_search = config.get("use_web_search", False)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        from app.service.llm_service import generate_response
        
        query = input_data.get("query", "")
        context = input_data.get("context", None)
        
        logger.info(f"LLMEngineComponent [{self.node_id}]: Generating response")
        
        try:
            result = generate_response(
                query=query,
                context=context,
                system_prompt=self.system_prompt,
                model=self.model
            )
            
            return {
                "query": query,
                "response": result.get("response", ""),
                "model": result.get("model", ""),
                "tokens": result.get("tokens", 0),
                "component": self.type,
                "node_id": self.node_id
            }
        
        except Exception as e:
            logger.error(f"Error in LLMEngineComponent: {str(e)}")
            return {
                "query": query,
                "response": f"Error: {str(e)}",
                "error": str(e),
                "component": self.type,
                "node_id": self.node_id
            }
    
    def validate_config(self) -> bool:
        return True

class OutputComponent(BaseComponent):
    
    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, config)
        self.type = ComponentType.OUTPUT
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"OutputComponent [{self.node_id}]: Formatting output")
        
        return {
            "query": input_data.get("query", ""),
            "response": input_data.get("response", ""),
            "final_output": True,
            "component": self.type,
            "node_id": self.node_id
        }
    
    def validate_config(self) -> bool:
        return True

def create_component(node_type: str, node_id: str, config: Dict[str, Any]) -> BaseComponent:
    
    component_map = {
        ComponentType.USER_QUERY: UserQueryComponent,
        ComponentType.KNOWLEDGE_BASE: KnowledgeBaseComponent,
        ComponentType.LLM_ENGINE: LLMEngineComponent,
        ComponentType.OUTPUT: OutputComponent
    }
    
    component_class = component_map.get(node_type)
    if not component_class:
        raise ValueError(f"Unknown component type: {node_type}")
    
    return component_class(node_id, config)