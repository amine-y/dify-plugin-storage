# tools/set_strings_with_prefix_if_not_exist.py
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class SetStringsWithPrefixIfNotExistTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        prefix = tool_parameters.get("prefix", "")
        kv_list = tool_parameters.get("list", [])
        set_count = 0

        for item in kv_list:
            key = item.get("key")
            value = item.get("value")
            if key and value is not None:
                full_key = f"{prefix}{key}"
                if not self.session.storage.exist(full_key):
                    self.session.storage.set(full_key, value.encode())
                    set_count += 1

        yield self.create_text_message(f"SUCCESS: Set {set_count} new items.")
