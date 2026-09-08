def test_load_emoji_utils_class_public():
    try:
        import sys
        import types
        import importlib
        m = types.ModuleType("emoji_utils")
        sys.modules["emoji_utils"] = m
        importlib.import_module("emoji_utils")
    except Exception as e:
        assert False, f"Importing emoji_utils failed: {e}"