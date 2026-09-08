import pytest
from wikipediaapi import Namespace, ExtractFormat, namespace2int

def test_namespace_enum_members():
    # Spot check a few enum values
    assert Namespace.MAIN == 0
    assert Namespace.USER == 2
    assert Namespace.CATEGORY == 14
    assert Namespace.BOOK == 108
    assert Namespace.GADGET == 2300

def test_extractformat_enum_members():
    assert ExtractFormat.WIKI == 1
    assert ExtractFormat.HTML == 2

def test_namespace2int_with_enum():
    assert namespace2int(Namespace.MAIN) == 0
    assert namespace2int(Namespace.CATEGORY) == 14

def test_namespace2int_with_int():
    assert namespace2int(42) == 42
    assert namespace2int(0) == 0

def test_invalid_namespace2int():
    # Should not raise
    assert namespace2int(Namespace.USER_TALK) == Namespace.USER_TALK.value

def test_extractformat_repr():
    assert ExtractFormat.WIKI.name == 'WIKI'
    assert ExtractFormat.HTML.name == 'HTML'