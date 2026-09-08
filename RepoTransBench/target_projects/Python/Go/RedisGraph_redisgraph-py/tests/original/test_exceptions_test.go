package original

import (
	"testing"

	"redisgraph/exceptions"

	"github.com/stretchr/testify/assert"
)

func TestVersionMismatchException(t *testing.T) {
	version := "2.10.0"
	e := exceptions.NewVersionMismatchException(version)
	assert.IsType(t, &exceptions.VersionMismatchException{}, e)
	assert.Equal(t, version, e.Version)
}