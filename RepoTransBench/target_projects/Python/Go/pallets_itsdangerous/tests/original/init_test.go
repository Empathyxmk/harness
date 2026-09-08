package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"pallets_itsdangerous/src/itsdangerous"
)

func TestVersionIsString(t *testing.T) {
	version := itsdangerous.Version()
	assert.IsType(t, "", version)
	// Simulate a DeprecationWarning; Go doesn't have warnings. Mark test as passed if type is string.
}

func TestImportlibVersion(t *testing.T) {
	v := itsdangerous.ModuleVersion("itsdangerous")
	assert.Contains(t, v, ".")
}