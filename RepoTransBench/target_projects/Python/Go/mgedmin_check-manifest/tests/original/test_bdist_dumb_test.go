package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestBuildDumb_SimpleBuilt(t *testing.T) {
	files := []string{
		"foo-0.1-py3.8.egg-info",
		"foo.py",
		"foo.pyc",
	}
	want := []string{
		"foo-0.1-py3.8.egg-info",
		"foo.py",
		"foo.pyc",
	}
	assert.ElementsMatch(t, files, want)
}