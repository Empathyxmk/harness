import pytest

import sys
import types

# Build a mock 'transform' module for demonstration
transform = types.SimpleNamespace()

def _transform(doclets):
    # filter out kind: 'file', 'package', 'module' with undocumented, or [undocumented==True]
    return [
        d for d in doclets
        if d.get("kind") not in ["file", "package"]
           and not d.get("undocumented", False)
    ]

def _setIsExportedFlag(doclet):
    if doclet.get("kind") == "member" and str(doclet.get("name", "")).startswith("module:"):
        doclet["isExported"] = True
        doclet["memberof"] = doclet["longname"]
    else:
        doclet["isExported"] = None
    return doclet

def _setCodename(doclet):
    doclet["codeName"] = doclet.get("meta", {}).get("code", {}).get("name")
    return doclet

def _setID(doclet):
    if doclet.get("kind") == "member":
        if "longname" in doclet:
            doclet["id"] = (
                f"{doclet['longname']}--{doclet.get('codeName', '')}"
                if doclet.get("isExported") else doclet["longname"]
            )
        return doclet
    if doclet.get("kind") == "constructor":
        doclet["id"] = doclet.get("longname", "")
        if doclet.get("scope") == "static":
            doclet.pop("scope", None)
        elif doclet.get("scope") == "instance":
            doclet["id"] += "()"
            doclet.pop("scope", None)
        return doclet
    return doclet

def _createConstructor(doclet):
    if doclet.get("kind") != "class":
        raise Exception("only pass a class")
    class_doc = doclet.copy()
    ctor_doc = dict(class_doc)
    ctor_doc["kind"] = "constructor"
    class_doc["description"] = class_doc.get("classdesc", "")
    class_doc.pop("classdesc", None)
    return [class_doc, ctor_doc]

transform.__call__ = _transform
transform.setIsExportedFlag = _setIsExportedFlag
transform.setCodename = _setCodename
transform.setID = _setID
transform.createConstructor = _createConstructor

def buildDoclet(overrides):
    result = {
        "name": "SomeName",
        "longname": "SomeLongName",
        "kind": "member",
        "meta": { "code": { "name": "SomeName" } }
    }
    result.update(overrides)
    return result

def test_transform_strips_undocumented_package_file():
    input = [
        {"kind": "file"},
        {"kind": "package"},
        {"kind": "module", "undocumented": True},
        buildDoclet({})
    ]
    output = transform(input)
    assert len(output) == 1
    assert output[0]["kind"] == "member"

def test_setIsExportedFlag_flags_exports():
    doclet = buildDoclet({"name": "module:foo", "kind": "member"})
    transform.setIsExportedFlag(doclet)
    assert doclet["isExported"] is True
    assert doclet["memberof"] == doclet["longname"]

def test_setCodename_sets_correct_codeName():
    doclet = buildDoclet({})
    transform.setCodename(doclet)
    assert doclet["codeName"] == "SomeName"

def test_setID_with_exported():
    doclet = buildDoclet({
        "longname": "foo",
        "kind": "member",
        "isExported": True,
        "codeName": "bar"
    })
    transform.setID(doclet)
    assert doclet["id"] == "foo--bar"

def test_setID_with_constructor_and_static():
    doclet = buildDoclet({
        "longname": "abc",
        "kind": "constructor",
        "scope": "static"
    })
    transform.setID(doclet)
    assert doclet["id"] == "abc"
    assert "scope" not in doclet

def test_setID_with_constructor_and_instance():
    doclet = buildDoclet({
        "longname": "def",
        "kind": "constructor",
        "scope": "instance"
    })
    transform.setID(doclet)
    assert doclet["id"] == "def()"

def test_createConstructor_throws_on_non_class():
    doclet = buildDoclet({"kind": "function"})
    with pytest.raises(Exception, match="only pass a class"):
        transform.createConstructor(doclet)

# Needed to allow transform(x) directly since JS test is transform(input)
def transform(doclets):
    return transform.__call__(doclets)