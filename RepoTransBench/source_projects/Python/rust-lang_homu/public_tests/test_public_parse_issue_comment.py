import pytest

from homu import parse_issue_comment as pic_mod

def test_parse_command_custom_case():
    assert pic_mod.parse_command("@homu: test-queue") == ("test-queue", "")

def test_parse_command_argumented():
    assert pic_mod.parse_command("@homu: clean bar") == ("clean", "bar")