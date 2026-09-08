import pytest

from slapping.slap_that_like_button import (
    LikeState,
    slap,
    slap_many,
    auto_slap
)

@pytest.mark.parametrize("initial,expected", [
    (LikeState.empty, LikeState.liked),
    (LikeState.liked, LikeState.empty),
    (LikeState.disliked, LikeState.liked),
])
def test_public_slap_like(initial, expected):
    assert slap(initial, "l") is expected

@pytest.mark.parametrize("initial,expected", [
    (LikeState.empty, LikeState.disliked),
    (LikeState.liked, LikeState.disliked),
    (LikeState.disliked, LikeState.empty),
])
def test_public_slap_dislike(initial, expected):
    assert slap(initial, "d") is expected

def test_public_slap_invalid_action():
    with pytest.raises(ValueError):
        slap(LikeState.empty, "x")

def test_public_slap_many_like_streak():
    # like->empty->like->empty->like
    assert slap_many(LikeState.liked, "ll") is LikeState.liked

def test_public_slap_many_dislike_streak():
    # disliked->empty->disliked
    assert slap_many(LikeState.disliked, "d") is LikeState.empty
    assert slap_many(LikeState.empty, "dd") is LikeState.empty

@pytest.mark.parametrize("initial,slap_seq,final", [
    (LikeState.empty, "dll", LikeState.liked),
    (LikeState.liked, "dl", LikeState.disliked),
    (LikeState.liked, "dld", LikeState.empty),
])
def test_public_states_transitions_new_cases(initial, slap_seq, final):
    assert slap_many(initial, slap_seq) is final

@pytest.mark.parametrize("initial,slap_seq,final", [
    (LikeState.empty, "", LikeState.empty),
    (LikeState.empty, "l", LikeState.liked),
    (LikeState.liked, "d", LikeState.disliked),
    (LikeState.disliked, "l", LikeState.liked),
])
def test_public_states_slap_many_simple_variants(initial, slap_seq, final):
    assert slap_many(initial, slap_seq) is final

@pytest.mark.parametrize("presses,expected", [
    (1, LikeState.liked),
    (2, LikeState.empty),
    (3, LikeState.liked),
    (6, LikeState.empty),
])
def test_public_auto_slap_likes(presses, expected):
    assert auto_slap(presses, "like") is expected

@pytest.mark.parametrize("presses,expected", [
    (1, LikeState.disliked),
    (2, LikeState.empty),
    (3, LikeState.disliked),
    (6, LikeState.empty),
])
def test_public_auto_slap_dislikes(presses, expected):
    assert auto_slap(presses, "dislike") is expected

@pytest.mark.parametrize("action", ["foo", "", None])
def test_public_auto_slap_invalid(action):
    with pytest.raises(ValueError):
        auto_slap(1, action)