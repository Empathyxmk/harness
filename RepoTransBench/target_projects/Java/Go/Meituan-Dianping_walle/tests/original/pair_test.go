package original

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

func TestPair_OfGetters(t *testing.T) {
	pair := Of("hello", 42)
	if pair.GetFirst() != "hello" {
		t.Errorf("expected 'hello', got %v", pair.GetFirst())
	}
	if pair.GetSecond() != 42 {
		t.Errorf("expected 42, got %v", pair.GetSecond())
	}
}

func TestPair_EqualsHashCode_SameObject(t *testing.T) {
	pair := Of("foo", 123)
	if !pair.Equals(pair) {
		t.Errorf("pair.Equals(pair) should be true")
	}
	if pair.HashCode() != pair.HashCode() {
		t.Errorf("hash codes should match")
	}
}

func TestPair_EqualsHashCode_EqualPairs(t *testing.T) {
	pair1 := Of("a", 1)
	pair2 := Of("a", 1)
	if !pair1.Equals(pair2) || !pair2.Equals(pair1) {
		t.Errorf("pairs should be equal")
	}
	if pair1.HashCode() != pair2.HashCode() {
		t.Errorf("hash codes should be equal")
	}
}

func TestPair_Equals_NotEqualByFirst(t *testing.T) {
	pair1 := Of("a", 1)
	pair2 := Of("b", 1)
	if pair1.Equals(pair2) {
		t.Errorf("pairs with different first must not be equal")
	}
}

func TestPair_Equals_NotEqualBySecond(t *testing.T) {
	pair1 := Of("a", 1)
	pair2 := Of("a", 2)
	if pair1.Equals(pair2) {
		t.Errorf("pairs with different second must not be equal")
	}
}

func TestPair_Equals_NullObject(t *testing.T) {
	pair := Of("x", 10)
	if pair.Equals(nil) {
		t.Errorf("pair.Equals(nil) should be false")
	}
}

func TestPair_Equals_DifferentClass(t *testing.T) {
	pair := Of("x", 10)
	// Cannot compare with string in Go, always false
	if reflect.DeepEqual(pair, "not a pair") {
		t.Errorf("pair is not equal to a string")
	}
}

func TestPair_Equals_NullFields(t *testing.T) {
	p1 := Of(nil, nil)
	p2 := Of(nil, nil)
	if !p1.Equals(p2) {
		t.Errorf("pairs with both fields nil must be equal")
	}
	if p1.HashCode() != p2.HashCode() {
		t.Errorf("hash codes must be equal for nil fields")
	}
}

func TestPair_Equals_NullFirstDifferentSecond(t *testing.T) {
	p1 := Of(nil, 10)
	p2 := Of(nil, 11)
	if p1.Equals(p2) {
		t.Errorf("should not be equal if second different (first nil)")
	}
}

func TestPair_Equals_DifferentFirstNullSecond(t *testing.T) {
	p1 := Of("x", nil)
	p2 := Of("y", nil)
	if p1.Equals(p2) {
		t.Errorf("should not be equal if first differ and second is nil")
	}
}

func TestPair_Equals_NullFirstNonNullOther(t *testing.T) {
	p1 := Of(nil, 1)
	p2 := Of("z", 1)
	if p1.Equals(p2) {
		t.Errorf("should not be equal if first nil and other not nil")
	}
}

func TestPair_Equals_NonNullFirstNullOther(t *testing.T) {
	p1 := Of("z", 1)
	p2 := Of(nil, 1)
	if p1.Equals(p2) {
		t.Errorf("should not be equal if first not nil and other is nil")
	}
}