from typing import Dict, List, Any, Tuple
from app.core.components import ComponentType
import logging

logger = logging.getLogger(__name__)

def validate_workflow(nodes: List[Dict], edges: List[Dict]) -> Tuple[bool, str]:
    if not nodes:
        return False, "Workflow must have at least one node"
    
    node_types = {node.get("type") for node in nodes}
    if ComponentType.USER_QUERY not in node_types:
        return False, "Workflow must have a User Query component"
    
    if ComponentType.OUTPUT not in node_types:
        return False, "Workflow must have an Output component"
    
    adjacency = {}
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if source not in adjacency:
            adjacency[source] = []
        adjacency[source].append(target)
    
    user_query_nodes = [n for n in nodes if n.get("type") == ComponentType.USER_QUERY]
    if len(user_query_nodes) != 1:
        return False, "Workflow must have exactly one User Query component"
    
    user_query_id = user_query_nodes[0].get("id")
    
    output_nodes = [n for n in nodes if n.get("type") == ComponentType.OUTPUT]
    if len(output_nodes) != 1:
        return False, "Workflow must have exactly one Output component"
    
    output_id = output_nodes[0].get("id")
    visited = set()
    
    def dfs(node_id):
        if node_id in visited:
            return False
        if node_id == output_id:
            return True
        visited.add(node_id)
        for neighbor in adjacency.get(node_id, []):
            if dfs(neighbor):
                return True
        return False
    
    if not dfs(user_query_id):
        return False, "No valid path from User Query to Output"
    for node in nodes:
        node_type = node.get("type")
        node_id = node.get("id")
        config = node.get("data", {})
        
        if node_type == ComponentType.KNOWLEDGE_BASE:
            if not config.get("collection_name"):
                return False, f"KnowledgeBase component '{node_id}' requires a collection_name"
    
    logger.info("Workflow validation passed")
    return True, "Workflow is valid"