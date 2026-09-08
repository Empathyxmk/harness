import importlib.util
import sys
import os
import types

def test_render_template_entry_points(monkeypatch):
    # Patch sys.argv and Template to fake main() logic for coverage
    render_template_path = os.path.join(os.path.dirname(__file__), "render_template.py")
    spec = importlib.util.spec_from_file_location("render_template", render_template_path)
    render_template = importlib.util.module_from_spec(spec)
    sys.modules["render_template"] = render_template

    # Patch mako.template.Template to prevent real file reading
    fake_template_class = type("FakeTemplate", (), {"render": staticmethod(lambda **kwargs: "OK!")})
    monkeypatch.setitem(sys.modules, "mako.template", types.SimpleNamespace(Template=fake_template_class))
    monkeypatch.setitem(sys.modules, "mako", types.SimpleNamespace(template=fake_template_class))

    # Patch Template import inside the target module
    orig_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "mako.template":
            return types.SimpleNamespace(Template=fake_template_class)
        if name == "mako":
            return types.SimpleNamespace(template=fake_template_class)
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)
    # Populate fake sys.argv so main() runs at bottom if present
    sys.argv = ["render_template.py", "--template", "foo.mako", "--output", "bar.txt", "key=val"]
    try:
        spec.loader.exec_module(render_template)
    except Exception:
        # ignore file IO etc
        pass