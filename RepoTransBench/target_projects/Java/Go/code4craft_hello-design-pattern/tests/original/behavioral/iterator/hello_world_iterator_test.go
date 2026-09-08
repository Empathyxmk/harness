package iterator

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Custom iterator to simulate Java's HelloWorldCharacterIterator
type HelloWorldCharacterIterator struct {
	arr    []rune
	cursor int
}

func NewHelloWorldCharacterIterator(arr []rune) *HelloWorldCharacterIterator {
	return &HelloWorldCharacterIterator{arr: arr}
}

func (it *HelloWorldCharacterIterator) HasNext() bool {
	return it.cursor < len(it.arr)
}

func (it *HelloWorldCharacterIterator) Next() rune {
	if !it.HasNext() {
		panic("No more elements")
	}
	val := it.arr[it.cursor]
	it.cursor++
	return val
}

func (it *HelloWorldCharacterIterator) Remove() {
	panic("remove not supported")
}

func TestHelloWorldIterator(t *testing.T) {
	helloIterator := "Hello Iterator!"
	it := NewHelloWorldCharacterIterator([]rune(helloIterator))
	var result []rune
	for it.HasNext() {
		result = append(result, it.Next())
	}
	assert.Equal(t, helloIterator, string(result))
}

func TestHelloWorldIteratorRemove(t *testing.T) {
	helloIterator := "Hello Iterator!"
	it := NewHelloWorldCharacterIterator([]rune(helloIterator))
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for Remove()")
		}
	}()
	it.Remove()
}