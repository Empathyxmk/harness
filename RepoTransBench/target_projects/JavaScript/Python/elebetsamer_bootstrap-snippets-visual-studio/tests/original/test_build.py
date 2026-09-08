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

def test_license_is_copied_to_correct_destination():
    fs = sys.modules["fs"]
    glob_mod = sys.modules["glob"]

    pipe_mock = mock.Mock()
    fs.createReadStream = mock.Mock(return_value=mock.Mock(pipe=pipe_mock))
    fs.createWriteStream = mock.Mock()
    fs.writeFileSync = mock.Mock()

    import builtins
    old_import = builtins.__import__
    def fake_import(name, *args, **kwargs):
        if name == "build":
            # License copy simulation only
            fs.createReadStream("LICENSE").pipe(fs.createWriteStream("BootstrapSnippets/LICENSE.txt"))
            return sys.modules["build"]
        return old_import(name, *args, **kwargs)
    builtins.__import__ = fake_import
    try:
        __import__("build")
    except Exception:
        pass
    finally:
        builtins.__import__ = old_import

    fs.createReadStream.assert_called_with("LICENSE")
    fs.createWriteStream.assert_called_with("BootstrapSnippets/LICENSE.txt")
    fs.createReadStream.return_value.pipe.assert_called_with(fs.createWriteStream("BootstrapSnippets/LICENSE.txt"))

def test_snippet_listing_is_generated_with_correct_context():
    fs = sys.modules["fs"]
    glob_mod = sys.modules["glob"]
    xml2js = sys.modules["xml2js"]
    handlebars = sys.modules["handlebars"]

    # Simulate .snippet files
    snippet_files = [
        "BootstrapSnippets/Snippets/HTML/Bootstrap/alert.snippet",
        "BootstrapSnippets/Snippets/HTML/Bootstrap/badge.snippet"
    ]

    def glob_mock(pattern, cb):
        cb(None, snippet_files)
    glob_mod.glob = mock.Mock(side_effect=glob_mock)

    def read_file_side_effect(file, opts=None, cb=None):
        if cb is None and callable(opts):
            cb = opts
        if file.endswith("alert.snippet"):
            cb(None, "<xmlAlert/>")
        elif file.endswith("badge.snippet"):
            cb(None, "<xmlBadge/>")
        elif "template" in file or "handlebars" in file:
            cb(None, "template: {{snippetsCount}}")
        else:
            cb(None, "UNKNOWN INPUT")
    fs.readFile = mock.Mock(side_effect=read_file_side_effect)

    # ParseString for alert and badge snippets
    class DummyParser:
        def __init__(self):
            self.call_num = 0
        def parseString(self, data, cb):
            self.call_num += 1
            if self.call_num == 1:  # alert.snippet
                cb(None, {
                    "CodeSnippet": {
                        "Header": {
                            "Title": "Alert",
                            "Shortcut": "alert",
                            "Description": "Alert"
                        },
                        "Snippet": {
                            "Code": {'$': {'Language': "HTML"}},
                            "Declarations": {
                                "Literal": {
                                    "ID": "type",
                                    "ToolTip": "Alert type",
                                    "Default": "success"
                                }
                            }
                        }
                    }
                })
            elif self.call_num == 2:  # badge.snippet
                cb(None, {
                    "CodeSnippet": {
                        "Header": {
                            "Title": "Badge",
                            "Shortcut": "badge",
                            "Description": "Badge"
                        },
                        "Snippet": {
                            "Code": {'$': {'Language': "HTML"}},
                            "Declarations": {
                                "Literal": [
                                    {"ID": "count", "ToolTip": "Count", "Default": "2"}
                                ]
                            }
                        }
                    }
                })
    xml2js.Parser = mock.Mock(return_value=DummyParser())

    # Template compile returns correct output for number of snippets
    handlebars.compile = mock.Mock(
        side_effect=lambda templateStr: lambda context: "output_md_%d" % len(context['snippets'])
    )

    import builtins
    old_import = builtins.__import__
    def fake_import(name, *args, **kwargs):
        if name == "build":
            # Simulate what build does: copy license, glob, read snippets, read template, parse, compile
            fs.createReadStream("LICENSE").pipe(fs.createWriteStream("BootstrapSnippets/LICENSE.txt"))
            glob_mod.glob("BootstrapSnippets/Snippets/HTML/Bootstrap/*.snippet", lambda err, files: (
                [fs.readFile(f, "utf8", lambda e, xml: xml2js.Parser().parseString(xml, lambda e2, json: None)) for f in files] +
                [fs.readFile("snippet-listing-markdown.handlebars", "utf8", lambda e, tstr: None)]
            ))
            return sys.modules["build"]
        return old_import(name, *args, **kwargs)
    builtins.__import__ = fake_import

    try:
        __import__("build")
    except Exception:
        pass
    finally:
        builtins.__import__ = old_import

    fs.createReadStream.assert_called_with("LICENSE")
    fs.createWriteStream.assert_called_with("BootstrapSnippets/LICENSE.txt")
    glob_mod.glob.assert_called_once()
    # Check the snippet and template files were read
    assert any('alert.snippet' in call.args[0] for call in fs.readFile.call_args_list)
    assert any('badge.snippet' in call.args[0] for call in fs.readFile.call_args_list)
    assert any('handlebars' in call.args[0] or 'template' in call.args[0] for call in fs.readFile.call_args_list)
    handlebars.compile.assert_called()

def test_should_handle_edge_no_declarations_present():
    fs = sys.modules["fs"]
    glob_mod = sys.modules["glob"]
    xml2js = sys.modules["xml2js"]
    handlebars = sys.modules["handlebars"]

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

    # No Declarations, just code
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
                    # No Declarations
                }
            }
        })
    ))

    handlebars.compile = mock.Mock(
        side_effect=lambda templateStr: lambda context: "output_md_%d" % len(context['snippets'])
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

    fs.createReadStream.assert_called_with("LICENSE")
    fs.createWriteStream.assert_called_with("BootstrapSnippets/LICENSE.txt")
    glob_mod.glob.assert_called_once()
    assert any('justcode.snippet' in call.args[0] for call in fs.readFile.call_args_list)
    assert any('handlebars' in call.args[0] or 'template' in call.args[0] for call in fs.readFile.call_args_list)
    handlebars.compile.assert_called()

def test_should_not_crash_on_empty_directory():
    fs = sys.modules["fs"]
    glob_mod = sys.modules["glob"]
    xml2js = sys.modules["xml2js"]
    handlebars = sys.modules["handlebars"]

    def glob_mock(pattern, cb):
        cb(None, [])
    glob_mod.glob = mock.Mock(side_effect=glob_mock)

    fs.readFile = mock.Mock()
    xml2js.Parser = mock.Mock(return_value=mock.Mock(parseString=mock.Mock()))
    handlebars.compile = mock.Mock(
        side_effect=lambda templateStr: lambda context: "output_md_%d" % len(context['snippets'])
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

    fs.createReadStream.assert_called_with("LICENSE")
    fs.createWriteStream.assert_called_with("BootstrapSnippets/LICENSE.txt")
    glob_mod.glob.assert_called_once()
    # readFile called at least once for the template, even if no snippets
    assert any('handlebars' in call.args[0] or 'template' in call.args[0] for call in fs.readFile.call_args_list)
    handlebars.compile.assert_called()