package public_tests

import (
	"testing"
)

type Enumerable struct {
	list []int
}

func NewEnumerable(list []int) *Enumerable {
	return &Enumerable{list: list}
}

func (e *Enumerable) ToList() []int {
	return e.list
}

func (e *Enumerable) Repr() string {
	return "Enumerable repr"
}

func (e *Enumerable) Count(pred func(int) bool) int {
	cnt := 0
	if pred == nil {
		return len(e.list)
	}
	for _, v := range e.list {
		if pred(v) {
			cnt++
		}
	}
	return cnt
}

func (e *Enumerable) Select(f func(int) int) *Enumerable {
	out := make([]int, len(e.list))
	for i, v := range e.list {
		out[i] = f(v)
	}
	return NewEnumerable(out)
}

func (e *Enumerable) Sum() int {
	total := 0
	for _, v := range e.list {
		total += v
	}
	return total
}

func (e *Enumerable) Min() int {
	if len(e.list) == 0 {
		panic("NoElementsError")
	}
	min := e.list[0]
	for _, v := range e.list {
		if v < min {
			min = v
		}
	}
	return min
}

func (e *Enumerable) Max() int {
	if len(e.list) == 0 {
		panic("NoElementsError")
	}
	max := e.list[0]
	for _, v := range e.list {
		if v > max {
			max = v
		}
	}
	return max
}

func (e *Enumerable) Avg() float64 {
	if len(e.list) == 0 {
		panic("NoElementsError")
	}
	sum := 0
	for _, v := range e.list {
		sum += v
	}
	return float64(sum) / float64(len(e.list))
}

func TestPublicEnumerableToList(t *testing.T) {
	e := NewEnumerable([]int{13, 14, 15})
	got := e.ToList()
	want := []int{13, 14, 15}
	for i, v := range got {
		if v != want[i] {
			t.Errorf("at %d got %d want %d", i, v, want[i])
		}
	}
}

func TestPublicEnumerableReprAndGetItem(t *testing.T) {
	e := NewEnumerable([]int{1, 2, 3})
	r := e.Repr()
	if len(r) == 0 {
		t.Errorf("repr returned empty string")
	}
	if e.list[0] != 1 {
		t.Errorf("1st element want 1 got %d", e.list[0])
	}
	if e.list[2] != 3 {
		t.Errorf("3rd element want 3 got %d", e.list[2])
	}
}

func TestPublicEnumerableLenIterReversed(t *testing.T) {
	e := NewEnumerable([]int{7, 8, 9, 10})
	if len(e.list) != 4 {
		t.Errorf("Len want 4 got %d", len(e.list))
	}
	got := e.ToList()
	want := []int{7, 8, 9, 10}
	for i, v := range got {
		if v != want[i] {
			t.Errorf("At %d got %d want %d", i, v, want[i])
		}
	}
	r := []int{10, 9, 8, 7}
	for i, v := range r {
		if got[3-i] != v {
			t.Errorf("Reverse check at %d want %d got %d", i, v, got[3-i])
		}
	}
}

func TestPublicEnumerableCountPredicate(t *testing.T) {
	e := NewEnumerable([]int{1, 10, 100, 1000})
	cnt := e.Count(func(x int) bool { return x > 9 })
	if cnt != 3 {
		t.Errorf("Count predicate want 3 got %d", cnt)
	}
}

func TestPublicEnumerableSelectSumMinMaxAvg(t *testing.T) {
	e := NewEnumerable([]int{22, 4, 7})
	s := e.Select(func(x int) int { return x + 1 }).Sum()
	if s != 35 {
		t.Errorf("Select+Sum: got %d want 35", s)
	}
	minVal := e.Min()
	maxVal := e.Max()
	if minVal != 4 || maxVal != 22 {
		t.Errorf("min=%d max=%d want min=4 max=22", minVal, maxVal)
	}
	avg := e.Avg()
	if !(avg > 10.99 && avg < 11.01) {
		t.Errorf("avg = %v want 11", avg)
	}
}

func TestPublicEnumerableMinMaxAvgEmpty(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for NoElementsError")
		}
	}()
	ee := NewEnumerable([]int{})
	ee.Min()
}