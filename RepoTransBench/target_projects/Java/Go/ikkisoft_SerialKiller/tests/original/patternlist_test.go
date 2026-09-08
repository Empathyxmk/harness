package original

import (
	"regexp"
	"testing"
)

type PatternList struct {
	patterns []*regexp.Regexp
}

func NewPatternList(patterns ...string) (*PatternList, error) {
	if patterns == nil {
		return nil, &NullPointerError{"nil pattern slice"}
	}
	res := &PatternList{}
	for _, p := range patterns {
		r, err := regexp.Compile(p)
		if err != nil {
			return nil, err
		}
		res.patterns = append(res.patterns, r)
	}
	return res, nil
}

func (pl *PatternList) Iterator() []*regexp.Regexp {
	return pl.patterns
}

type NullPointerError struct{ msg string }
func (e *NullPointerError) Error() string { return e.msg }

// ------ Tests --------

func TestCreateNullPatternList(t *testing.T) {
	_, err := NewPatternList(nil...)
	if err == nil {
		t.Fatalf("expected error for nil input, got none")
	}
	if _, ok := err.(*NullPointerError); !ok {
		t.Fatalf("expected NullPointerError, got %T", err)
	}
}

func TestCreateBadPatternPatternList(t *testing.T) {
	_, err := NewPatternList("(")
	if err == nil {
		t.Fatalf("expected error for bad regex, got none")
	}
}

func TestCreateEmptyPatternList(t *testing.T) {
	list, err := NewPatternList()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(list.Iterator()) != 0 {
		t.Errorf("expected empty pattern list")
	}
}

func TestCreateSinglePatternList(t *testing.T) {
	list, err := NewPatternList("a")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(list.Iterator()) != 1 {
		t.Fatalf("expected 1 pattern, got %d", len(list.Iterator()))
	}
	p := list.Iterator()[0]
	if p == nil || p.String() != "a" {
		t.Errorf("expected pattern 'a', got %v", p)
	}
}

func TestCreateSequencePatternList(t *testing.T) {
	patterns := []string{"a", "b", "c"}
	list, err := NewPatternList(patterns...)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	for i, got := range list.Iterator() {
		if got == nil || got.String() != patterns[i] {
			t.Errorf("at %d expected '%s', got '%v'", i, patterns[i], got)
		}
	}
	if len(list.Iterator()) != 3 {
		t.Errorf("expected 3 patterns")
	}
}

func TestCreateSafeArgsPatternList(t *testing.T) {
	patterns := []string{"1", "2"}
	list, err := NewPatternList(patterns...)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	patterns[1] = "three" // should not modify list
	index := 0
	for _, got := range list.Iterator() {
		exp := string('1' + index)
		if got.String() != exp {
			t.Errorf("expected %q, got %q", exp, got.String())
		}
		index++
	}
	if index != 2 {
		t.Errorf("expected 2 patterns")
	}
}