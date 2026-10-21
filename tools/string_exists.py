# tools/string_exists.py
import json
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._storage import get_optional

class StringExistsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        key = tool_parameters.get("key")
        value = get_optional(self.session.storage, key)
        response = {"exists": value is not None}
        yield self.create_text_message(json.dumps(response))
