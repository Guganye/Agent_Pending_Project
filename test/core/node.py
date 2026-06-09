import time
from typing import Dict, Any

shared = {}
class Node:
    def __init__(self, max_retries: int = 1, wait: float = 0.0):
        self.successor: Dict = {}
        self._action: str = "default"
        self.max_retries, wait = max_retries, wait

    def exec(self, payload):
        raise NotImplementedError

    def _exec(self, payload):
        for cur_retry in range(self.max_retries):
            try:
                return self.exec(payload)
            except Exception as e:
                if cur_retry == self.max_retries - 1:
                    raise e
                if self.wait > 0:
                    time.sleep(self.wait)

        raise RuntimeError("Unexpected exception in Node._exec")

    def __rshift__(self, other):
        self.successor[self._action] = other
        self._action = "default"
        return other

    def __sub__(self, other: str):
        if not isinstance(other, str):
            raise TypeError("Node.__sub__ only accepts str")
        self._action = other or "default"
        return self

class Flow:
    def __init__(self, start):
        self.start = start
    def run(self, payload: Any):
        last_action, curr = "default", self.start
        while curr:
            last_action, payload = curr._exec(payload)
            curr = curr.successor.get(last_action)
        return last_action, payload
