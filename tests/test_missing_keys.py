import json
import sys
import types
import unittest
from types import SimpleNamespace


class _Tool:
    def create_text_message(self, text):
        return text


_dify_plugin = types.ModuleType("dify_plugin")
_dify_plugin.Tool = _Tool
_entities = types.ModuleType("dify_plugin.entities")
_entities_tool = types.ModuleType("dify_plugin.entities.tool")
_entities_tool.ToolInvokeMessage = object
sys.modules.setdefault("dify_plugin", _dify_plugin)
sys.modules.setdefault("dify_plugin.entities", _entities)
sys.modules.setdefault("dify_plugin.entities.tool", _entities_tool)

from tools.check_key_existence import CheckKeyExistenceTool
from tools.get_string import GetStringTool
from tools.get_string_with_default import GetStringWithDefaultTool
from tools.get_strings import GetStringsTool
from tools.set_string_if_not_exist import SetStringIfNotExistTool


class FakeStorage:
    def __init__(self, values=None, *, exist_error=None):
        self.values = dict(values or {})
        self.exist_error = exist_error
        self.get_calls = []

    def exist(self, key):
        if self.exist_error is not None:
            raise self.exist_error
        return key in self.values

    def get(self, key):
        self.get_calls.append(key)
        if key not in self.values:
            raise RuntimeError("load data failed")
        return self.values[key]

    def set(self, key, value):
        self.values[key] = value


def invoke(tool_class, storage, parameters):
    tool = tool_class.__new__(tool_class)
    tool.session = SimpleNamespace(storage=storage)
    return list(tool._invoke(parameters))


class MissingKeyTests(unittest.TestCase):
    def test_get_string_returns_empty_text_without_loading_a_missing_key(self):
        storage = FakeStorage()

        messages = invoke(GetStringTool, storage, {"key": "missing"})

        self.assertEqual(messages, [""])
        self.assertEqual(storage.get_calls, [])

    def test_get_string_returns_an_existing_value(self):
        storage = FakeStorage({"token": b"stored-value"})

        messages = invoke(GetStringTool, storage, {"key": "token"})

        self.assertEqual(messages, ["stored-value"])
        self.assertEqual(storage.get_calls, ["token"])

    def test_get_string_still_surfaces_a_storage_availability_error(self):
        storage = FakeStorage(exist_error=RuntimeError("storage unavailable"))

        with self.assertRaisesRegex(RuntimeError, "storage unavailable"):
            invoke(GetStringTool, storage, {"key": "token"})

    def test_get_string_with_default_returns_the_default_for_a_missing_key(self):
        storage = FakeStorage()

        messages = invoke(
            GetStringWithDefaultTool,
            storage,
            {"key": "missing", "default": "fallback"},
        )

        self.assertEqual(json.loads(messages[0]), {"value": "fallback"})
        self.assertEqual(storage.get_calls, [])

    def test_get_strings_skips_missing_keys(self):
        storage = FakeStorage({"present": b"value"})

        messages = invoke(
            GetStringsTool,
            storage,
            {"keys": ["present", "missing"]},
        )

        self.assertEqual(messages, ["{'present': 'value'}"])
        self.assertEqual(storage.get_calls, ["present"])

    def test_existence_check_reports_a_missing_key_without_loading_it(self):
        storage = FakeStorage()

        messages = invoke(CheckKeyExistenceTool, storage, {"key": "missing"})

        self.assertEqual(json.loads(messages[0]), {"exists": False, "type": None})
        self.assertEqual(storage.get_calls, [])

    def test_set_if_absent_does_not_load_a_missing_key(self):
        storage = FakeStorage()

        messages = invoke(
            SetStringIfNotExistTool,
            storage,
            {"key": "token", "value": "value"},
        )

        self.assertEqual(messages, ["SUCCESS: Key 'token' was set."])
        self.assertEqual(storage.values, {"token": b"value"})
        self.assertEqual(storage.get_calls, [])


if __name__ == "__main__":
    unittest.main()
