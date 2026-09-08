import pytest
import types

transform = types.SimpleNamespace()

def _setIsExportedFlag(doclet):
    # Only sets flag for member kind with name starting with "module:"
    if doclet.get("kind") == "member" and str(doclet.get("name", "")).startswith("module:"):
        doclet["isExported"] = True
        doclet["memberof"] = doclet["longname"]
    else:
        doclet["isExported"] = None
    return doclet

transform.setIsExportedFlag = _setIsExportedFlag

def test_setIsExportedFlag_returns_undefined_for_non_modules():
    d1 = {"name": "nonExported", "kind": "class"}
    d2 = {"name": "plainFunction", "kind": "function"}
    assert transform.setIsExportedFlag(d1)["isExported"] is None
    assert transform.setIsExportedFlag(d2)["isExported"] is None

def test_setIsExportedFlag_does_not_set_exported_for_unrelated_kind():
    d3 = {"name": "someVariable", "kind": "member"}
    # This would be exported only if the name starts with "module:", which does not
    assert transform.setIsExportedFlag(d3)["isExported"] is None