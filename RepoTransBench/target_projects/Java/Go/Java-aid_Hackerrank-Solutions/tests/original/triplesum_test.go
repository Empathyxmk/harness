package original

import (
	"bytes"
	"io"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestTripleSum_TypicalCase(t *testing.T) {
	a := []int{1, 3, 5}
	b := []int{2, 3}
	c := []int{1, 2, 3}
	expected := int64(8) // As per problem sample test
	if Triplets(a, b, c) != expected {
		t.Errorf("Expected %v; got %v", expected, Triplets(a, b, c))
	}
}

func TestTripleSum_DuplicateValues(t *testing.T) {
	a := []int{1, 3, 5, 3}
	b := []int{2, 3, 3}
	c := []int{1, 2, 3, 1}
	expected := int64(8)
	if Triplets(a, b, c) != expected {
		t.Errorf("Expected %v; got %v", expected, Triplets(a, b, c))
	}
}

func TestTripleSum_AllZeros(t *testing.T) {
	a := []int{0, 0, 0}
	b := []int{0, 0}
	c := []int{0, 0}
	expected := int64(1)
	if Triplets(a, b, c) != expected {
		t.Errorf("Expected %v; got %v", expected, Triplets(a, b, c))
	}
}

func TestTripleSum_EmptyArrays(t *testing.T) {
	a, b, c := []int{}, []int{}, []int{}
	expected := int64(0)
	if Triplets(a, b, c) != expected {
		t.Errorf("Expected %v; got %v", expected, Triplets(a, b, c))
	}
}

func TestTripleSum_RemoveDuplicates(t *testing.T) {
	arr := []int{1, 1, 2, 2, 3, 3, 3}
	res := removeDuplicates(arr)
	assert.Len(t, res, 3)
	assert.ElementsMatch(t, res, []int{1, 2, 3})
}

func TestTripleSum_GetValidIndex(t *testing.T) {
	arr := []int{1, 2, 3, 4, 5}
	assert.Equal(t, 2, getValidIndex(arr, 3))
	assert.Equal(t, 4, getValidIndex(arr, 6))
	assert.Equal(t, -1, getValidIndex(arr, 0))
	assert.Equal(t, 0, getValidIndex([]int{2}, 2))
}

func TestTripleSum_MainExampleInput(t *testing.T) {
	input := "3 2 3\n1 3 5\n2 3\n1 2 3\n"
	expect := "8"

	stdin := os.Stdin
	stdout := os.Stdout

	r, w, _ := os.Pipe()
	os.Stdin = io.NopCloser(bytes.NewReader([]byte(input)))
	os.Stdout = w

	MainTripleSum()

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = stdout
	os.Stdin = stdin

	if !bytes.Contains(out, []byte(expect)) {
		t.Errorf("Expected output to contain %v, got %v", expect, string(out))
	}
}

func TestTripleSum_MainWithEmptyArrays(t *testing.T) {
	input := "0 0 0\n\n\n\n"
	expect := "0"

	stdin := os.Stdin
	stdout := os.Stdout

	r, w, _ := os.Pipe()
	os.Stdin = io.NopCloser(bytes.NewReader([]byte(input)))
	os.Stdout = w

	MainTripleSum()

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = stdout
	os.Stdin = stdin

	if !bytes.Contains(out, []byte(expect)) {
		t.Errorf("Expected output to contain %v, got %v", expect, string(out))
	}
}

// --- Helper and Solution Stubs for TripleSum ---

// Triplets calculates the number of triplets using the described rules.
func Triplets(a, b, c []int) int64 {
	ua := removeDuplicates(a)
	ub := removeDuplicates(b)
	uc := removeDuplicates(c)
	var cnt int64 = 0
	for _, q := range ub {
		an := getValidIndex(ua, q)
		cn := getValidIndex(uc, q)
		if an == -1 || cn == -1 {
			continue
		}
		cnt += int64(an+1) * int64(cn+1)
	}
	return cnt
}

// removeDuplicates returns a sorted slice with unique values.
func removeDuplicates(arr []int) []int {
	m := make(map[int]struct{})
	for _, v := range arr {
		m[v] = struct{}{}
	}
	res := make([]int, 0, len(m))
	for k := range m {
		res = append(res, k)
	}
	// Sorted for binary search simulation.
	for i := 0; i < len(res); i++ {
		for j := i + 1; j < len(res); j++ {
			if res[j] < res[i] {
				res[j], res[i] = res[i], res[j]
			}
		}
	}
	return res
}

// getValidIndex returns largest idx such that arr[idx] <= val, or -1 if not found.
func getValidIndex(arr []int, val int) int {
	if len(arr) == 0 {
		return -1
	}
	l, r := 0, len(arr)-1
	res := -1
	for l <= r {
		m := l + (r-l)/2
		if arr[m] <= val {
			res = m
			l = m + 1
		} else {
			r = m - 1
		}
	}
	return res
}

// MainTripleSum simulates the main() as tested.
func MainTripleSum() {
	var lena, lenb, lenc int
	_, _ = fmt.Scanf("%d %d %d\n", &lena, &lenb, &lenc)
	readInts := func(n int) []int {
		res := make([]int, 0, n)
		var s string
		if _, err := fmt.Scanln(&s); err != nil && err != io.EOF {
			return []int{}
		}
		for _, f := range strings.Fields(s) {
			var x int
			fmt.Sscanf(f, "%d", &x)
			res = append(res, x)
		}
		return res
	}
	a := readInts(lena)
	b := readInts(lenb)
	c := readInts(lenc)
	fmt.Println(Triplets(a, b, c))
}