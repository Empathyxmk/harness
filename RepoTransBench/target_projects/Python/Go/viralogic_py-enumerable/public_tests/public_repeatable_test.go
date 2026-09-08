package public_tests

import (
	"testing"
)

type RepeatableIterable struct {
	data []int
	cur  int
}

func NewRepeatableIterable(data []int) *RepeatableIterable {
	return &RepeatableIterable{data: data, cur: 0}
}

func (ri *RepeatableIterable) Iter() []int {
	return ri.data
}

func (ri *RepeatableIterable) Sum() int {
	total := 0
	for _, v := range ri.data {
		total += v
	}
	return total
}

func TestPublicRepeatableCommonUsage(t *testing.T) {
	items := NewRepeatableIterable([]int{10, 20, 30})
	got := items.Iter()
	want := []int{10, 20, 30}
	for i, v := range got {
		if v != want[i] {
			t.Errorf("Iter: At %d got %d want %d", i, v, want[i])
		}
	}
	got2 := items.Iter()
	for i, v := range got2 {
		if v != want[i] {
			t.Errorf("2nd Iter: At %d got %d want %d", i, v, want[i])
		}
	}
	sum := items.Sum()
	if sum != 60 {
		t.Errorf("sum got %d want 60", sum)
	}
	any := false
	for _, v := range items.Iter() {
		if v > 25 {
			any = true
		}
	}
	if !any {
		t.Error("Expected at least one v > 25 in items")
	}
	all := true
	for _, v := range items.Iter() {
		if v >= 40 {
			all = false
		}
	}
	if !all {
		t.Error("Expected all v < 40 in items")
	}
}