#!/usr/bin/env python3
"""
一个简单的本地 mcp 服务器
提供：加法、减法、获取当前时间 三个工具
"""

import asyncio
import json
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 创建服务器实例
server = Server("server")


# 1. 定义工具列表（暴露给 AI 的能力）
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """返回所有可用工具的描述"""
    return [
        Tool(
            name="add",
            description="两个数字相加",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个数字"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="subtract",
            description="两个数字相减",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "被减数"},
                    "b": {"type": "number", "description": "减数"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="get_current_time",
            description="获取当前日期和时间",
            inputSchema={
                "type": "object",
                "properties": {},  # 无需参数
            }
        )
    ]


# 2. 处理工具调用
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """根据工具名称执行对应的函数"""

    if name == "add":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [TextContent(type="text", text=str(result))]

    elif name == "subtract":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a - b
        return [TextContent(type="text", text=str(result))]

    elif name == "get_current_time":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [TextContent(type="text", text=f"当前时间：{now}")]

    else:
        raise ValueError(f"未知工具: {name}")


# 3. 启动服务器
async def main():
    """通过 stdio 与客户端通信"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, raise_exceptions=True)


if __name__ == "__main__":
    pass
    # asyncio.run(main())