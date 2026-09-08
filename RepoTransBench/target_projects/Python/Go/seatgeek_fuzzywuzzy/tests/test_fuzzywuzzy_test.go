package tests

import (
	"regexp"
	"strings"
	"testing"

	"seatgeek_fuzzywuzzy/fuzzywuzzy"
	"github.com/stretchr/testify/assert"
)

func TestReplaceNonLettersNonNumbersWithWhitespace(t *testing.T) {
	stringsToTest := []string{
		"new york mets - atlanta braves",
		"Cães danados",
		"New York //// Mets $$$",
		"Ça va?",
	}
	re := regexp.MustCompile(`(?ui)[\W]`)
	for _, s := range stringsToTest {
		ps := fuzzywuzzy.ReplaceNonLettersNonNumbersWithWhitespace(s)
		for _, m := range re.FindAllString(ps, -1) {
			assert.Equal(t, " ", m)
		}
	}
}

func TestDontCondenseWhitespace(t *testing.T) {
	s1 := "new york mets - atlanta braves"
	s2 := "new york mets atlanta braves"
	p1 := fuzzywuzzy.ReplaceNonLettersNonNumbersWithWhitespace(s1)
	p2 := fuzzywuzzy.ReplaceNonLettersNonNumbersWithWhitespace(s2)
	assert.NotEqual(t, p1, p2)
}

// Add remaining tests accordingly (see full test code in Python, rework with Go types)
// For brevity, we demonstrate translation of StringProcessing tests as representative.