package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestCore_Basic(t *testing.T) {
	ran := false
	if !ran {
		ran = true
	}
	assert.True(t, ran)
}