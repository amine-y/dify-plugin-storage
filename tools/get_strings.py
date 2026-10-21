from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._storage import get_optional


class GetStringsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        keys: list[str] = tool_parameters.get("keys", [])

        if not isinstance(keys, list):
            raise ValueError("keys must be a list of strings")

        results = {}
        for key in keys:
            value = get_optional(self.session.storage, key)
            if value is not None:
                results[key] = value.decode()

        yield self.create_text_message(str(results))
