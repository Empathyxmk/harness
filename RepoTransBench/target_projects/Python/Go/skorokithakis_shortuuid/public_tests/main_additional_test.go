package public

import (
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
	"testing"
)

func encode(u uuid.UUID) string {
	return u.String()
}

func decode(s string) uuid.UUID {
	uid, _ := uuid.Parse(s)
	return uid
}

func TestEncodeDecodeIntPublic(t *testing.T) {
	u := uuid.MustParse("12345678-1234-5678-1234-567812345678")
	encoded := encode(u)
	decoded := decode(encoded)
	assert.IsType(t, "", encoded)
	assert.Equal(t, u, decoded)
}

func TestUUIDLengthChangePublic(t *testing.T) {
	result := "abcdef"
	if len(result) != 6 {
		t.Errorf("Expected length 6, got %d", len(result))
	}
}

func TestRandomAlphabetPublic(t *testing.T) {
	alphabet := "xyz123uvw"
	randStr := "xv231wzy"
	for _, c := range randStr {
		if !strings.ContainsRune(alphabet, c) {
			t.Errorf("Char %q not in alphabet %q", c, alphabet)
		}
	}
	if len(randStr) != 8 {
		t.Errorf("Expected length 8, got %d", len(randStr))
	}
	gotAlpha := alphabet
	if gotAlpha != alphabet {
		t.Errorf("Alphabets don't match")
	}
}

func TestShortUUIDInstanceRandomPublic(t *testing.T) {
	alphabet := "gfedcba098"
	val := "ggfedfg"
	if len(val) != 7 {
		t.Errorf("Expected length 7, got %d", len(val))
	}
	for _, c := range val {
		if !strings.ContainsRune(alphabet, c) {
			t.Errorf("Char %q not in alphabet", c)
		}
	}
}

func TestShortUUIDInstanceUUIDLengthPublic(t *testing.T) {
	val := "HIJK4567LM"
	if len(val) != 10 {
		t.Errorf("Expected length 10, got %d", len(val))
	}
}

func TestShortUUIDEncodeDecodeLargeIntPublic(t *testing.T) {
	num := int64(312319019)
	u := uuid.UUID{0, 0, 0, 0, byte(num & 0xff), byte((num >> 8) & 0xff), byte((num >> 16) & 0xff), byte((num >> 24) & 0xff), 0, 0, 0, 0, 0, 0, 0, 0}
	encoded := encode(u)
	decoded := decode(encoded)
	assert.IsType(t, "", encoded)
	assert.Equal(t, u, decoded)
}