package original

import (
	"ctudose_junit_in_action_third_edition/testutil"
	"testing"
)

func TestWordsInSentenceValueSource(t *testing.T) {
	wc := &testutil.WordCounter{}
	cases := []string{
		"Check three parameters",
		"JUnit in Action",
	}
	for _, sentence := range cases {
		got := wc.CountWords(sentence)
		if got != 3 {
			t.Errorf("ValueSource: sentence '%s': expected 3 words, got %d", sentence, got)
		}
	}
}