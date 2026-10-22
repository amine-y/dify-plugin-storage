from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._storage import get_optional


class GetStringTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        value = get_optional(self.session.storage, tool_parameters["key"])
        yield self.create_text_message(value.decode() if value is not None else "")
