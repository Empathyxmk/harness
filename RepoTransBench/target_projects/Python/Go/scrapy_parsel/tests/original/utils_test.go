package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestShorten(t *testing.T) {
	tests := []struct{
		width int
		expected interface{} // string or error
	}{
		{-1, "error"},
		{0, ""},
		{1, "."},
		{2, ".."},
		{3, "..."},
		{4, "f..."},
		{5, "fo..."},
		{6, "foobar"},
		{7, "foobar"},
	}
	for _, test := range tests {
		val, err := parsel.Shorten("foobar", test.width)
		if test.expected == "error" {
			assert.Error(t, err)
		} else {
			assert.NoError(t, err)
			assert.Equal(t, test.expected, val)
		}
	}
}

func TestExtractRegex(t *testing.T) {
	type testcase struct {
		regex string
		text  string
		replaceEntities bool
		expected []string
	}
	tests := []testcase{
		{regex: `(?P<month>\w+)\s*(?P<day>\d+)\s*\,?\s*(?P<year>\d+)`, text: "October  25, 2019", replaceEntities: true, expected: []string{"October", "25", "2019"}},
		{regex: `(?P<month>\w+)\s*(?P<day>\d+)\s*\,?\s*(?P<year>\d+)`, text: "October  25 2019", replaceEntities: true, expected: []string{"October", "25", "2019"}},
		{regex: `(?P<extract>\w+)\s*(?P<day>\d+)\s*\,?\s*(?P<year>\d+)`, text: "October  25 2019", replaceEntities: true, expected: []string{"October"}},
		{regex: `\w+\s*\d+\s*\,?\s*\d+`, text: "October  25 2019", replaceEntities: true, expected: []string{"October  25 2019"}},
		{regex: `^.*$`, text: `&quot;sometext&quot; &amp; &quot;moretext&quot;`, replaceEntities: true, expected: []string{`"sometext" &amp; "moretext"`}},
		{regex: `^.*$`, text: `&quot;sometext&quot; &amp; &quot;moretext&quot;`, replaceEntities: false, expected: []string{`&quot;sometext&quot; &amp; &quot;moretext&quot;`}},
	}
	for _, test := range tests {
		val, err := parsel.ExtractRegex(test.regex, test.text, test.replaceEntities)
		assert.NoError(t, err)
		assert.Equal(t, test.expected, val)
	}
}