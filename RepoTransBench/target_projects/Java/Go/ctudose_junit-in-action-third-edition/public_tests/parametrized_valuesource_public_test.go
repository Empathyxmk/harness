package public_tests

import (
	"ctudose_junit_in_action_third_edition/testutil"
	"testing"
)

func TestWordsInSentenceValueSourcePublic(t *testing.T) {
	wc := &testutil.WordCounter{}
	cases := []string{
		"New public test",
		"OpenAI model",
	}
	for _, sentence := range cases {
		got := wc.CountWords(sentence)
		if got != 3 {
			t.Errorf("Public ValueSource: expected 3 words for '%s', got %d", sentence, got)
		}
	}
}