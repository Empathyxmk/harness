package public_tests

import (
	"testing"

	"slapping/src/slapping"
)

func TestPublicAlternateLikesDislikes(t *testing.T) {
	got, err := slapping.SlapMany(slapping.StateEmpty, "ldld")
	if err != nil {
		t.Errorf("SlapMany error: %v", err)
	}
	if got != slapping.StateLiked {
		t.Errorf("SlapMany(empty, \"ldld\") = %v; want %v", got, slapping.StateLiked)
	}
	got, err = slapping.SlapMany(slapping.StateLiked, "dldl")
	if err != nil {
		t.Errorf("SlapMany error: %v", err)
	}
	if got != slapping.StateLiked {
		t.Errorf("SlapMany(liked, \"dldl\") = %v; want %v", got, slapping.StateLiked)
	}
}

func TestPublicFullCycle(t *testing.T) {
	got, err := slapping.SlapMany(slapping.StateLiked, "ldl")
	if err != nil {
		t.Errorf("SlapMany error: %v", err)
	}
	if got != slapping.StateDisliked {
		t.Errorf("SlapMany(liked, \"ldl\") = %v; want %v", got, slapping.StateDisliked)
	}
}

func TestPublicInvalidSlapCharSequence(t *testing.T) {
	_, err := slapping.SlapMany(slapping.StateEmpty, "zqyz")
	if err == nil {
		t.Errorf("expected error for SlapMany(empty, \"zqyz\"), got nil")
	}
}

func TestPublicAutoSlapCycles(t *testing.T) {
	cases := []struct {
		num      int
		action   string
		expected slapping.LikeState
	}{
		{4, "like", slapping.StateEmpty},
		{5, "like", slapping.StateLiked},
		{7, "dislike", slapping.StateDisliked},
		{0, "dislike", slapping.StateEmpty},
	}
	for _, tc := range cases {
		got, err := slapping.AutoSlap(tc.num, tc.action)
		if err != nil {
			t.Errorf("AutoSlap error: %v", err)
		}
		if got != tc.expected {
			t.Errorf("AutoSlap(%d, %q) = %v; want %v", tc.num, tc.action, got, tc.expected)
		}
	}
}

func TestPublicAutoSlapInvalidNum(t *testing.T) {
	// In Go, passing a string where an int is required won't compile,
	// so this test does not have a direct equivalent.
}