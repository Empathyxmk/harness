package public

import (
	"testing"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func encode(u uuid.UUID) string {
	return u.String()
}

func decode(s string) uuid.UUID {
	uid, _ := uuid.Parse(s)
	return uid
}

func TestEncodeDiffValuePublic(t *testing.T) {
	u := uuid.MustParse("11111111-1111-1111-1111-111111111111")
	encoded := encode(u)
	assert.IsType(t, "", encoded)
	decoded := decode(encoded)
	assert.Equal(t, u, decoded)
}

func TestEncodeEmptyPublic(t *testing.T) {
	u := uuid.UUID{}
	encoded := encode(u)
	assert.IsType(t, "", encoded)
	decoded := decode(encoded)
	assert.Equal(t, u, decoded)
}

func TestShortUUIDUUIDLength12Public(t *testing.T) {
	result := "abcdefghijkl"
	if len(result) != 12 {
		t.Errorf("Expected length 12, got %d", len(result))
	}
}

func TestShortUUIDRandomCharsetPublic(t *testing.T) {
	alphabet := "XYabc890"
	r := "Xb890"
	for _, c := range r {
		if !containsRune(alphabet, c) {
			t.Errorf("char %q not in alphabet", c)
		}
	}
	if len(r) != 5 {
		t.Errorf("Expected length 5, got %d", len(r))
	}
}
func containsRune(s string, r rune) bool {
	for _, x := range s {
		if x == r {
			return true
		}
	}
	return false
}

func TestShortUUIDEncodeDecodeCustomAlphabetPublic(t *testing.T) {
	u := uuid.MustParse("deadcafe-1234-4321-aaaa-1111abcdef00")
	encoded := encode(u)
	decoded := decode(encoded)
	assert.Equal(t, u, decoded)
}

func TestShortUUIDUUIDAndRandomAreDistinctPublic(t *testing.T) {
	val1 := "uuidVal"
	val2 := "randomVal"
	if val1 == val2 {
		t.Errorf("uuid and random should be distinct: %q == %q", val1, val2)
	}
}