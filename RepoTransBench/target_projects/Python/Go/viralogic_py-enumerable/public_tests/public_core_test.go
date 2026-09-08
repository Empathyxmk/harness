package public_tests

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

func TestPublicNodeNextValue(t *testing.T) {
	node1 := &Node{Value: 99}
	node2 := &Node{Value: 101}
	node1.Next = node2
	if node1.Next != node2 {
		t.Errorf("Expected node1.Next == node2")
	}
}

func TestPublicKeyRepr(t *testing.T) {
	k := NewKey(map[string]int{"foo": 42, "bar": 13})
	fields := k.fields
	if fields["foo"] != 42 || fields["bar"] != 13 {
		t.Errorf("Key fields missing or mismatch")
	}
}

func TestPublicOrderingDirection(t *testing.T) {
	od := NewOrderingDirection(func(x int) int { return -x }, false)
	res := od.key(5)
	if res != -5 {
		t.Errorf("Expected key(5) == -5 got %d", res)
	}
}

func TestPublicRepeatableIterableBasics(t *testing.T) {
	r := NewRepeatableIterable([]int{10, 11, 12})
	out := r.Iter()
	want := []int{10, 11, 12}
	for i, v := range out {
		if v != want[i] {
			t.Errorf("At %d, got %d want %d", i, v, want[i])
		}
	}
	if r.Len() != 3 {
		t.Errorf("Expected len==3 got %d", r.Len())
	}
}

func TestPublicRepeatableIterableReversed(t *testing.T) {
	r := NewRepeatableIterable([]int{1, 2, 3})
	want := []int{3, 2, 1}
	got := r.Reversed()
	for i, v := range got {
		if v != want[i] {
			t.Errorf("Reversed: At idx %d, got %d want %d", i, v, want[i])
		}
	}
}

func TestPublicRepeatableIterableIterAndNext(t *testing.T) {
	r := NewRepeatableIterable([]int{41, 18})
	it := r
	first := it.Value()
	if first != 41 {
		t.Errorf("First value got %d want 41", first)
	}
	n, ok := it.Next()
	if !ok || n != 18 {
		t.Errorf("Second value got %d want 18", n)
	}
}

func TestPublicRepeatableIterableTypeError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for non-slice input")
		}
	}()
	NewRepeatableIterable(nil)
}