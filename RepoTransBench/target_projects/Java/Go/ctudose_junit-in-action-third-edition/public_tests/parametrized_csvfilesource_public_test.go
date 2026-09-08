package public_tests

import (
	"ctudose_junit_in_action_third_edition/testutil"
	"testing"
)

func TestWordsInSentenceCsvFileSourcePublic(t *testing.T) {
	wc := &testutil.WordCounter{}
	// Simulate public CSV file for public test: word_counter_public.csv
	// 1,Hello
	// 5,This is a public test
	// 2,Hello World
	// 4,Public test OpenAI Go
	cases := []struct {
		expected int
		sentence string
	}{
		{1, "Hello"},
		{5, "This is a public test"},
		{2, "Hello World"},
		{4, "Public test OpenAI Go"},
	}
	for i, c := range cases {
		got := wc.CountWords(c.sentence)
		if got != c.expected {
			t.Errorf("row %d: expected %d words for sentence '%s', got %d", i, c.expected, c.sentence, got)
		}
	}
}