package tests

import (
	"strings"
	"testing"

	"seatgeek_fuzzywuzzy/fuzzywuzzy"
	"github.com/stretchr/testify/assert"
)

func TestValidateStringStrAndNone(t *testing.T) {
	assert.True(t, fuzzywuzzy.ValidateString("abc"))
	assert.False(t, fuzzywuzzy.ValidateString(nil))
	assert.False(t, fuzzywuzzy.ValidateString(123))
	assert.False(t, fuzzywuzzy.ValidateString([]string{}))
}

func TestMakeTypeConsistentStr(t *testing.T) {
	s1, s2 := fuzzywuzzy.MakeTypeConsistent("abc", "def")
	_, ok1 := s1.(string)
	_, ok2 := s2.(string)
	assert.True(t, ok1)
	assert.True(t, ok2)
}

func TestIntrBehavior(t *testing.T) {
	assert.Equal(t, 4, fuzzywuzzy.Intr(3.7))
	assert.Equal(t, 3, fuzzywuzzy.Intr(3.3))

	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic when passing string to Intr")
		}
	}()
	fuzzywuzzy.Intr("42")
}

func TestAsciidammitAscii(t *testing.T) {
	assert.Equal(t, "hello", fuzzywuzzy.Asciidammit("hello"))
}

func TestAsciionlyBasic(t *testing.T) {
	assert.Equal(t, "TeSt", fuzzywuzzy.Asciionly("TeSt"))
	assert.Equal(t, "abc✓", fuzzywuzzy.Asciionly("abc✓"))
}

func TestFullProcessOptions(t *testing.T) {
	s := " This is Ünicode!   "
	processed := fuzzywuzzy.FullProcess(s, false)
	assert.Contains(t, strings.ToLower(processed), "ünicod")
	processedAscii := fuzzywuzzy.FullProcess(s, true)
	assert.Contains(t, strings.ToLower(processedAscii), "nicode")
	assert.Equal(t, "", fuzzywuzzy.FullProcess("", true))
	assert.Equal(t, "", fuzzywuzzy.FullProcess("   ", true))
}

func TestStripAndCase(t *testing.T) {
	s := "  hello\n"
	assert.Equal(t, strings.TrimSpace(s), fuzzywuzzy.Strip(s))
	assert.Equal(t, strings.ToLower(s), fuzzywuzzy.ToLowerCase(s))
	assert.Equal(t, strings.ToUpper(s), fuzzywuzzy.ToUpperCase(s))
}