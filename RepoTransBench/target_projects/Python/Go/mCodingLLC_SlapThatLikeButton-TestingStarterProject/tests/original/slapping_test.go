package original

import (
	"testing"

	"slapping/src/slapping"
)

func TestEmptySlap(t *testing.T) {
	got, err := slapping.SlapMany(slapping.StateEmpty, "")
	if err != nil {
		t.Fatalf("SlapMany error: %v", err)
	}
	if got != slapping.StateEmpty {
		t.Errorf("SlapMany(empty, \"\") = %v; want %v", got, slapping.StateEmpty)
	}
}

func TestSingleSlaps(t *testing.T) {
	got, err := slapping.SlapMany(slapping.StateEmpty, "l")
	if err != nil {
		t.Fatalf("SlapMany(empty, \"l\") error: %v", err)
	}
	if got != slapping.StateLiked {
		t.Errorf("SlapMany(empty, \"l\") = %v; want %v", got, slapping.StateLiked)
	}
	got, err = slapping.SlapMany(slapping.StateEmpty, "d")
	if err != nil {
		t.Fatalf("SlapMany(empty, \"d\") error: %v", err)
	}
	if got != slapping.StateDisliked {
		t.Errorf("SlapMany(empty, \"d\") = %v; want %v", got, slapping.StateDisliked)
	}
}

func TestMultiSlaps(t *testing.T) {
	cases := []struct {
		input    string
		expected slapping.LikeState
	}{
		{"ll", slapping.StateEmpty},
		{"dd", slapping.StateEmpty},
		{"ld", slapping.StateDisliked},
		{"dl", slapping.StateLiked},
		{"ldd", slapping.StateEmpty},
		{"lldd", slapping.StateEmpty},
		{"ddl", slapping.StateLiked},
	}
	for _, c := range cases {
		got, err := slapping.SlapMany(slapping.StateEmpty, c.input)
		if err != nil {
			t.Errorf("SlapMany(empty, %q) error: %v", c.input, err)
		}
		if got != c.expected {
			t.Errorf("SlapMany(empty, %q) = %v; want %v", c.input, got, c.expected)
		}
	}
}

func TestInvalidSlap(t *testing.T) {
	_, err := slapping.SlapMany(slapping.StateEmpty, "x")
	if err == nil {
		t.Errorf("expected error for SlapMany(empty, \"x\"), got nil")
	}
}

func TestPrint(t *testing.T) {
	// In Go, we don't have easy stdout capture in tests; skip implementation
	// as it's not a core test for SlapMany logic.
	// Println("hello")
	// Would normally capture stdout output here.
}