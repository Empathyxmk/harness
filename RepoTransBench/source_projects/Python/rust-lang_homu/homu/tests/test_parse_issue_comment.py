import pytest

from homu import parse_issue_comment as pic_mod

def test_parse_command_cases():
    assert pic_mod.parse_command("@homu: retry") == ("retry", "")
    assert pic_mod.parse_command("@homu: clean foo") == ("clean", "foo")