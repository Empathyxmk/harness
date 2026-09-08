package public_tests

import (
	"strconv"
	"testing"

	"bmwcarit_hmm_lib/tests"
)

func TestTransition_EqualsAndHashCodePublic(t *testing.T) {
	x, y, z := "X", "Y", "Z"
	t1 := tests.NewTransition(&x, &y)
	t2 := tests.NewTransition(&x, &y)
	t3 := tests.NewTransition(&y, &z)
	t4 := tests.NewTransition(&x, &z)

	if !t1.Equal(t2) {
		t.Errorf("Transitions %v and %v should be equal", t1, t2)
	}
	if t1.Hash() != t2.Hash() {
		t.Errorf("Hash codes for %v and %v should be equal", t1, t2)
	}
	if t1.Equal(t3) {
		t.Errorf("t1 and t3 should not be equal")
	}
	if t1.Hash() == t3.Hash() {
		t.Errorf("t1 and t3 should not have the same hash")
	}
	if t1.Equal(t4) {
		t.Errorf("t1 and t4 should not be equal")
	}
}

func TestTransition_EqualsWithNullsPublic(t *testing.T) {
	y := "Y"
	x := "X"
	t1 := tests.NewTransition[string](nil, &y)
	t2 := tests.NewTransition[string](nil, &y)
	t3 := tests.NewTransition[string](&x, nil)
	t4 := tests.NewTransition[string](nil, nil)
	t5 := tests.NewTransition[string](nil, nil)

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

func TestTransition_ToStringPublic(t *testing.T) {
	q, p := "Q", "P"
	t1 := tests.NewTransition(&q, &p)
	str := t1.String()
	if str == "" || (str != "" && !(contains(str, "fromCandidate=Q") && contains(str, "toCandidate=P"))) {
		t.Errorf("Transition.ToString doesn't contain correct fields: %s", str)
	}
}

func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s == sub || (len(sub) > 0 && s != "" && (s == sub || contains(s[1:], sub))))
}

func TestTransition_NotEqualsOtherTypesAndNullPublic(t *testing.T) {
	i, j := "I", "J"
	t1 := tests.NewTransition(&i, &j)
	if t1 == (tests.Transition[string]{}) {
		t.Errorf("Transition should not be equal to zero-value struct")
	}
	if t1.Equal(tests.Transition[string]{}) {
		t.Errorf("t1 shouldn't equal zero-value transition")
	}
	intint := 12345
	if t1.Hash() == strconv.Itoa(intint) {
		t.Errorf("Hash shouldn't match a random string representation")
	}
}