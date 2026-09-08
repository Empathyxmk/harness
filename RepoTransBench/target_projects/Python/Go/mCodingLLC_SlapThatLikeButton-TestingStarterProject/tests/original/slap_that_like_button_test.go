package original

import (
	"testing"

	"slapping/src/slapping"
)

func TestSlapLikeTransitions(t *testing.T) {
	// LikeState.empty -> liked
	if got := slapping.SlapLike(slapping.StateEmpty); got != slapping.StateLiked {
		t.Errorf("slapLike(empty) = %v; want %v", got, slapping.StateLiked)
	}
	// LikeState.liked -> empty
	if got := slapping.SlapLike(slapping.StateLiked); got != slapping.StateEmpty {
		t.Errorf("slapLike(liked) = %v; want %v", got, slapping.StateEmpty)
	}
	// LikeState.disliked -> liked
	if got := slapping.SlapLike(slapping.StateDisliked); got != slapping.StateLiked {
		t.Errorf("slapLike(disliked) = %v; want %v", got, slapping.StateLiked)
	}
}

func TestSlapDislikeTransitions(t *testing.T) {
	// LikeState.empty -> disliked
	if got := slapping.SlapDislike(slapping.StateEmpty); got != slapping.StateDisliked {
		t.Errorf("slapDislike(empty) = %v; want %v", got, slapping.StateDisliked)
	}
	// LikeState.liked -> disliked
	if got := slapping.SlapDislike(slapping.StateLiked); got != slapping.StateDisliked {
		t.Errorf("slapDislike(liked) = %v; want %v", got, slapping.StateDisliked)
	}
	// LikeState.disliked -> empty
	if got := slapping.SlapDislike(slapping.StateDisliked); got != slapping.StateEmpty {
		t.Errorf("slapDislike(disliked) = %v; want %v", got, slapping.StateEmpty)
	}
}

func TestOtherStatesSlapMany(t *testing.T) {
	cases := []struct {
		initial  slapping.LikeState
		seq      string
		expected slapping.LikeState
	}{
		{slapping.StateLiked, "", slapping.StateLiked},
		{slapping.StateDisliked, "", slapping.StateDisliked},
		{slapping.StateLiked, "l", slapping.StateEmpty},
		{slapping.StateLiked, "d", slapping.StateDisliked},
		{slapping.StateLiked, "ld", slapping.StateDisliked},
		{slapping.StateDisliked, "l", slapping.StateLiked},
		{slapping.StateDisliked, "d", slapping.StateEmpty},
		{slapping.StateLiked, "dl", slapping.StateLiked},
	}
	for _, c := range cases {
		got, err := slapping.SlapMany(c.initial, c.seq)
		if err != nil {
			t.Errorf("SlapMany(%v, %q) error: %v", c.initial, c.seq, err)
		}
		if got != c.expected {
			t.Errorf("SlapMany(%v, %q) = %v; want %v", c.initial, c.seq, got, c.expected)
		}
	}
}

func TestSlapManyInvalidUppercase(t *testing.T) {
	tests := []struct {
		start   slapping.LikeState
		seq     string
		want    slapping.LikeState
	}{
		{slapping.StateEmpty, "L", slapping.StateLiked},
		{slapping.StateLiked, "D", slapping.StateDisliked},
		{slapping.StateDisliked, "L", slapping.StateLiked},
		{slapping.StateEmpty, "lD", slapping.StateDisliked},
		{slapping.StateLiked, "Dl", slapping.StateLiked},
	}
	for _, tc := range tests {
		got, err := slapping.SlapMany(tc.start, tc.seq)
		if err != nil {
			t.Errorf("SlapMany(%v, %q) returned error: %v", tc.start, tc.seq, err)
		}
		if got != tc.want {
			t.Errorf("SlapMany(%v, %q) = %v; want %v", tc.start, tc.seq, got, tc.want)
		}
	}
}

func TestSlapManyInvalidInputRaises(t *testing.T) {
	badSeqs := []string{"x", "z", " ", "1", "-", "_", "LdX"}
	for _, bad := range badSeqs {
		_, err := slapping.SlapMany(slapping.StateEmpty, bad)
		if err == nil {
			t.Errorf("expected error for SlapMany(empty, %q), got nil", bad)
		}
	}
}