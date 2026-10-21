# tools/check_key_existence.py
import json
from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._storage import get_optional

class CheckKeyExistenceTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        key = tool_parameters.get("key")
        value_bytes = get_optional(self.session.storage, key)

        if value_bytes is None:
            response = {"exists": False, "type": None}
        else:
            value_str = value_bytes.decode()
            try:
                # If it can be cast to a float, we'll call it a number
                float(value_str)
                key_type = "number"
            except ValueError:
                key_type = "string"
            response = {"exists": True, "type": key_type}

        yield self.create_text_message(json.dumps(response))
