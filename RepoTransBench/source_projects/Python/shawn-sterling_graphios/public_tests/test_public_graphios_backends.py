import sys
import os
import pathlib

# Ensure project root is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import graphios_backends

def test_public_strip_forbidden_chars():
    if hasattr(graphios_backends, "strip_forbidden_chars"):
        assert graphios_backends.strip_forbidden_chars("a/b:c*d?e<f>g|h") == "abcdefg"

def test_public_strip_and_lower():
    if hasattr(graphios_backends, "strip_and_lower"):
        assert graphios_backends.strip_and_lower("AbC-DeF_123") == "abc-def_123"

def test_public_string_cleanup():
    if hasattr(graphios_backends, "string_cleanup"):
        assert graphios_backends.string_cleanup("   Remove   Spaces   ") == "Remove Spaces"

def test_public_string_cleanup_replaces():
    if hasattr(graphios_backends, "string_cleanup"):
        assert graphios_backends.string_cleanup("strip\tit   now") == "strip it now"

def test_public_camel_case_to_underscore():
    if hasattr(graphios_backends, "camel_case_to_underscore"):
        assert graphios_backends.camel_case_to_underscore("PublicCaseToUnderscore") == "public_case_to_underscore"

def test_public_strip_unicode():
    if hasattr(graphios_backends, "strip_unicode"):
        text = u"café 漢字"
        result = graphios_backends.strip_unicode(text)
        assert "cafe" in result
        assert all(ord(c) < 128 for c in result)

def test_public_getattr_from_path():
    if hasattr(graphios_backends, "getattr_from_path"):
        class Dummy:
            class Inner:
                value = 404
        import types
        dummy_mod = types.ModuleType('dummy_mod')
        dummy_mod.Dummy = Dummy
        import sys
        sys.modules['dummy_mod'] = dummy_mod
        res = graphios_backends.getattr_from_path('dummy_mod.Dummy.Inner.value')
        assert res == 404