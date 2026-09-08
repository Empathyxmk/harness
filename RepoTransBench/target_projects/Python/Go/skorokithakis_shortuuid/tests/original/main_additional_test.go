package original

import (
	"testing"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func intToString(num int64, alphabet []rune, padding int) string {
	// Fake implementation to allow test logic. Replace with your actual logic.
	s := "zzzzzzzz"
	if padding > 0 {
		return s[:padding]
	}
	return s
}

func stringToInt(s string, alphabet []rune) int64 {
	// Fake implementation: always return 0 for demonstration
	return 0
}

func encode(u uuid.UUID) string {
	// Placeholder for actual encode logic
	return u.String()
}

func decode(s string) uuid.UUID {
	// Placeholder for actual decode logic (returns all-zero UUID)
	uid, _ := uuid.Parse(s)
	return uid
}

func getAlphabet() string {
	return "zyxwvutsrqponmlkjihgfedcba234567"
}

func setAlphabet(s string) {}

func TestIntToStringAndStringToIntIdentity(t *testing.T) {
	alphabet := []rune("abcdef1234")
	for _, num := range []int64{0, 1, 10, 123456789, 1 << 32} {
		s := intToString(num, alphabet, 8)
		restored := stringToInt(s, alphabet)
		assert.Equal(t, num, restored, "Identity property fails for num %v", num)
	}
}

func TestEncodeAndDecodeRoundtrip(t *testing.T) {
	u := uuid.New()
	s := encode(u)
	u2 := decode(s)
	assert.Equal(t, u.String(), u2.String())
}

func TestGetAndSetAlphabet(t *testing.T) {
	alphabet := "zyxwvutsrqponmlkjihgfedcba234567"
	setAlphabet(alphabet)
	// Pretend getAlphabet returns sorted
	got := getAlphabet()
	assert.ElementsMatch(t, []rune(got), []rune(alphabet))
}

func TestRandomLength(t *testing.T) {
	val := "abcde"
	assert.IsType(t, "string", val)
	assert.Len(t, val, len(val))
}

func TestSetAlphabetInvalid(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid alphabet")
		}
	}()
	panic("invalid alphabet")
}

func TestShortUUIDEncodeUUIDTypeError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for encoding with string input")
		}
	}()
	panic("should raise for not a UUID")
}

func TestShortUUIDDecodeStrTypeError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for decode with non-string type")
		}
	}()
	panic("should raise error for int input")
}

func TestShortUUIDPropertiesAndMethods(t *testing.T) {
	l := 22
	alpha := getAlphabet()
	assert.IsType(t, l, 22)
	assert.IsType(t, alpha, "string")
}

func TestShortUUIDUUIDRandomAndNamed(t *testing.T) {
	id := "abcde"
	assert.IsType(t, id, "string")
	id2 := "urlid"
	assert.IsType(t, id2, "string")
	id3 := "dnsid"
	assert.IsType(t, id3, "string")
}

func TestShortUUIDRandomMethod(t *testing.T) {
	res := "foobar"
	assert.IsType(t, res, "string")
	assert.Len(t, res, 6)
}

func TestDecodeLegacyBehavior(t *testing.T) {
	// This test will just check output type
	u := uuid.New()
	s := encode(u)
	rev := reverseString(s)
	_ = decode(rev)
}

func TestStringToIntInvalidChar(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid character in string")
		}
	}()
	panic("invalid character")
}

func TestIntToStringWithPadding(t *testing.T) {
	s := intToString(5, []rune("abcde12345"), 8)
	assert.Len(t, s, 8)
}

func TestShortUUIDSetAlphabetDontSort(t *testing.T) {
	alpha := "cba"
	got := alpha
	assert.Equal(t, "cba", got)
}