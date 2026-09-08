import sys
import os

# Ensure json2html can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from json2html import Json2Html, json2html, convert

def test_public_json2html_instance_conversion():
    j2h = Json2Html()
    data = {"fruit": "banana", "quantity": 12}
    html = j2h.convert(data)
    assert "banana" in html
    assert "quantity" in html

def test_public_json2html_function_conversion():
    data = {"planet": "Mars", "distance": 225}
    html = json2html.convert(data)
    assert "Mars" in html
    assert "distance" in html

def test_public_convert_dict_with_none():
    data = {"exists": None, "name": "test"}
    html = convert(json=data)
    assert "None" in html or "none" in html

def test_public_convert_bool_values():
    data = {"sunny": True, "rainy": False}
    html = convert(json=data)
    assert "True" in html
    assert "False" in html

def test_public_convert_list_with_dicts_and_strings():
    data = [{"animal": "dog"}, "cat", {"animal": "bird"}]
    html = convert(json=data)
    assert "dog" in html
    assert "cat" in html
    assert "bird" in html

def test_public_json2html_custom_table_attributes():
    data = {"val": 40}
    html = convert(json=data, table_attributes='id="public_test_table" class="newtab"')
    assert 'id="public_test_table"' in html
    assert 'class="newtab"' in html

def test_public_json2html_list_of_dicts_diff():
    data = [{"model": "A", "year": 1990}, {"model": "B", "year": 2020}]
    html = convert(json=data)
    assert "model" in html
    assert "A" in html
    assert "B" in html
    assert "1990" in html
    assert "2020" in html

def test_public_json2html_escape_script():
    data = {"x": "<script>alert('a')</script>"}
    html = convert(json=data)
    assert "&lt;script&gt;" in html and "alert" in html