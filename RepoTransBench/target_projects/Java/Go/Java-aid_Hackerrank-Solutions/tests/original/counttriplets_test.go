package original

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCountTriplets_TypicalCase(t *testing.T) {
	arr := []int64{1, 2, 2, 4}
	r := int64(2)
	expected := int64(2)
	assert.Equal(t, expected, countTriplets(arr, r))
}

func TestCountTriplets_AllOnesR1(t *testing.T) {
	arr := []int64{1, 1, 1, 1}
	r := int64(1)
	assert.Equal(t, int64(4), countTriplets(arr, r))
}

func TestCountTriplets_NoTriplets(t *testing.T) {
	arr := []int64{1, 2, 4, 8}
	r := int64(3)
	assert.Equal(t, int64(0), countTriplets(arr, r))
}

func TestCountTriplets_SingleElement(t *testing.T) {
	arr := []int64{7}
	r := int64(2)
	assert.Equal(t, int64(0), countTriplets(arr, r))
}

func TestCountTriplets_EmptyList(t *testing.T) {
	arr := []int64{}
	assert.Equal(t, int64(0), countTriplets(arr, 2))
}

func TestCountTriplets_MainTypicalCase(t *testing.T) {
	input := "4 2\n1 2 2 4\n"
	stdin := os.Stdin
	stdout := os.Stdout

	r, w, _ := os.Pipe()
	os.Stdin = io.NopCloser(bytes.NewReader([]byte(input)))
	os.Stdout = w

	MainCountTriplets()

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = stdout
	os.Stdin = stdin

	assert.True(t, strings.HasSuffix(strings.TrimSpace(string(out)), "2"))
}

func TestCountTriplets_MainEmpty(t *testing.T) {
	input := "0 2\n"
	stdin := os.Stdin
	stdout := os.Stdout

	r, w, _ := os.Pipe()
	os.Stdin = io.NopCloser(bytes.NewReader([]byte(input)))
	os.Stdout = w

	MainCountTriplets()

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = stdout
	os.Stdin = stdin

	outStr := strings.ReplaceAll(string(out), "\n", "")
	assert.True(t, strings.HasSuffix(strings.TrimSpace(outStr), "0"))
}

// --- Helper and Solution Stubs for CountTriplets ---

func countTriplets(arr []int64, r int64) int64 {
	left, right := make(map[int64]int64), make(map[int64]int64)
	for _, v := range arr {
		right[v]++
	}
	var count int64
	for _, v := range arr {
		right[v]--
		if v%r == 0 {
			count += left[v/r] * right[v*r]
		}
		left[v]++
	}
	return count
}

// MainCountTriplets simulates the main() as tested.
func MainCountTriplets() {
	var n, r int
	_, _ = fmt.Scanf("%d %d\n", &n, &r)
	s := ""
	fmt.Scanln(&s)
	if n == 0 {
		fmt.Println(0)
		return
	}
	var arr []int64
	for _, f := range strings.Fields(s) {
		var x int64
		fmt.Sscanf(f, "%d", &x)
		arr = append(arr, x)
	}
	fmt.Println(countTriplets(arr, int64(r)))
}