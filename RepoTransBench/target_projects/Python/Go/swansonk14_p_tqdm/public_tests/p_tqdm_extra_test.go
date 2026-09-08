package public_tests

import (
	"errors"
	"reflect"
	"regexp"
	"testing"
)

type PublicVersion struct {
	Version string
}

var ptqdmVersion = PublicVersion{"1.4.2"}

type PublicP_TQDM struct{}

func (p PublicP_TQDM) _sequential(fn interface{}, arrs ...[]int) []int {
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

var ptqdm = PublicP_TQDM{}

func TestVersionPublic(t *testing.T) {
	if ptqdmVersion.Version == "" {
		t.Error("ptqdmVersion.Version missing")
	}
	matched, err := regexp.MatchString(`\d+\.\d+\.\d+`, ptqdmVersion.Version)
	if err != nil {
		t.Fatal("Regex error:", err)
	}
	if !matched {
		t.Errorf("Expected version to match regex, got %s", ptqdmVersion.Version)
	}
}

func TestSequentialInternalPublic_Sequential(t *testing.T) {
	f := func(x int) int { return x * 3 }
	out := ptqdm._sequential(f, []int{2, 4, 6})
	expected := []int{6, 12, 18}
	if !reflect.DeepEqual(out, expected) {
		t.Errorf("Expected %v, got %v", expected, out)
	}
}

func TestSequentialInternalPublic_SequentialMultiple(t *testing.T) {
	f := func(a, b int) int { return a * b }
	out := ptqdm._sequential(f, []int{3, 4}, []int{5, 6})
	expected := []int{15, 24}
	if !reflect.DeepEqual(out, expected) {
		t.Errorf("Expected %v, got %v", expected, out)
	}
}

func TestSequentialInternalPublic_SequentialLength(t *testing.T) {
	f := func(x, y int) int { return x * y * 2 }
	out := ptqdm._sequential(f, []int{2, 3}, []int{7, 11})
	expected := []int{28, 66}
	if !reflect.DeepEqual(out, expected) {
		t.Errorf("Expected %v, got %v", expected, out)
	}
}

func TestSequentialInternalPublic_SequentialWithEmpty(t *testing.T) {
	f := func(x int) int { return x * 10 }
	out := ptqdm._sequential(f, []int{})
	expected := []int{}
	if !reflect.DeepEqual(out, expected) {
		t.Errorf("Expected %v, got %v", expected, out)
	}
}

func TestSequentialInternalPublic_SequentialWithException(t *testing.T) {
	f := func(x int) int {
		if x == 5 {
			panic(errors.New("terrible"))
		}
		return x * 2
	}
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic (RuntimeError), got none")
		}
	}()
	_ = ptqdm._sequential(f, []int{3, 5, 7})
}