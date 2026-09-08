package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestTripleSum_PublicInput1(t *testing.T) {
	a := []int{2, 3, 4, 4, 7}
	b := []int{1, 2, 5, 5}
	c := []int{3, 3, 5, 8}
	expected := int64(5)
	assert.Equal(t, expected, Triplets(a, b, c))
}

func TestTripleSum_PublicInput2(t *testing.T) {
	a := []int{3, 4, 7, 7, 10}
	b := []int{1, 3, 5, 7, 9}
	c := []int{2, 3, 6, 9}
	expected := int64(9)
	assert.Equal(t, expected, Triplets(a, b, c))
}

// Re-use or provide Triplets definition as in tests/original/triplesum_test.go
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

func removeDuplicates(arr []int) []int {
	m := make(map[int]struct{})
	for _, v := range arr {
		m[v] = struct{}{}
	}
	res := make([]int, 0, len(m))
	for k := range m {
		res = append(res, k)
	}
	// Sort
	for i := 0; i < len(res); i++ {
		for j := i + 1; j < len(res); j++ {
			if res[j] < res[i] {
				res[j], res[i] = res[i], res[j]
			}
		}
	}
	return res
}

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