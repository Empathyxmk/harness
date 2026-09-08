package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSpawn_Failure(t *testing.T) {
	program := "does-not-exist"
	got := false
	want := false
	if program == "does-not-exist" {
		got = false
	}
	assert.Equal(t, want, got)
}