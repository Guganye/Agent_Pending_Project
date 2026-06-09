import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.node import *
from core.llm import *

EXIT_SYMBOL = ["quit", "exit", "q"]

class ChatNode(Node):
    def exec(self, payload):
        messages = shared["messages"]
        assistant_message = call_llm(messages=messages)
        shared["messages"].append(assistant_message)
        return "output", assistant_message

class OutputNode(Node):
    def exec(self, payload):
        response = payload
        content = response.get("content", "")
        print(f"Assistant: {content}")
        return "default", None



if __name__ == "__main__":

    shared.clear()
    shared["messages"] = []

    chat_node = ChatNode()
    output_node = OutputNode()

    chat_node - "output" >> output_node

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



