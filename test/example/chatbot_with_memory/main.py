import os
import sys
from pathlib import Path
from typing import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ...core.llm import call_llm
from ...core.node import Node, Flow, shared
# from ...core.memory import Memory
from ...tools import get_tools, ToolExecutor
from ...core.memory import Memory


SYSTEM_PROMPT = (
    "你是一个会调用工具的助手。"
    "当问题涉及最新信息、模型版本、产品发布时间或事实核验时，优先先调用 search 工具，再基于搜索结果回答。"
    "若问题是本地文件/代码相关，优先使用 read/grep/find/ls 等本地工具。"
)

class ChatNode(Node):
    """发送消息给LLM，获取响应（可能包含tool_calls)"""

    def exec(self, payload: Any) -> Tuple[str, Any]:
        memory = shared["memory"]
        tools = shared["tools"]

        messages = memory.build_context(system_prompt=SYSTEM_PROMPT)
        assistant_message = call_llm(messages = messages, tools = tools)
        memory.add_message(assistant_message)

        if assistant_message.get("tool_calls"):
            return "tool_call", assistant_message

        return "output", assistant_message

class ToolCallNode(Node):
    """执行LLM返回的tool_calls"""

    def exec(self, payload: Any) -> Tuple[str, Any]:
        response = payload
        memory = shared["memory"]
        executor = shared["tool_executor"]

        tool_calls = executor.parse_tool_calls(response)
        results = executor.execute_all(tool_calls)

        for tool_call, result in zip(tool_calls, results):
            print(f"{tool_call}: {result}")
            print(f"{tool_call}: {result}")
            memory.add_message(result.to_message())

        return "chat", None

class OutputNode(Node):
    """输出助手回复"""

    def exec(self, payload: Any) -> Tuple[str, Any]:
        response = payload
        content = response.get("content", "")
        print(f"\n Assistant: {content}\n")
        return "default", None

def run_chat() -> None:
    """运行对话循环"""
    print("=" * 60)
    print("Chatbot with Memory")
    print("=" * 60)
    print("可用工具: read, write, edit, bash, grep, find, ls, search")
    print("记忆管理: 短期上下文 + 长期记忆 (自动压缩)")
    print("输入 'quit' 或 'exit' 退出\n")

    shared.clear()

    shared["memory"] = Memory()
    shared["tools"] = [t.to_llm_format() for t in get_tools()]
    shared["tool_executor"] = ToolExecutor()

    chat = ChatNode()
    tool_call = ToolCallNode()
    output = OutputNode()

    chat - "tool_call" >> tool_call
    tool_call - "chat" >> chat
    chat - "output" >> output

    while True:
        user_input = input("👤 You: ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print("\n再见！")
            break

        if not user_input:
            continue

        shared["memory"].add_message({"role": "user", "content": user_input})
        flow = Flow(chat)
        flow.run(None)

def main() -> None:
    run_chat()

if __name__ == "__main__":
    main()