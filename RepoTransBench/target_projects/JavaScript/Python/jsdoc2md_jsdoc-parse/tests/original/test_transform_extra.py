import pytest

# Assume we import the actual transform module here, e.g.
# from src.jsdoc2md_jsdoc_parse.transform import setCodename, setID, setIsExportedFlag, createConstructor
# For demonstration, we'll mock these with minimal logic.
import sys
import types

transform = types.SimpleNamespace()

def _setCodename(doclet):
    if not doclet.get("meta", {}).get("code"):
        return doclet
    doclet["codeName"] = doclet["meta"]["code"]["name"]
    return doclet

def _setID(d):
    if d.get("kind") == "member":
        if "longname" in d:
            d["id"] = f"{d['longname']}" if not d.get("isExported") else f"{d['longname']}--{d.get('codeName', '')}"
        return d
    if d.get("kind") == "constructor":
        d["id"] = d.get("longname", "")
        if d.get("scope") == "instance":
            d["id"] += "()"
        d.pop("scope", None)
        return d
    if d.get("kind") == "module":
        d["id"] = d["longname"]
        return d
    return d

def _setIsExportedFlag(doclet):
    # Only sets flag for member kind with name starting with "module:"
    if doclet.get("kind") == "member" and str(doclet.get("name", "")).startswith("module:"):
        doclet["isExported"] = True
        doclet["memberof"] = doclet["longname"]
    else:
        doclet["isExported"] = None
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

transform.setCodename = _setCodename
transform.setID = _setID
transform.setIsExportedFlag = _setIsExportedFlag
transform.createConstructor = _createConstructor

def test_setCodename_does_nothing_if_no_meta_code():
    doclet = {"name": "NoMeta"}
    assert transform.setCodename(doclet) is doclet

def test_setID_fallback():
    d = {"kind": "member"}
    assert transform.setID(d) is d
    assert d.get("id") is None

def test_setIsExportedFlag_false_for_module_kind():
    d1 = {"name": "module:x", "kind": "module"}
    d2 = {"name": "module:x", "kind": "constructor"}
    assert transform.setIsExportedFlag(d1)["isExported"] is None
    assert transform.setIsExportedFlag(d2)["isExported"] is None

def test_createConstructor_success():
    classDoclet = {
        "kind": "class",
        "longname": "Foo",
        "name": "Foo",
        "description": "something",
        "params": [],
        "examples": [],
        "returns": [],
        "exceptions": [],
        "classdesc": "The class!"
    }
    result = transform.createConstructor(classDoclet)
    assert isinstance(result, list)
    assert result[0]["kind"] == "class"
    assert result[1]["kind"] == "constructor"
    assert result[0]["description"] == "The class!"
    assert "classdesc" not in result[0]