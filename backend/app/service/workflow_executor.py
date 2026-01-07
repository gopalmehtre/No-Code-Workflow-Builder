from typing import Dict, List, Any
from app.core.components import create_component
from app.core.validator import validate_workflow
import logging

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    
    def __init__(self, nodes: List[Dict], edges: List[Dict]):
        self.nodes = nodes
        self.edges = edges
        self.components = {}
        self.adjacency = {}
        self._build_adjacency()
        self._create_components()
    
    def _build_adjacency(self):
        for edge in self.edges:
            source = edge.get("source")
            target = edge.get("target")
            if source not in self.adjacency:
                self.adjacency[source] = []
            self.adjacency[source].append(target)
    
    def _create_components(self):
        for node in self.nodes:
            node_id = node.get("id")
            node_type = node.get("type")
            config = node.get("data", {})
            
            try:
                component = create_component(node_type, node_id, config)
                self.components[node_id] = component
                logger.info(f"Created component: {node_type} [{node_id}]")
            except Exception as e:
                logger.error(f"Error creating component {node_id}: {str(e)}")
                raise
    
    def _find_start_node(self) -> str:
        from app.core.components import ComponentType
        
        for node in self.nodes:
            if node.get("type") == ComponentType.USER_QUERY:
                return node.get("id")
        
        raise ValueError("No UserQuery component found")
    
    def _get_execution_order(self) -> List[str]:
        visited = set()
        order = []
        
        def dfs(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            
            # Visit children first
            for neighbor in self.adjacency.get(node_id, []):
                dfs(neighbor)
            
            # Add to order after visiting children
            order.append(node_id)
        
        start_node = self._find_start_node()
        dfs(start_node)
        
        # Reverse to get correct order
        order.reverse()
        return order
    
    def execute(self, query: str) -> Dict[str, Any]:
        try:
            # Validate workflow
            is_valid, error_msg = validate_workflow(self.nodes, self.edges)
            if not is_valid:
                return {
                    "success": False,
                    "error": f"Invalid workflow: {error_msg}"
                }
            
            # Get execution order
            execution_order = self._get_execution_order()
            logger.info(f"Execution order: {execution_order}")
            
            # Initialize data with query
            current_data = {"query": query}
            execution_log = []
            
            # Execute components in order
            for node_id in execution_order:
                component = self.components.get(node_id)
                if not component:
                    logger.warning(f"Component {node_id} not found, skipping")
                    continue
                
                logger.info(f"Executing component: {component.type} [{node_id}]")
                
                try:
                    # Execute component
                    result = component.execute(current_data)
                    
                    # Update current data with result
                    current_data.update(result)
                    
                    # Log execution
                    execution_log.append({
                        "node_id": node_id,
                        "component_type": str(component.type),
                        "success": True
                    })
                    
                    logger.info(f"Component {node_id} executed successfully")
                
                except Exception as e:
                    logger.error(f"Error executing component {node_id}: {str(e)}")
                    execution_log.append({
                        "node_id": node_id,
                        "component_type": str(component.type),
                        "success": False,
                        "error": str(e)
                    })
                    return {
                        "success": False,
                        "error": f"Error in component {node_id}: {str(e)}",
                        "execution_log": execution_log
                    }
            
            # Return final result
            return {
                "success": True,
                "query": query,
                "response": current_data.get("response", ""),
                "execution_log": execution_log,
                "metadata": {
                    "components_executed": len(execution_log),
                    "model": current_data.get("model"),
                    "tokens": current_data.get("tokens", 0)
                }
            }
        
        except Exception as e:
            logger.error(f"Workflow execution error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

def execute_workflow(nodes: List[Dict], edges: List[Dict], query: str) -> Dict[str, Any]:
    executor = WorkflowExecutor(nodes, edges)
    return executor.execute(query)