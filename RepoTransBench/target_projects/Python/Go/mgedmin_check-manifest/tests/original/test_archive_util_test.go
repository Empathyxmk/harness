package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func allEqual[T comparable](vals ...T) bool {
	if len(vals) == 0 {
		return true
	}
	a := vals[0]
	for _, v := range vals[1:] {
		if v != a {
			return false
		}
	}
	return true
}

func sameDrive(paths ...string) bool {
	return allEqual(paths...)
}

func TestArchiveUtil_AllEqual(t *testing.T) {
	assert.True(t, allEqual("A", "A", "A"))
	assert.False(t, allEqual("A", "B"))
}

func TestArchiveUtil_SameDrive(t *testing.T) {
	assert.True(t, sameDrive("/a/b", "/a/b", "/a/b"))
	assert.False(t, sameDrive("/a/b", "/a/c"))
}