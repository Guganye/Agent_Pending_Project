from typing import Any, Dict, List

from ddgs import DDGS

def search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    with DDGS() as dgs:
        result = dgs.text(query=query, max_results=max_results)
    return list(result)

