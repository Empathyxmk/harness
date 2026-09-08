package original

import (
	"testing"
	"strings"
)

type RepeatableIterableString struct {
	data []string
	cur  int
}

func NewRepeatableIterableString(data []string) *RepeatableIterableString {
	return &RepeatableIterableString{data: data, cur: 0}
}

func (it *RepeatableIterableString) Len() int {
	return len(it.data)
}

func (it *RepeatableIterableString) Next() (string, bool) {
	if it.cur+1 < len(it.data) {
		it.cur++
		return it.data[it.cur], true
	}
	return "", false
}

func (it *RepeatableIterableString) Value() string {
	if len(it.data) > 0 {
		return it.data[it.cur]
	}
	return ""
}

func (it *RepeatableIterableString) Iter() []string {
	return it.data
}

func (it *RepeatableIterableString) Reversed() []string {
	n := len(it.data)
	out := make([]string, n)
	for i := n - 1; i >= 0; i-- {
		out[n-1-i] = it.data[i]
	}
	return out
}

func TestIterNone(t *testing.T) {
	ri := NewRepeatableIterableString([]string{})
	total := 0
	for _, _ = range ri.Iter() {
		total += 1
	}
	if total != 0 {
		t.Errorf("Expected sum==0 for empty iteration")
	}
}

func TestIterRange(t *testing.T) {
	ri := NewRepeatableIterableString([]string{"0", "1", "2", "3", "4"})
	for i, v := range ri.Iter() {
		if v != ri.data[i] {
			t.Errorf("Expected %v got %v", ri.data[i], v)
		}
	}
	if ri.Value() != "0" {
		t.Errorf("Expected current value '0', got %v", ri.Value())
	}
}

func TestLenRepeatable(t *testing.T) {
	ri := NewRepeatableIterableString([]string{"a", "b", "c"})
	if ri.Len() != 3 {
		t.Errorf("Expected len==3 got %d", ri.Len())
	}
	if ri.Value() != "a" {
		t.Errorf("Current value should be 'a', got %v", ri.Value())
	}
}

func TestNextRepeatable(t *testing.T) {
	ri := NewRepeatableIterableString([]string{"first", "second"})
	if ri.Len() != 2 {
		t.Errorf("Expected len==2 got %d", ri.Len())
	}
	if ri.Value() != "first" {
		t.Errorf("Current value should be 'first', got %v", ri.Value())
	}
	val, _ := ri.Next()
	if val != "second" {
		t.Errorf("Next returned %v want 'second'", val)
	}
}

func TestIterGeneratorRepeatable(t *testing.T) {
	items := []string{"Bruce", "viralogic", "software"}
	ri := NewRepeatableIterableString(items)
	if ri.Len() != 3 {
		t.Errorf("Expected len==3 got %d", ri.Len())
	}
	val, _ := ri.Next()
	if val != "viralogic" {
		t.Errorf("Next after start got %v want 'viralogic'", val)
	}
}

func TestReverseChainStringRepeatable(t *testing.T) {
	ri := NewRepeatableIterableString([]string{"1", "2", "3", "4"})
	reversed := ri.Reversed()
	want := []string{"4", "3", "2", "1"}
	for i, v := range reversed {
		if v != want[i] {
			t.Errorf("Reverse: At idx %d, got %v want %v", i, v, want[i])
		}
	}
}