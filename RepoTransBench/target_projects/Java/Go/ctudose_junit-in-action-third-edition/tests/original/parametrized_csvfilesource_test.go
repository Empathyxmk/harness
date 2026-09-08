package original

import (
	"ctudose_junit_in_action_third_edition/testutil"
	"testing"
)

func TestWordsInSentenceCsvFileSource(t *testing.T) {
	wc := &testutil.WordCounter{}
	// Simulate CSV file reading (word_counter.csv):
	// 2,Unit testing
	// 3,JUnit in Action
	// 4,Write solid Java code
	type row struct {
		expected int
		sentence string
	}
	cases := []row{
		{2, "Unit testing"},
		{3, "JUnit in Action"},
		{4, "Write solid Java code"},
	}
	for i, c := range cases {
		got := wc.CountWords(c.sentence)
		if got != c.expected {
			t.Errorf("row %d: expected %d words for sentence '%s', got %d", i, c.expected, c.sentence, got)
		}
	}
}