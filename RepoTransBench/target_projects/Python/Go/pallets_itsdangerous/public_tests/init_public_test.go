package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"pallets_itsdangerous/src/itsdangerous"
)

func TestVersionIsStringPublic(t *testing.T) {
	version := itsdangerous.Version()
	assert.IsType(t, "", version)
	// No warnings in Go; only type check.
}

func TestImportlibVersionPublic(t *testing.T) {
	v := itsdangerous.ModuleVersion("itsdangerous")
	assert.Contains(t, v, ".")
}