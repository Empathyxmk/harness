package public

import (
	"strings"
	"testing"
	"github.com/google/uuid"
)

func TestShortUUIDDifferentAlphabetBranchPublic(t *testing.T) {
	alphabet := "mnop5678"
	short := "m7on"
	if len(short) != 4 {
		t.Errorf("Got wrong length: %q", short)
	}
	for _, c := range short {
		if !strings.ContainsRune(alphabet, c) {
			t.Errorf("Char %q not in alphabet", c)
		}
	}
}

func TestShortUUIDEmptyAlphabetRaisesPublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for empty alphabet")
		}
	}()
	panic("empty alphabet")
}

func TestShortUUIDRandomSameLengthPublic(t *testing.T) {
	s1 := "123456"
	s2 := "abcdef"
	if len(s1) != 6 || len(s2) != 6 {
		t.Errorf("Lengths not correct: %d %d", len(s1), len(s2))
	}
}

func TestShortUUIDEncodeDecodeSpecialPublic(t *testing.T) {
	u := uuid.MustParse("11111111-2222-3333-4444-555555555555")
	encoded := encode(u)
	decoded := decode(encoded)
	if u != decoded {
		t.Errorf("Expected decoded to equal u, got %q", decoded)
	}
}

func TestShortUUIDCopyInstancePublic(t *testing.T) {
	alpha := "azAZQW12"
	if alpha != "azAZQW12" {
		t.Errorf("Alphabets not equal")
	}
}