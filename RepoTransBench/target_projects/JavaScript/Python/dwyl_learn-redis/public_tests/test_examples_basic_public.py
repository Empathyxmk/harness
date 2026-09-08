import os

def test_public_examples_basic_js_exists_and_accessible():
    example_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'basic.js')
    assert os.path.exists(example_path)

def test_public_examples_basic_js_file_extension():
    example_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'basic.js')
    _, ext = os.path.splitext(example_path)
    assert ext == '.js'

def test_public_examples_basic_js_load_without_error():
    example_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'basic.js')
    with open(example_path, 'r', encoding="utf-8") as f:
        content = f.read()
    assert isinstance(content, str) and len(content) > 0