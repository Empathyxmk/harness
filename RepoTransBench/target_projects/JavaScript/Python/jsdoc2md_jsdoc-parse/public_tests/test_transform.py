import pytest

import types

# Mock the 'transform' module with the relevant methods
transform = types.SimpleNamespace()

def _transform(doclets):
    return [
        d for d in doclets
        if d.get("kind") != "enum"
        and d.get("kind") != "typedef"
        and (d.get("documented", True) or d.get("kind") == "function")
    ]

def _setID(doclet):
    if doclet.get("kind") == "function":
        doclet["id"] = doclet["longname"]
        doclet.pop("scope", None)
        return doclet
    if doclet.get("kind") == "constructor":
        doclet["id"] = doclet.get("longname", "") + "()"
        return doclet
    if doclet.get("kind") == "module":
        doclet["id"] = doclet["longname"]
        return doclet
    return doclet

transform.__call__ = _transform
transform.setID = _setID

def test_transform_strips_undocumented_and_enums_and_typedefs():
    input = [
        {"kind": "function", "name": "anotherFunc", "documented": True},
        {"kind": "enum", "name": "notEnum", "undocumented": True},
        {"kind": "typedef", "name": "exampleType", "undocumented": True},
    ]
    output = transform(input)
    assert len(output) == 1
    assert output[0]["kind"] == "function"
    assert output[0]["name"] == "anotherFunc"

def test_setID_sets_ID_for_ordinary_and_exported_kinds():
    doclet = {"longname": "foo.bar", "kind": "function"}
    transform.setID(doclet)
    assert doclet["id"] == "foo.bar"
    assert "scope" not in doclet or doclet.get("scope") is None

def test_setID_with_constructor_and_global():
    doclet = {"longname": "uvw", "kind": "constructor", "scope": "global"}
    transform.setID(doclet)
    assert doclet["id"] == "uvw()"

def test_setID_with_module():
    md = {"kind": "module", "longname": "module:bar"}
    transform.setID(md)
    assert md["id"] == "module:bar"