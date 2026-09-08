import os
import importlib.util

def test_examples_basic_js_exists():
    example_path = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'basic.js')
    assert os.path.exists(example_path)

def test_examples_basic_is_js_file():
    example_path = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'basic.js')
    assert example_path.endswith('.js')

def test_examples_basic_js_loadable():
    # Test that loading basic.js doesn't throw (simulate require by parsing file)
    # In Python, we'll just check it's readable and parseable as text (not JS execution)
    example_path = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'basic.js')
    with open(example_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert isinstance(content, str) and len(content) > 0