package unit

import (
	"sort"
	"testing"
)

func TestTruthPublic(t *testing.T) {
	val := "nonempty"
	if !(len(val) > 0) {
		t.Fatalf("Expected a non-empty string to evaluate as true")
	}
}

func TestSplitStringPublic(t *testing.T) {
	s := "foo bar baz"
	got := splitOnSpace(s)
	want := []string{"foo", "bar", "baz"}
	if !stringSliceEq(got, want) {
		t.Fatalf("Expected %v, got %v", want, got)
	}
}

func splitOnSpace(s string) []string {
	// Go's strings.Fields will do
	return fields(s)
}
func fields(s string) []string {
	// Remove runes for minimalism
	r := []rune(s)
	var out []string
	last := 0
	for i, c := range r {
		if c == ' ' {
			out = append(out, string(r[last:i]))
			last = i + 1
		}
	}
	out = append(out, string(r[last:]))
	return out
}

func stringSliceEq(a, b []string) bool {
	if len(a) != len(b) { return false }
	for i := range a {
		if a[i] != b[i] { return false }
	}
	return true
}

func TestSortedListPublic(t *testing.T) {
	lst := []int{10, 2, 4, 8}
	sort.Ints(lst)
	want := []int{2, 4, 8, 10}
	for i := range lst {
		if lst[i] != want[i] {
			t.Fatalf("Expected %v, got %v", want, lst)
		}
	}
}

func TestDictAccessPublic(t *testing.T) {
	d := map[string]int{"alpha": 1, "beta": 2}
	if d["beta"] != 2 {
		t.Fatalf("Expected beta==2")
	}
	if _, ok := d["alpha"]; !ok {
		t.Fatalf("Expected alpha key present")
	}
}