import pytest
from wikipediaapi import Namespace, ExtractFormat, namespace2int

def test_public_namespace_enum_members():
    # Use different but valid namespace values
    assert Namespace.TALK == 1
    assert Namespace.PROJECT == 4
    assert Namespace.FILE == 6
    assert Namespace.PORTAL == 100
    assert Namespace.GADGET_TALK == 2301

def test_public_extractformat_enum_members():
    # Reversed to test both, still covers both values
    assert ExtractFormat.HTML == 2
    assert ExtractFormat.WIKI == 1

def test_public_namespace2int_with_enum_other():
    assert namespace2int(Namespace.FILE) == 6
    assert namespace2int(Namespace.PORTAL) == 100

def test_public_namespace2int_with_different_int():
    assert namespace2int(99) == 99
    assert namespace2int(6) == 6

def test_public_invalid_namespace2int_other():
    # Should not raise
    assert namespace2int(Namespace.PROJECT_TALK) == Namespace.PROJECT_TALK.value

def test_public_extractformat_repr_other():
    assert ExtractFormat.HTML.name == 'HTML'
    assert ExtractFormat.WIKI.name == 'WIKI'