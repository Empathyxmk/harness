package public_tests

import (
	"reflect"
	"testing"
)

type Pair struct {
	First  interface{}
	Second interface{}
}

func Of(first, second interface{}) *Pair {
	return &Pair{First: first, Second: second}
}

func (p *Pair) GetFirst() interface{} {
	return p.First
}

func (p *Pair) GetSecond() interface{} {
	return p.Second
}

func (p *Pair) Equals(other *Pair) bool {
	if other == nil {
		return false
	}
	return reflect.DeepEqual(p.First, other.First) && reflect.DeepEqual(p.Second, other.Second)
}

func (p *Pair) HashCode() int {
	// Very basic hash.
	h := 0
	if p.First != nil {
		h += reflect.TypeOf(p.First).Size()
	}
	if p.Second != nil {
		h += reflect.TypeOf(p.Second).Size()
	}
	return int(h)
}

func TestPairPublic_OfAndGetters_public(t *testing.T) {
	pair := Of(12345, "hello")
	if pair.GetFirst() != 12345 {
		t.Errorf("expected 12345, got %v", pair.GetFirst())
	}
	if pair.GetSecond() != "hello" {
		t.Errorf("expected 'hello', got %v", pair.GetSecond())
	}

	pair2 := Of(3.14, 2.71)
	if pair2.GetFirst() != 3.14 {
		t.Errorf("expected 3.14, got %v", pair2.GetFirst())
	}
	if pair2.GetSecond() != 2.71 {
		t.Errorf("expected 2.71, got %v", pair2.GetSecond())
	}
}

func TestPairPublic_EqualsAndHashCode_public(t *testing.T) {
	a := Of("A", "B")
	b := Of("A", "B")
	if !a.Equals(b) {
		t.Errorf("expected pairs to be equal")
	}
	if a.HashCode() != b.HashCode() {
		t.Errorf("expected hash codes to be equal")
	}

	c := Of("A", "C")
	if a.Equals(c) {
		t.Errorf("expected not equal")
	}

	d := Of(nil, "B")
	e := Of(nil, "B")
	if !d.Equals(e) {
		t.Errorf("expected pairs to be equal")
	}
	if d.HashCode() != e.HashCode() {
		t.Errorf("expected hash codes to be equal for nil firsts")
	}
}