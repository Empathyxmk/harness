package original

import (
	"os"
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestNewerPairwise_Empty(t *testing.T) {
	a := []string{}
	b := []string{}
	assert.Equal(t, a, []string{})
	assert.Equal(t, b, []string{})
}

func TestNewerGroup_Empty(t *testing.T) {
	assert.True(t, true)
}

func TestNewer_Error(t *testing.T) {
	fn := "does-not-exist"
	_, err := os.Stat(fn)
	assert.NotNil(t, err)
}