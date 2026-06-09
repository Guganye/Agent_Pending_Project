import sys
from pathlib import Path
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.node import *
from core.llm import call_llm
from tools import get_tools, ToolExecutor

EXIT_SYMBOL=["quit", "exit", "q"]
class ChatNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        messages = shared["messages"]
        tools = shared["tools"]
        assistant_message = call_llm(messages=messages, tools=tools)
        messages.append(assistant_message)

        if assistant_message.get("content"):
            print(f"Assistant: {assistant_message['content']}")
        if assistant_message.get("tool_calls"):
            return "tool", assistant_message["tool_calls"]

        return "done", assistant_message

class ToolCallNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        response = payload
        messages = shared["messages"]
        executor = shared["tool_executor"]

        tool_calls = executor.parse_tool_calls(response)
        results = executor.execute_all(tool_calls)

        for tc, result in zip(tool_calls, results):
            print(f"[Tool]执行: {tc.name}({tc.arguments})")
            print(f"[Tool]结果: {result.content[:100]}...")
        messages.append(result.to_message())

        return "chat", None

def main():
    shared.clear()
    shared["messages"] = []
    shared["tools"] = [t.to_llm_format() for t in get_tools()]
    shared["tool_executor"] = ToolExecutor()
    chat_node = ChatNode()
    tool_node = ToolCallNode()

    chat_node - "tool" >> tool_node
    tool_node - "chat" >> chat_node

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in EXIT_SYMBOL:
            print("Goodbye!")
            break

        if not user_input:
            continue

        shared["messages"].append({"role":"user", "content":user_input})

        flow = Flow(chat_node)
        flow.run(None)


if __name__ == "__main__":
    main()


