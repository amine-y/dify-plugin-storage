# tools/get_strings_with_prefix_with_default.py
import json
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._storage import get_optional

class GetStringsWithPrefixWithDefaultTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        prefix = tool_parameters.get("prefix", "")
        default_value = tool_parameters.get("default")
        results = []

        matching_keys = self.session.storage.scan_keys(f"{prefix}*")

        if not matching_keys:
             # If no keys match the prefix, maybe we should return something,
             # but the prompt example is ambiguous. Returning empty list for now.
             pass

        for key_bytes in matching_keys:
            key = key_bytes.decode()
            value = get_optional(self.session.storage, key)
            results.append({
                "key": key.removeprefix(prefix),
                "value": value.decode() if value is not None else default_value
            })

        yield self.create_text_message(json.dumps(results))
