import pytest
from slapping.slap_that_like_button import (
    LikeState, slap_like, slap_dislike, slap_many,
    slap_like_transitions, slap_dislike_transitions
)

def test_slap_like_transitions():
    # LikeState.empty -> liked
    assert slap_like(LikeState.empty) is LikeState.liked
    # LikeState.liked -> empty
    assert slap_like(LikeState.liked) is LikeState.empty
    # LikeState.disliked -> liked
    assert slap_like(LikeState.disliked) is LikeState.liked

def test_slap_dislike_transitions():
    # LikeState.empty -> disliked
    assert slap_dislike(LikeState.empty) is LikeState.disliked
    # LikeState.liked -> disliked
    assert slap_dislike(LikeState.liked) is LikeState.disliked
    # LikeState.disliked -> empty
    assert slap_dislike(LikeState.disliked) is LikeState.empty

@pytest.mark.parametrize("initial,slap_seq,final", [
    (LikeState.liked, "", LikeState.liked),
    (LikeState.disliked, "", LikeState.disliked),
    (LikeState.liked, "l", LikeState.empty),   # liked->empty
    (LikeState.liked, "d", LikeState.disliked),# liked->disliked
    (LikeState.liked, "ld", LikeState.disliked), # liked->empty->disliked
    (LikeState.disliked, "l", LikeState.liked), # disliked->liked
    (LikeState.disliked, "d", LikeState.empty), # disliked->empty
    (LikeState.liked, "dl", LikeState.liked),     # liked->disliked->liked
])
def test_other_states_slap_many(initial, slap_seq, final):
    assert slap_many(initial, slap_seq) is final

def test_slap_many_invalid_uppercase():
    # Should handle upper/lower case correctly
    assert slap_many(LikeState.empty, 'L') is LikeState.liked
    assert slap_many(LikeState.liked, 'D') is LikeState.disliked
    assert slap_many(LikeState.disliked, 'L') is LikeState.liked
    # Mixed case
    assert slap_many(LikeState.empty, 'lD') is LikeState.disliked
    assert slap_many(LikeState.liked, 'Dl') is LikeState.liked

@pytest.mark.parametrize("bad_slap", ["x", "z", " ", "1", "-", "_", "LdX"])
def test_slap_many_invalid_input_raises(bad_slap):
    with pytest.raises(ValueError):
        slap_many(LikeState.empty, bad_slap)