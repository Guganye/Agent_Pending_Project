from typing import Dict, Callable, Any, List


class Tool:
    def __init__(
            self,
            name: str,
            description: str,
            parameters: Dict,
            fn: Callable
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.fn = fn

    def execute(self, **kwargs) -> Any:
        return self.fn(**kwargs)

    def to_llm_format(self) -> Dict:
        return {
            "type": "function",
            "function":{
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }

def get_builtins_tools() -> List[Tool]:
    from .search import search
    from .write import write_file

    return [
        Tool(
            name="search",
            description="Search the web for up-to-date information and return relevant results.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Maximum number of results"},
                },
            },
            fn=search
        ),
        Tool(
            name="write",
            description="Write content to a file. Creates parent directories automatically.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
            fn=write_file,
        ),
    ]