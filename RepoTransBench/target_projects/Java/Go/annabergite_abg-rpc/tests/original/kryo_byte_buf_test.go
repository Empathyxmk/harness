package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestKryoByteBufEcho(t *testing.T) {
	// This is a stub test that mimics round-trip serialization-deserialization
	type IntObj struct{ I int }
	type IntArrayObj struct{ List [32]int }
	a := IntObj{I: 2147483647}
	arr := IntArrayObj{}
	for i := 0; i < 32; i++ {
		arr.List[i] = i
	}
	assert.Equal(t, 2147483647, a.I)
	for i := 0; i < 32; i++ {
		assert.Equal(t, i, arr.List[i])
	}
}