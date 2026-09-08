package original

import (
	"ctudose_junit_in_action_third_edition/testutil"
	"testing"
)

type Sentences int

const (
	JUNIT_IN_ACTION Sentences = iota
	SOME_PARAMETERS
	THREE_PARAMETERS
)

func (s Sentences) Value() string {
	switch s {
	case JUNIT_IN_ACTION:
		return "JUnit in Action"
	case SOME_PARAMETERS:
		return "Check some parameters"
	case THREE_PARAMETERS:
		return "Check three parameters"
	default:
		return ""
	}
}

func TestWordsInSentenceEnumSource_All(t *testing.T) {
	wc := &testutil.WordCounter{}
	for _, s := range []Sentences{JUNIT_IN_ACTION, SOME_PARAMETERS, THREE_PARAMETERS} {
		got := wc.CountWords(s.Value())
		if got != 3 {
			t.Errorf("Enum Value '%s': expected 3 words, got %d", s.Value(), got)
		}
	}
}

func TestWordsInSentenceEnumSource_Selected(t *testing.T) {
	wc := &testutil.WordCounter{}
	for _, s := range []Sentences{JUNIT_IN_ACTION, THREE_PARAMETERS} {
		got := wc.CountWords(s.Value())
		if got != 3 {
			t.Errorf("Enum Selected '%s': expected 3 words, got %d", s.Value(), got)
		}
	}
}

func TestWordsInSentenceEnumSource_Exclude(t *testing.T) {
	wc := &testutil.WordCounter{}
	for _, s := range []Sentences{JUNIT_IN_ACTION, SOME_PARAMETERS} {
		got := wc.CountWords(s.Value())
		if got != 3 {
			t.Errorf("Enum Excluded '%s': expected 3 words, got %d", s.Value(), got)
		}
	}
}