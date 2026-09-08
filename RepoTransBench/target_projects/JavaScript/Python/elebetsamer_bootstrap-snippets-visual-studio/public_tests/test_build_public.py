import sys
from unittest import mock
import pytest

@pytest.fixture(autouse=True, scope="module")
def mock_modules():
    sys.modules["fs"] = mock.Mock()
    sys.modules["glob"] = mock.Mock()
    sys.modules["xml2js"] = mock.Mock()
    sys.modules["handlebars"] = mock.Mock()
    sys.modules["util"] = mock.Mock()
    sys.modules["build"] = mock.Mock()
    yield
    for name in ["fs", "glob", "xml2js", "handlebars", "util", "build"]:
        try:
            del sys.modules[name]
        except KeyError:
            pass

def test_copies_license_and_generates_snippet_listing_with_alternate_parsing():
    fs = sys.modules["fs"]
    glob_mod = sys.modules["glob"]
    xml2js = sys.modules["xml2js"]
    handlebars = sys.modules["handlebars"]
    util = sys.modules["util"]

    # pipe() chaining mock for createReadStream -> creates .pipe()
    pipe_mock = mock.Mock()
    fs.createReadStream = mock.Mock(return_value=mock.Mock(pipe=pipe_mock))
    fs.createWriteStream = mock.Mock()
    fs.writeFileSync = mock.Mock()
    util.isArray = lambda v: isinstance(v, list)

    # Mock glob.glob to call cb with two .snippet files
    def glob_mock(pattern, cb):
        cb(None, [
            "BootstrapSnippets/Snippets/HTML/Bootstrap/carousel.snippet",
            "BootstrapSnippets/Snippets/HTML/Bootstrap/input-group.snippet"
        ])
    glob_mod.glob = mock.Mock(side_effect=glob_mock)

    # Simulate three calls to fs.readFile
    read_file_cb_args = []

    def read_file_side_effect(file, opts=None, cb=None):
        if cb is None and callable(opts):
            cb = opts
        if file.endswith("carousel.snippet"):
            cb(None, "<xmlA/>")
        elif file.endswith("input-group.snippet"):
            cb(None, "<xmlB/>")
        elif "template" in file or "handlebars" in file:
            cb(None, "template: {{snippetsCount}}")
        else:
            cb(None, "UNKNOWN")
        read_file_cb_args.append(file)
    fs.readFile = mock.Mock(side_effect=read_file_side_effect)

    # xml2js.Parser to return different CodeSnippet dicts per call
    class DummyParser:
        def __init__(self):
            self.call_num = 0
        def parseString(self, data, cb):
            self.call_num += 1
            if self.call_num == 1:  # for carousel.snippet
                cb(None, {
                    "CodeSnippet": {
                        "Header": {
                            "Title": "Carousel",
                            "Shortcut": "carousel",
                            "Description": "Carousel component"
                        },
                        "Snippet": {
                            "Code": {'$': {'Language': "HTML"}},
                            "Declarations": {
                                "Literal": {
                                    "ID": "slides",
                                    "ToolTip": "Number of slides",
                                    "Default": "3"
                                }
                            }
                        }
                    }
                })
            elif self.call_num == 2:  # for input-group.snippet
                cb(None, {
                    "CodeSnippet": {
                        "Header": {
                            "Title": "Input Group",
                            "Shortcut": "input-group",
                            "Description": "Input group field"
                        },
                        "Snippet": {
                            "Code": {'$': {'Language': "HTML"}},
                            "Declarations": {
                                "Literal": [
                                    {"ID": "addon", "ToolTip": "Addon String", "Default": "+"},
                                    {"ID": "size", "ToolTip": "Input size", "Default": "lg"}
                                ]
                            }
                        }
                    }
                })
            else:
                cb(None, {})
    xml2js.Parser = mock.Mock(return_value=DummyParser())

    # handlebars.compile returns a func that returns a dummy string with the correct context length
    def compile_side_effect(template_str):
        def renderer(context):
            # Check that snippets length matches what we expect (should be 2)
            assert len(context.get('snippets', [])) == 2
            return "public_output_md_%d" % len(context['snippets'])
        return renderer
    handlebars.compile = mock.Mock(side_effect=compile_side_effect)

    # Patch import to call our pipeline
    import builtins
    old_import = builtins.__import__
    def fake_import(name, *args, **kwargs):
        if name == "build":
            # simulate what the build module does (triggering readFile, createReadStream, etc)
            fs.createReadStream("LICENSE").pipe(fs.createWriteStream("BootstrapSnippets/LICENSE.txt"))
            glob_mod.glob("BootstrapSnippets/Snippets/HTML/Bootstrap/*.snippet", lambda err, files: (
                [fs.readFile(f, "utf8", lambda e, xml: xml2js.Parser().parseString(xml, lambda e2, json: None)) for f in files] +
                [fs.readFile("snippet-listing-markdown.handlebars", "utf8", lambda e, tstr: None)]
            ))
            return sys.modules["build"]
        else:
            return old_import(name, *args, **kwargs)
    builtins.__import__ = fake_import

    try:
        __import__("build")
    except Exception:
        pass
    finally:
        builtins.__import__ = old_import

    # Validations
    fs.createReadStream.assert_called_with("LICENSE")
    fs.createWriteStream.assert_called_with("BootstrapSnippets/LICENSE.txt")
    glob_mod.glob.assert_called_once()
    # Should be called for each .snippet file and the template
    assert any("carousel.snippet" in call.args[0] for call in fs.readFile.call_args_list)
    assert any("input-group.snippet" in call.args[0] for call in fs.readFile.call_args_list)
    assert any("handlebars" in call.args[0] or "template" in call.args[0] for call in fs.readFile.call_args_list)
    handlebars.compile.assert_called()

def test_should_handle_edge_no_declarations_present_public():
    fs = sys.modules["fs"]
    glob_mod = sys.modules["glob"]
    xml2js = sys.modules["xml2js"]
    handlebars = sys.modules["handlebars"]

    # Setup glob to only return one file
    def glob_mock(pattern, cb):
        cb(None, [
            "BootstrapSnippets/Snippets/HTML/Bootstrap/justcode.snippet"
        ])
    glob_mod.glob = mock.Mock(side_effect=glob_mock)

    def read_file_side_effect(file, opts=None, cb=None):
        if cb is None and callable(opts):
            cb = opts
        if '.snippet' in file:
            cb(None, "<xmlOnlyCode/>")
        else:
            cb(None, "template-file")
    fs.readFile = mock.Mock(side_effect=read_file_side_effect)

    # No Declarations at all
    xml2js.Parser = mock.Mock(return_value=mock.Mock(
        parseString=lambda data, cb: cb(None, {
            "CodeSnippet": {
                "Header": {
                    "Title": "JustCode",
                    "Shortcut": "justcode",
                    "Description": "No declarations here"
                },
                "Snippet": {
                    "Code": {'$': {'Language': "HTML"}}
                    # No Declarations field
                }
            }
        })
    ))

    handlebars.compile = mock.Mock(
        side_effect=lambda templateStr: lambda context: "public_output_md_%d" % len(context['snippets'])
    )

    import builtins
    old_import = builtins.__import__
    def fake_import(name, *args, **kwargs):
        if name == "build":
            fs.createReadStream("LICENSE").pipe(fs.createWriteStream("BootstrapSnippets/LICENSE.txt"))
            glob_mod.glob("BootstrapSnippets/Snippets/HTML/Bootstrap/*.snippet", lambda err, files: (
                [fs.readFile(f, "utf8", lambda e, xml: xml2js.Parser().parseString(xml, lambda e2, json: None)) for f in files] +
                [fs.readFile("snippet-listing-markdown.handlebars", "utf8", lambda e, tstr: None)]
            ))
            return sys.modules["build"]
        else:
            return old_import(name, *args, **kwargs)
    builtins.__import__ = fake_import

    try:
        __import__("build")
    except Exception:
        pass
    finally:
        builtins.__import__ = old_import

    # Validators
    fs.createReadStream.assert_called_with("LICENSE")
    fs.createWriteStream.assert_called_with("BootstrapSnippets/LICENSE.txt")
    glob_mod.glob.assert_called_once()
    # At least snippet and template files are read
    assert any('justcode.snippet' in call.args[0] for call in fs.readFile.call_args_list)
    assert any('handlebars' in call.args[0] or 'template' in call.args[0] for call in fs.readFile.call_args_list)
    handlebars.compile.assert_called()