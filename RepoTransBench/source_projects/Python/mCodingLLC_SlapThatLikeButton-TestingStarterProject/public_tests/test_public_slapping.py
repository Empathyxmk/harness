import pytest

from slapping.slap_that_like_button import (
    LikeState,
    slap,
    slap_many,
    auto_slap
)

def test_public_alternate_likes_dislikes():
    assert slap_many(LikeState.empty, "ldld") is LikeState.liked
    assert slap_many(LikeState.liked, "dldl") is LikeState.liked

def test_public_full_cycle():
    assert slap_many(LikeState.liked, "ldl") is LikeState.disliked

def test_public_invalid_slap_char_sequence():
    with pytest.raises(ValueError):
        slap_many(LikeState.empty, "zqyz")

@pytest.mark.parametrize("num,action,final", [
    (4, "like", LikeState.empty),
    (5, "like", LikeState.liked),
    (7, "dislike", LikeState.disliked),
    (0, "dislike", LikeState.empty),
])
def test_public_auto_slap_cycles(num, action, final):
    assert auto_slap(num, action) is final

def test_public_auto_slap_invalid_num():
    with pytest.raises(TypeError):
        auto_slap("not-an-integer", "like")