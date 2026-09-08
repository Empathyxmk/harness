package original

import (
	"testing"
	"errors"

	"github.com/stretchr/testify/assert"
)

// Example helpers, update types/functions to match real implementation.
func AddInts(a, b int) int {
	return a + b
}

func RaisesError(a int) (int, error) {
	if a < 0 {
		return 0, errors.New("negative not allowed")
	}
	return a * 2, nil
}

func TestAddIntsBasic(t *testing.T) {
	assert.Equal(t, 3, AddInts(1, 2))
	assert.Equal(t, -1, AddInts(-2, 1))
}

func TestRaisesError(t *testing.T) {
	val, err := RaisesError(5)
	assert.Nil(t, err)
	assert.Equal(t, 10, val)
	_, err = RaisesError(-1)
	assert.NotNil(t, err)
	assert.EqualError(t, err, "negative not allowed")
}

func TestDictMerge(t *testing.T) {
	d1 := map[string]int{"a": 1, "b": 2}
	d2 := map[string]int{"b": 3, "c": 4}
	merged := DictMerge(d1, d2)
	assert.Equal(t, map[string]int{"a": 1, "b": 3, "c": 4}, merged)
}

// Helper function for merging two dictionaries (maps).
func DictMerge(m1, m2 map[string]int) map[string]int {
	result := map[string]int{}
	for k, v := range m1 {
		result[k] = v
	}
	for k, v := range m2 {
		result[k] = v
	}
	return result
}