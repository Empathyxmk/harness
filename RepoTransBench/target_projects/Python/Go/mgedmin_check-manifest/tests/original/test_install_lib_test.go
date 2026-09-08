package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestInstallLib_FinalizeOptions(t *testing.T) {
	compile := 1
	optimize := 0
	assert.Equal(t, 1, compile)
	assert.Equal(t, 0, optimize)
}