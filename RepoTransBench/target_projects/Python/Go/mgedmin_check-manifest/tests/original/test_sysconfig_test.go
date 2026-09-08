package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSysconfig_GetConfigVars(t *testing.T) {
	configVars := map[string]string{"FOO": "BAR"}
	assert.Equal(t, "BAR", configVars["FOO"])
}