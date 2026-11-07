"""Core Agent Prompt Taint Tracker implementation."""
from typing import Dict, Any, List


class TaintedValue:
    def __init__(self, value: str, source: str, is_tainted: bool = True):
        self.value = value
        self.source = source
        self.is_tainted = is_tainted

    def sanitize(self) -> "TaintedValue":
        # Returns sanitized copy
        return TaintedValue(self.value, self.source, is_tainted=False)


class AgentPromptTaintTracker:
    def __init__(self):
        self._tainted_registry: Dict[str, TaintedValue] = {}

    def register_untrusted(self, var_name: str, value: str, source: str = "web_scrape") -> TaintedValue:
        tv = TaintedValue(value, source, is_tainted=True)
        self._tainted_registry[var_name] = tv
        return tv

    def check_sink(self, sink_name: str, command_string: str) -> Dict[str, Any]:
        violations = []
        for var_name, tv in self._tainted_registry.items():
            if tv.is_tainted and tv.value in command_string:
                violations.append({
                    "variable": var_name,
                    "source": tv.source,
                    "tainted_value": tv.value
                })

        is_safe = len(violations) == 0
        return {
            "sink": sink_name,
            "is_safe": is_safe,
            "violations": violations
        }
