package original

import (
	"errors"
	"reflect"
	"testing"
)

// Simulated Version struct
type P_TQDMVersion struct {
	Version     string
	VersionInfo []int
}

var ptqdmVersion = P_TQDMVersion{"1.4.2", []int{1, 4, 2}}

// Simulate p_tqdm module with stub _sequential
type P_TQDM struct{}

func (p P_TQDM) _sequential(fn interface{}, arrs ...[]int) []int {
	// For the tests, switch on arity based on function type
	if len(arrs) == 0 {
		return []int{}
	}
	switch f := fn.(type) {
	case func(int) int:
		out := make([]int, len(arrs[0]))
		for i, v := range arrs[0] {
			out[i] = f(v)
		}
		return out
	case func(int, int) int:
		n := min(len(arrs[0]), len(arrs[1]))
		out := make([]int, n)
		for i := 0; i < n; i++ {
			out[i] = f(arrs[0][i], arrs[1][i])
		}
		return out
	default:
		return []int{}
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

var ptqdm = P_TQDM{}

// TestVersion test
func TestVersion(t *testing.T) {
	if ptqdmVersion.Version == "" {
		t.Error("ptqdm_version.Version missing")
	}
	if ptqdmVersion.Version != "1.4.2" {
		t.Errorf("Expected 1.4.2, got %v", ptqdmVersion.Version)
	}
	if !reflect.DeepEqual(ptqdmVersion.VersionInfo, []int{1, 4, 2}) {
		t.Errorf("VersionInfo mismatch: %v", ptqdmVersion.VersionInfo)
	}
}

// Test internal sequential logic
func TestSequential(t *testing.T) {
	f := func(x int) int { return x + 1 }
	out := ptqdm._sequential(f, []int{1, 2, 3})
	correct := []int{2, 3, 4}
	if !reflect.DeepEqual(out, correct) {
		t.Errorf("Expected %v, got %v", correct, out)
	}
}

func TestSequentialMultiple(t *testing.T) {
	f := func(a, b int) int { return a + b }
	out := ptqdm._sequential(f, []int{1, 2}, []int{2, 3})
	correct := []int{3, 5}
	if !reflect.DeepEqual(out, correct) {
		t.Errorf("Expected %v, got %v", correct, out)
	}
}

func TestSequentialLength(t *testing.T) {
	f := func(x, y int) int { return x + y }
	out := ptqdm._sequential(f, []int{1, 2}, []int{5, 10})
	correct := []int{6, 12}
	if !reflect.DeepEqual(out, correct) {
		t.Errorf("Expected %v, got %v", correct, out)
	}
}

func TestSequentialWithEmpty(t *testing.T) {
	f := func(x int) int { return x }
	out := ptqdm._sequential(f, []int{})
	correct := []int{}
	if !reflect.DeepEqual(out, correct) {
		t.Errorf("Expected %v, got %v", correct, out)
	}
}

func TestSequentialWithException(t *testing.T) {
	f := func(x int) int {
		if x == 2 {
			panic(errors.New("bad"))
		}
		return x + 1
	}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic (ValueError), got none")
		}
	}()
	_ = ptqdm._sequential(f, []int{1, 2, 3})
}