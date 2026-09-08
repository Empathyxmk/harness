package original

import (
	"testing"
)

type Node struct {
	Value int
	Next  *Node
}

type Key struct {
	fields map[string]int
	c      int
	d      int
}

func NewKey(fields map[string]int, opts ...func(*Key)) *Key {
	k := &Key{fields: fields}
	for _, o := range opts {
		o(k)
	}
	return k
}

type OrderingDirection struct {
	key        func(int) int
	descending bool
}

func NewOrderingDirection(key func(int) int, descending bool) *OrderingDirection {
	return &OrderingDirection{key: key, descending: descending}
}

type RepeatableIterable struct {
	data []int
	cur  int
}

func NewRepeatableIterable(data []int) *RepeatableIterable {
	return &RepeatableIterable{data: data, cur: 0}
}

func (it *RepeatableIterable) Len() int {
	return len(it.data)
}

func (it *RepeatableIterable) Reset() {
	it.cur = 0
}

func (it *RepeatableIterable) Next() (int, bool) {
	if it.cur+1 < len(it.data) {
		it.cur++
		return it.data[it.cur], true
	}
	return 0, false
}

func (it *RepeatableIterable) Value() int {
	if len(it.data) > 0 {
		return it.data[it.cur]
	}
	return 0
}

func (it *RepeatableIterable) Iter() []int {
	return it.data
}

func (it *RepeatableIterable) Reversed() []int {
	n := len(it.data)
	out := make([]int, n)
	for i := n - 1; i >= 0; i-- {
		out[n-1-i] = it.data[i]
	}
	return out
}

func TestNodeNextValue(t *testing.T) {
	n1 := &Node{Value: 1}
	n2 := &Node{Value: 2}
	n1.Next = n2
	if n1.Value != 1 {
		t.Errorf("Expected n1.Value == 1 got %d", n1.Value)
	}
	if n1.Next.Value != 2 {
		t.Errorf("Expected n1.Next.Value == 2 got %d", n1.Next.Value)
	}
}

func TestKeyRepr(t *testing.T) {
	k := NewKey(map[string]int{"a": 1, "b": 2})
	r := k.fields
	if r["a"] != 1 || r["b"] != 2 {
		t.Errorf("Expected key fields 'a' and 'b' with correct values")
	}
	k2 := NewKey(nil, func(k *Key) { k.c = 3; k.d = 4 })
	if k2.c != 3 || k2.d != 4 {
		t.Errorf("Expected c == 3 and d == 4, got c=%d d=%d", k2.c, k2.d)
	}
}

func TestOrderingDirection(t *testing.T) {
	od := NewOrderingDirection(func(x int) int { return -x }, true)
	if !od.descending {
		t.Errorf("Expected descending == true")
	}
	if od.key(3) != -3 {
		t.Errorf("Expected key(3) == -3 got %d", od.key(3))
	}
}

func TestRepeatableIterableBasics(t *testing.T) {
	data := []int{1, 2, 3}
	rit := NewRepeatableIterable(data)
	out := rit.Iter()
	for i, v := range out {
		if v != data[i] {
			t.Errorf("At idx %d, expected %d got %d", i, data[i], v)
		}
	}
	if rit.Len() != 3 {
		t.Errorf("Expected length 3 got %d", rit.Len())
	}
}

func TestRepeatableIterableReversed(t *testing.T) {
	data := []int{1, 2, 3}
	rit := NewRepeatableIterable(data)
	out := rit.Reversed()
	want := []int{3, 2, 1}
	for i, v := range out {
		if v != want[i] {
			t.Errorf("Reversed: At idx %d, expected %d got %d", i, want[i], v)
		}
	}
}

func TestRepeatableIterableIterAndNext(t *testing.T) {
	data := []int{10, 20, 30}
	rit := NewRepeatableIterable(data)
	it := rit
	result := it.Value()
	if result != 10 {
		t.Errorf("Expected first value 10 got %d", result)
	}
	for i := 0; i < rit.Len(); i++ {
		_, _ = it.Next()
	}
	rit.Reset()
	for i, v := range rit.Iter() {
		if v != data[i] {
			t.Errorf("Reset iterate: At %d expected %d got %d", i, data[i], v)
		}
	}
}

func TestRepeatableIterableTypeError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for non-slice input")
		}
	}()
	NewRepeatableIterable(nil)
}