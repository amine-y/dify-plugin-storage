# tools/get_string_with_default.py
import json
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._storage import get_optional

class GetStringWithDefaultTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        key = tool_parameters.get("key")
        default_value = tool_parameters.get("default")

        value = get_optional(self.session.storage, key)

        if value is not None:
            yield self.create_text_message(json.dumps({"value": value.decode()}))
        else:
            yield self.create_text_message(json.dumps({"value": default_value}))
