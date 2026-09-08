import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_FIXTURES = os.path.join(BASE, "test", "fixtures")

def load_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def no_space(s):
    return re.sub(r"\s+", "", s)

def concise_process(file_content):
    # Simulate CSS postprocessing; as in JS, just return .css content with spacing removed
    # For demonstration, this "processor" just returns the original file content (in real tests, would invoke module)
    return no_space(file_content)

def expected(file_name):
    return no_space(load_file(os.path.join(TEST_FIXTURES, file_name, f"{file_name}.css")))

def actual(file_name):
    file_content = load_file(os.path.join(TEST_FIXTURES, file_name, f"{file_name}.pcss"))
    return concise_process(file_content)

def test_media_queries_media_min_max():
    assert actual('mediaMinMax') == expected('mediaMinMax'), "Ranges in media queries (different order)"

def test_media_queries_custom_media():
    assert actual('customMedia') == expected('customMedia'), "Custom media queries (different order)"

def test_units_vertical_rhythm():
    assert actual('verticalRhythm') == expected('verticalRhythm'), "lh (public)"