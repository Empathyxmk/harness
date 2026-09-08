package public_tests

import (
	"regexp"
	"testing"
	"strings"

	"seatgeek_fuzzywuzzy/fuzzywuzzy"
	"github.com/stretchr/testify/assert"
)

func TestReplaceNonLettersNonNumbersWithWhitespacePublic(t *testing.T) {
	stringsToTest := []string{
		"san francisco giants@los angeles dodgers",
		"São Tomé",
		"Big City ^^^^^ Giants $$$",
		"¿Cómo estás?",
	}
	re := regexp.MustCompile(`(?ui)[\W]`)
	for _, s := range stringsToTest {
		proc := fuzzywuzzy.ReplaceNonLettersNonNumbersWithWhitespace(s)
		for _, m := range re.FindAllString(proc, -1) {
			assert.Equal(t, " ", m)
		}
	}
}

func TestDontCondenseWhitespacePublic(t *testing.T) {
	s1 := "san francisco giants @ los angeles dodgers"
	s2 := "san francisco giants los angeles dodgers"
	p1 := fuzzywuzzy.ReplaceNonLettersNonNumbersWithWhitespace(s1)
	p2 := fuzzywuzzy.ReplaceNonLettersNonNumbersWithWhitespace(s2)
	assert.NotEqual(t, p1, p2)
}

// Add further utility and ratio tests, adapting logic from the Python public version above for Go.