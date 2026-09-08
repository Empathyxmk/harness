import pytest

from homu import comments as comments_mod

def test_strip_mention():
    msg = "@homu r+"
    assert comments_mod.strip_mention(msg) == "r+"
    msg = " @Homu  approve please! "
    assert comments_mod.strip_mention(msg) == "approve please!"