import sys
from pathlib import Path
from typing import Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.node import *
from core.llm import *
from tools.builtins.search import search as search_ddgs

class QueryNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        return "search", payload

class SearchNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        results = search_ddgs(query=str(payload), max_results=3)
        titles = [r.get("title") or r.get("body") or "" for r in results]
        summary_input = "|".join([t for t in titles if t])
        return "summarize", summary_input

class SummarizeNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        prompt=f"基于以下要点写一句话摘要：{payload}"
        text = call_llm_simple(prompt)
        return "default", text

if __name__ == "__main__":
    query_node = QueryNode()
    search_node = SearchNode()
    summarize_node = SummarizeNode()

    query_node - "search" >> search_node
    search_node - "summarize" >> summarize_node

    flow = Flow(query_node)
    _, ans = flow.run("python")
    print(f"Workflow输出：{ans}")


