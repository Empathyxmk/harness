import sys
import os

# Ensure json2html can be imported for public tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from json2html import Json2Html, convert

def test_public_convert_simple_dict():
    # <th> not <td> for keys!
    data = {"animal": "Elephant", "region": "Africa"}
    html = convert(json=data)
    assert "<th>animal</th>" in html
    assert "<td>Elephant</td>" in html
    assert "<th>region</th>" in html
    assert "<td>Africa</td>" in html

def test_public_convert_list_of_numbers():
    # List of numbers => <ul><li>... (not a <table>)
    data = [400, 500, 600]
    html = convert(json=data)
    # Should be <ul><li>400</li><li>500</li><li>600</li></ul>
    assert html.startswith("<ul>")
    assert "<li>400</li>" in html
    assert "<li>500</li>" in html
    assert "<li>600</li>" in html

def test_public_convert_nested_dict_list():
    # List of dicts as value, tests for keys as <th>
    data = {"cars": [{"make": "Toyota", "year": 2010}, {"make": "Ford", "year": 2015}]}
    html = convert(json=data)
    assert "Toyota" in html
    assert "Ford" in html
    assert "year" in html and "make" in html

def test_public_convert_json_string():
    json_str = '{"genre": "Jazz", "artist": "Miles Davis"}'
    html = convert(json=json_str)
    assert "<th>genre</th>" in html
    assert "<td>Jazz</td>" in html
    assert "Miles Davis" in html

def test_public_convert_escape_html():
    # Dangerous tag -- will be escaped with &lt;
    data = {"malicious": "<img src='evil'>"}
    html = convert(json=data)
    assert "&lt;img" in html

def test_public_convert_bad_json_string():
    # Out-of-spec JSON should just be returned as a string with HTML escaped
    bad_json = '{"foo": bar'  # bad JSON (missing quote on bar, missing trailing })
    html = convert(json=bad_json)
    assert isinstance(html, str)
    assert '{&quot;foo&quot;: bar' in html

def test_public_convert_empty_object():
    data = {}
    html = convert(json=data)
    # According to implementation, empty dict gives ""
    assert html == ""

def test_public_convert_empty_list():
    data = []
    html = convert(json=data)
    assert html == ""