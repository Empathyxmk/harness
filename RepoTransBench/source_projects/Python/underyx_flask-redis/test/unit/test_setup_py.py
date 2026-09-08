import sys
import types
import pytest
import os
import importlib.util

def test_read_reads_file(tmp_path):
    # just test the read function without triggering setup()
    test_text = "abc"
    pkg_dir = tmp_path/"flask_redis"
    pkg_dir.mkdir()
    file_path = pkg_dir/"dummy.py"
    file_path.write_text(test_text, encoding="utf-8")

    setup_file = tmp_path/"setup.py"
    setup_code = """
import os
def read(*paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, *paths), "r", encoding="utf-8") as f:
        return f.read()
"""
    setup_file.write_text(setup_code)
    sys.path.insert(0, str(tmp_path))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("setup_tmp", str(setup_file))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mod.read("flask_redis", "dummy.py")
        assert result == test_text
    finally:
        sys.path.pop(0)

def test_find_meta_success(tmp_path):
    # Use proper regex and no double braces
    setup_file = tmp_path/"setup.py"
    setup_code = '''
import re
def read(*paths):
    return "__title__ = 'foo'\\n__description__ = 'bar'"
def find_meta(meta):
    meta_match = re.search(r"__" + re.escape(meta) + r"__\\s*=\\s*[\\'\\"]([^\\'\\"]*)[\\'\\"]", read())
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{}__ string.".format(meta))
'''
    setup_file.write_text(setup_code)
    sys.path.insert(0, str(tmp_path))
    try:
        spec = importlib.util.spec_from_file_location("setup_tmp", str(setup_file))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result1 = mod.find_meta("title")
        result2 = mod.find_meta("description")
        assert result1 == "foo"
        assert result2 == "bar"
    finally:
        sys.path.pop(0)

def test_find_meta_failure(tmp_path):
    # Use proper regex and no double braces
    setup_file = tmp_path/"setup.py"
    setup_code = '''
def read(*paths):
    return ""
def find_meta(meta):
    import re
    meta_match = re.search(r"__" + re.escape(meta) + r"__\\s*=\\s*[\\'\\"]([^\\'\\"]*)[\\'\\"]", read())
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{}__ string.".format(meta))
'''
    setup_file.write_text(setup_code)
    sys.path.insert(0, str(tmp_path))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("setup_tmp", str(setup_file))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with pytest.raises(RuntimeError):
            mod.find_meta("whatever")
    finally:
        sys.path.pop(0)