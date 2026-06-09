import json
from typing import Any, List, Dict

from .builtins.tool_def import get_builtins_tools as get_tools

class ToolCall:
    def __init__(self, id, name, arguments):
        self.id = id
        self.name = name
        self.arguments = arguments

    @classmethod
    def from_openai_item(cls, item:dict[str, Any]) -> 'ToolCall':
        function = item.get("function", {})
        arguments = function.get("arguments", {})
        if isinstance(arguments, str):
            arguments = _safe_json_loads(arguments)
        if not isinstance(arguments, dict):
            arguments = {}
        return cls(
            id = item.get("id", ""),
            name = function.get("name", ""),
            arguments = arguments,
        )
class ToolExecutor:
    def __init__(self):
        self.tools = get_tools()
        self.tool_map = {tool.name: tool for tool in self.tools}

    def parse_tool_calls(self, assistant_message: Dict[str, Any]) -> List[ToolCall]:

        openai_calls = assistant_message
        if isinstance(openai_calls, list):
            return [ToolCall.from_openai_item(item) for item in openai_calls]

    def execute(self, tool_call: ToolCall):
        tool = self.tool_map.get(tool_call.name)
        if not tool:
            return ToolResult(
                tool_call_id=tool_call.id,
                content=f"Tool'{tool_call.name}' not found.",
                is_error=True
            )
        try:
            raw_result = tool.execute(**tool_call.arguments)
        except Exception as e:
            return ToolResult(
                tool_call_id=tool_call.id,
                content=f"Error: {e}",
                is_error=True
            )
        return ToolResult(
            tool_call_id=tool_call.id,
            content=_stringify_result(raw_result),
            is_error=False
        )

    def execute_all(self, tool_calls: List[ToolCall]):
        return [self.execute(tool_call) for tool_call in tool_calls]

class ToolResult:
    def __init__(self, tool_call_id, content, is_error=False):
        self.tool_call_id = tool_call_id
        self.content = content
        self.is_error = is_error

    def to_message(self) -> Dict[str, str]:
        return {
            "role": "tool",
            "tool_call_id": self.tool_call_id,
            "content": self.content,
        }

def _safe_json_loads(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}

def _stringify_result(value: Any) -> str:
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value)
