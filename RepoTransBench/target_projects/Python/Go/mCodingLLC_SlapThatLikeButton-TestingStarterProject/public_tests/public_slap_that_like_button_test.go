package public_tests

import (
	"testing"

	"slapping/src/slapping"
)

func TestPublicSlapLike(t *testing.T) {
	cases := []struct {
		initial  slapping.LikeState
		expected slapping.LikeState
	}{
		{slapping.StateEmpty, slapping.StateLiked},
		{slapping.StateLiked, slapping.StateEmpty},
		{slapping.StateDisliked, slapping.StateLiked},
	}
	for _, tc := range cases {
		got, err := slapping.Slap(tc.initial, "l")
		if err != nil {
			t.Errorf("Slap(%v, \"l\") error: %v", tc.initial, err)
			continue
		}
		if got != tc.expected {
			t.Errorf("Slap(%v, \"l\") = %v; want %v", tc.initial, got, tc.expected)
		}
	}
}

func TestPublicSlapDislike(t *testing.T) {
	cases := []struct {
		initial  slapping.LikeState
		expected slapping.LikeState
	}{
		{slapping.StateEmpty, slapping.StateDisliked},
		{slapping.StateLiked, slapping.StateDisliked},
		{slapping.StateDisliked, slapping.StateEmpty},
	}
	for _, tc := range cases {
		got, err := slapping.Slap(tc.initial, "d")
		if err != nil {
			t.Errorf("Slap(%v, \"d\") error: %v", tc.initial, err)
			continue
		}
		if got != tc.expected {
			t.Errorf("Slap(%v, \"d\") = %v; want %v", tc.initial, got, tc.expected)
		}
	}
}

func TestPublicSlapInvalidAction(t *testing.T) {
	_, err := slapping.Slap(slapping.StateEmpty, "x")
	if err == nil {
		t.Errorf("Expected error for Slap(empty, \"x\"), got nil")
	}
}

func TestPublicSlapManyLikeStreak(t *testing.T) {
	got, err := slapping.SlapMany(slapping.StateLiked, "ll")
	if err != nil {
		t.Errorf("SlapMany error: %v", err)
	}
	if got != slapping.StateLiked {
		t.Errorf("SlapMany(liked, \"ll\") = %v; want %v", got, slapping.StateLiked)
	}
}

func TestPublicSlapManyDislikeStreak(t *testing.T) {
	got, err := slapping.SlapMany(slapping.StateDisliked, "d")
	if err != nil {
		t.Errorf("SlapMany error: %v", err)
	}
	if got != slapping.StateEmpty {
		t.Errorf("SlapMany(disliked, \"d\") = %v; want %v", got, slapping.StateEmpty)
	}
	got, err = slapping.SlapMany(slapping.StateEmpty, "dd")
	if err != nil {
		t.Errorf("SlapMany error: %v", err)
	}
	if got != slapping.StateEmpty {
		t.Errorf("SlapMany(empty, \"dd\") = %v; want %v", got, slapping.StateEmpty)
	}
}

func TestPublicStatesTransitionsNewCases(t *testing.T) {
	cases := []struct {
		initial  slapping.LikeState
		seq      string
		expected slapping.LikeState
	}{
		{slapping.StateEmpty, "dll", slapping.StateLiked},
		{slapping.StateLiked, "dl", slapping.StateDisliked},
		{slapping.StateLiked, "dld", slapping.StateEmpty},
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

func TestPublicStatesSlapManySimpleVariants(t *testing.T) {
	cases := []struct {
		initial  slapping.LikeState
		seq      string
		expected slapping.LikeState
	}{
		{slapping.StateEmpty, "", slapping.StateEmpty},
		{slapping.StateEmpty, "l", slapping.StateLiked},
		{slapping.StateLiked, "d", slapping.StateDisliked},
		{slapping.StateDisliked, "l", slapping.StateLiked},
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

func TestPublicAutoSlapLikes(t *testing.T) {
	cases := []struct {
		presses  int
		expected slapping.LikeState
	}{
		{1, slapping.StateLiked},
		{2, slapping.StateEmpty},
		{3, slapping.StateLiked},
		{6, slapping.StateEmpty},
	}
	for _, tc := range cases {
		got, err := slapping.AutoSlap(tc.presses, "like")
		if err != nil {
			t.Errorf("AutoSlap error: %v", err)
		}
		if got != tc.expected {
			t.Errorf("AutoSlap(%d, \"like\") = %v; want %v", tc.presses, got, tc.expected)
		}
	}
}

func TestPublicAutoSlapDislikes(t *testing.T) {
	cases := []struct {
		presses  int
		expected slapping.LikeState
	}{
		{1, slapping.StateDisliked},
		{2, slapping.StateEmpty},
		{3, slapping.StateDisliked},
		{6, slapping.StateEmpty},
	}
	for _, tc := range cases {
		got, err := slapping.AutoSlap(tc.presses, "dislike")
		if err != nil {
			t.Errorf("AutoSlap error: %v", err)
		}
		if got != tc.expected {
			t.Errorf("AutoSlap(%d, \"dislike\") = %v; want %v", tc.presses, got, tc.expected)
		}
	}
}

func TestPublicAutoSlapInvalid(t *testing.T) {
	invalidActions := []string{"foo", "", " "}
	for _, action := range invalidActions {
		_, err := slapping.AutoSlap(1, action)
		if err == nil {
			t.Errorf("expected error for AutoSlap(1, %q), got nil", action)
		}
	}
}