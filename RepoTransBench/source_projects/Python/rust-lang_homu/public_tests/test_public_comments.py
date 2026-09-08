import pytest

from homu import comments as comments_mod

def test_strip_mention_from_message():
    msg = "@botuser please test"
    assert comments_mod.strip_mention(msg) == "please test"
    msg = "  @dev hello Homu!**  "
    assert comments_mod.strip_mention(msg) == "hello Homu!**"