# tools/get_strings_with_prefix.py
import json
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._storage import get_optional

class GetStringsWithPrefixTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        prefix = tool_parameters.get("prefix", "")
        results = []

        # Assumes a scan_keys method exists to find keys by pattern
        matching_keys = self.session.storage.scan_keys(f"{prefix}*")

        for key_bytes in matching_keys:
            key = key_bytes.decode()
            value = get_optional(self.session.storage, key)
            if value is not None:
                results.append({
                    "key": key.removeprefix(prefix),
                    "value": value.decode()
                })

        yield self.create_text_message(json.dumps(results))
