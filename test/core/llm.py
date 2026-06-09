import os

from dotenv import load_dotenv
from openai import OpenAI

from typing import List, Dict, Any, Optional

load_dotenv()

SYSTEM_DEFAULT_PROMPT="You are a helpful assistant."
def call_llm_simple(prompt: str):
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    )

    response = client.chat.completions.create(
        model=os.getenv("DEEPSEEK_CURRENT_MODEL", "deepseek-v4-pro"),
        messages=[
            {"role":"system", "content":"You are a helpful assistant"},
            {"role":"user", "content":prompt}
        ]
    )

    message = response.choices[0].message
    return message.content or ""

def call_llm(
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
):
    msgs = list(messages)

    if system_prompt:
        messages = [{"role":"system", "content":system_prompt}, *msgs]

    kwargs = {
        "model": os.getenv("DEEPSEEK_CURRENT_MODEL", "deepseek-v4-pro"),
        "messages": messages,
    }

    if tools:
        kwargs["tools"]=tools

    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    )
    response = client.chat.completions.create(**kwargs)
    message = response.choices[0].message

    result = {
        "role": "assistant",
        "content": message.content or "",
        "usage":{
            "total_tokens": response.usage.total_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
        }
    }
    if hasattr(message, "reasoning_content"):
        result["reasoning_content"] = message.reasoning_content

    if message.tool_calls:
        result["tool_calls"] = [tool_call.model_dump() for tool_call in message.tool_calls]

    return result


    client = OpenAI()