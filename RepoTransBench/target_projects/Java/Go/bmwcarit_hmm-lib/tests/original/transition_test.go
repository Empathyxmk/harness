package tests

import (
	"testing"
	"strconv"
)

// Uses Transition[string] type defined in testutil.go

func TestTransition_EqualsAndHashCode(t *testing.T) {
	a, b, c := "A", "B", "C"
	t1 := NewTransition(&a, &b)
	t2 := NewTransition(&a, &b)
	t3 := NewTransition(&b, &a)
	t4 := NewTransition(&a, &c)

	if !t1.Equal(t2) {
		t.Errorf("Transitions %v and %v should be equal", t1, t2)
	}
	if t1.Hash() != t2.Hash() {
		t.Errorf("Hash codes %v and %v should be equal", t1.Hash(), t2.Hash())
	}
	if t1.Equal(t3) {
		t.Errorf("%v and %v should not be equal", t1, t3)
	}
	if t1.Hash() == t3.Hash() {
		t.Errorf("Hash codes for %v and %v should not be equal", t1, t3)
	}
	if t1.Equal(t4) {
		t.Errorf("%v and %v should not be equal", t1, t4)
	}
}

func TestTransition_EqualsWithNulls(t *testing.T) {
	b := "B"
	a := "A"
	t1 := NewTransition[string](nil, &b)
	t2 := NewTransition[string](nil, &b)
	t3 := NewTransition[string](&a, nil)
	t4 := NewTransition[string](nil, nil)
	t5 := NewTransition[string](nil, nil)

	if !t1.Equal(t2) {
		t.Errorf("t1 and t2 should be equal")
	}
	if !t4.Equal(t5) {
		t.Errorf("t4 and t5 should be equal")
	}
	if t1.Equal(t3) {
		t.Errorf("t1 and t3 should not be equal")
	}
}

func TestTransition_ToString(t *testing.T) {
	a, b := "A", "B"
	t1 := NewTransition(&a, &b)
	str := t1.String()
	if str == "" || (str != "" && !(contains(str, "fromCandidate=A") && contains(str, "toCandidate=B"))) {
		t.Errorf("Transition.ToString doesn't contain correct fields: %s", str)
	}
}

func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s == sub || (len(sub) > 0 && s != "" && (s == sub || contains(s[1:], sub))))
}

func TestTransition_NotEqualsOtherTypesAndNull(t *testing.T) {
	a, b := "A", "B"
	t1 := NewTransition(&a, &b)
	if t1 == (Transition[string]{}) {
		t.Errorf("Transition should not be equal to zero-value struct")
	}
	if t1.Equal(Transition[string]{}) {
		t.Errorf("t1 shouldn't equal zero-value transition")
	}
	notAString := "not_a_transition"
	hash := strconv.Itoa(42)
	if t1.Hash() == hash {
		t.Errorf("Hash shouldn't match a random string representation")
	}
}