package public_tests

import (
	"reflect"
	"testing"
)

func TestMatrixMultiplicationDifferentValues(t *testing.T) {
	a := [][]byte{
		{11, 22},
		{33, 44},
	}
	b := [][]byte{
		{2, 1},
		{0, 3},
	}
	expected := [][]byte{
		{11*2 + 22*0, 11*1 + 22*3},
		{33*2 + 44*0, 33*1 + 44*3},
	}
	actual := multiply(a, b)
	if !reflect.DeepEqual(expected[0], actual[0]) || !reflect.DeepEqual(expected[1], actual[1]) {
		t.Errorf("Expected %v and %v, got %v and %v", expected[0], expected[1], actual[0], actual[1])
	}
}

func multiply(a, b [][]byte) [][]byte {
	n, m, p := len(a), len(b[0]), len(b)
	c := make([][]byte, n)
	for i := 0; i < n; i++ {
		c[i] = make([]byte, m)
		for j := 0; j < m; j++ {
			for k := 0; k < p; k++ {
				c[i][j] += a[i][k] * b[k][j]
			}
		}
	}
	return c
}