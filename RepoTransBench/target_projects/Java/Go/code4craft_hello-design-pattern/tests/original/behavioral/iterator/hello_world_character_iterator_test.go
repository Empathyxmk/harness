package iterator

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type CharIterator struct {
	arr    []rune
	cursor int
}

func NewCharIterator(arr []rune) *CharIterator {
	return &CharIterator{arr: arr}
}

func (it *CharIterator) HasNext() bool {
	return it.cursor < len(it.arr)
}

func (it *CharIterator) Next() rune {
	if !it.HasNext() {
		panic("no such element")
	}
	val := it.arr[it.cursor]
	it.cursor++
	return val
}

func TestIterator(t *testing.T) {
	arr := []rune{'A', 'B', 'C'}
	iter := NewCharIterator(arr)
	assert.True(t, iter.HasNext())
	assert.Equal(t, 'A', iter.Next())
	assert.True(t, iter.HasNext())
	assert.Equal(t, 'B', iter.Next())
	assert.True(t, iter.HasNext())
	assert.Equal(t, 'C', iter.Next())
	assert.False(t, iter.HasNext())
}

func TestNextThrows(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for empty iterator Next()")
		}
	}()
	arr := []rune{}
	iter := NewCharIterator(arr)
	iter.Next()
}