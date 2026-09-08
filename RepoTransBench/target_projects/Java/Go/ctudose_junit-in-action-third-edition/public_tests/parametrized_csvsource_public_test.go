package public_tests

import (
	"ctudose_junit_in_action_third_edition/testutil"
	"testing"
)

func TestWordsInSentenceCsvSourcePublic(t *testing.T) {
	wc := &testutil.WordCounter{}
	cases := []struct {
		expected int
		sentence string
	}{
		{1, "Hello"},
		{5, "This is a public test"},
		{2, "Hello World"},
	}
	for i, c := range cases {
		got := wc.CountWords(c.sentence)
		if got != c.expected {
			t.Errorf("case %d: expected %d words for sentence '%s', got %d", i, c.expected, c.sentence, got)
		}
	}
}