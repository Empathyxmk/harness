package original

import (
	"ctudose_junit_in_action_third_edition/testutil"
	"testing"
)

func TestWordsInSentenceCsvSource(t *testing.T) {
	wc := &testutil.WordCounter{}
	cases := []struct {
		expected int
		sentence string
	}{
		{2, "Unit testing"},
		{3, "JUnit in Action"},
		{4, "Write solid Java code"},
	}
	for i, c := range cases {
		got := wc.CountWords(c.sentence)
		if got != c.expected {
			t.Errorf("case %d: expected %d words for sentence '%s', got %d", i, c.expected, c.sentence, got)
		}
	}
}