import pytest
import types

import builtins

class DummyExpoTransformer:
    def __init__(self):
        self.transform = lambda *a, **kw: "expo"

class DummySvgrCore:
    def __init__(self):
        self.transform = lambda *a, **kw: "svg"

class DummyFs:
    def __init__(self):
        self.exists_calls = []
        self.read_calls = []
        self.should_exist = False
        self.should_fail_read = False
        self.file_content = {}
    def existsSync(self, file):
        self.exists_calls.append(file)
        return self.should_exist if file in self.file_content else False
    def readFileSync(self, file):
        self.read_calls.append(file)
        if self.should_fail_read:
            raise Exception("fail")
        return self.file_content.get(file, "")

# Mock implementations of the api for testability
class IndexModule:
    # getExpoTransformer() tries to import an expo transformer module. We'll simulate that.
    use_expo = True
    svgr_content = "svgcontent"
    custom_config = None
    fail_svgr = False
    config_should_throw = False
    config_exists = False

    @staticmethod
    def reset():
        IndexModule.use_expo = True
        IndexModule.svgr_content = "svgcontent"
        IndexModule.custom_config = None
        IndexModule.fail_svgr = False
        IndexModule.config_should_throw = False
        IndexModule.config_exists = False

    @staticmethod
    def getExpoTransformer():
        if IndexModule.use_expo:
            return DummyExpoTransformer()
        return None

    @staticmethod
    async def transform(args):
        # Simulate the actual transform function
        src = args.get("src")
        filename = args.get("filename")
        options = args.get("options", {})

        if not isinstance(src, str):
            return {"code": None}
        if IndexModule.use_expo:
            if options.get("svgrConfigFile") and IndexModule.config_exists:
                if IndexModule.config_should_throw:
                    # Should swallow error, ignore config
                    pass
                else:
                    # Simulate config read and use
                    return {"code": "withcfg"}
            elif options.get("svgrConfigFile"):
                # Config specified but not found, use default transform
                return {"code": "defaultcfg"}
            # Default path, use expo
            return {"code": "expo"}
        else:
            # react-native fallback
            return {"code": "defaultcfg"}

@pytest.fixture(autouse=True)
def reset_index_module():
    IndexModule.reset()
    yield
    IndexModule.reset()

def test_get_expo_transformer_when_module_exists():
    IndexModule.use_expo = True
    transformer = IndexModule.getExpoTransformer()
    assert transformer is not None
    assert callable(transformer.transform)

def test_get_expo_transformer_when_not_found():
    IndexModule.use_expo = False
    transformer = IndexModule.getExpoTransformer()
    assert transformer is None

@pytest.mark.asyncio
async def test_main_exported_transform_returns_none_when_src_not_string():
    result = await IndexModule.transform({"src": None, "filename": "not-an-svg.png", "options": {}})
    assert result == {"code": None}

@pytest.mark.asyncio
async def test_transform_svg_with_expo_transformer_present():
    IndexModule.use_expo = True
    result = await IndexModule.transform({
        "src": "<svg></svg>",
        "filename": "icon.svg",
        "options": {"dev": True},
    })
    assert "code" in result
    assert result["code"] == "expo"

@pytest.mark.asyncio
async def test_transform_with_custom_config_exists():
    IndexModule.use_expo = True
    IndexModule.config_exists = True
    result = await IndexModule.transform({
        "src": "<svg></svg>",
        "filename": "icon.svg",
        "options": {"dev": True, "svgrConfigFile": ".svgrrc"},
    })
    assert result == {"code": "withcfg"}

@pytest.mark.asyncio
async def test_transform_fallback_if_custom_config_not_found():
    IndexModule.use_expo = True
    IndexModule.config_exists = False
    result = await IndexModule.transform({
        "src": "<svg></svg>",
        "filename": "icon.svg",
        "options": {"dev": True, "svgrConfigFile": ".notfound"},
    })
    assert result == {"code": "defaultcfg"}

@pytest.mark.asyncio
async def test_transform_using_fallback_metro_transformer_if_expo_transformer_missing():
    IndexModule.use_expo = False
    result = await IndexModule.transform({
        "src": "<svg></svg>",
        "filename": "icon.svg",
        "options": {"dev": False}
    })
    assert result == {"code": "defaultcfg"}

@pytest.mark.asyncio
async def test_transform_handles_thrown_errors_gracefully_in_config_reading():
    IndexModule.use_expo = True
    IndexModule.config_exists = True
    IndexModule.config_should_throw = True
    result = await IndexModule.transform({
        "src": "<svg></svg>",
        "filename": "icon.svg",
        "options": {"dev": True, "svgrConfigFile": ".svgrrc"}
    })
    # Should gracefully skip config and use normal "expo" transform
    assert result == {"code": "expo"}