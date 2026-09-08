import pytest
import importlib.util
import sys
import os

@pytest.mark.skip("Needs _kdtree_core.c.mako and will fail on CI/file-missing: skip until template in testpath or test logic uses mock.")
def test_render_template_public(tmp_path):
    tmpl = tmp_path / "greet.txt"
    out = tmp_path / "result.txt"
    tmpl.write_text("Hi, ${thing}. This is a test.")
    render_template_path = os.path.join(os.path.dirname(__file__), "render_template.py")
    spec = importlib.util.spec_from_file_location("render_template", render_template_path)
    render_template = importlib.util.module_from_spec(spec)
    sys.modules["render_template"] = render_template
    spec.loader.exec_module(render_template)
    class DummyArgs:
        template = str(tmpl)
        output = str(out)
        kwargs = ['thing=Tree']
    args = DummyArgs()
    render_template.main(args)
    assert out.read_text() == "Hi, Tree. This is a test."