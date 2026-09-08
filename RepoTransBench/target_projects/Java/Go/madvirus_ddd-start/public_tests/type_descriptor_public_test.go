package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TypeDescriptor emulation for test illustration
type TypeDescriptor struct{}

var (
	LONG_TYPE  *TypeDescriptor = &TypeDescriptor{}
	SHORT_TYPE *TypeDescriptor = &TypeDescriptor{}
)

func TestOtherPrimitiveTypesAreSingletons(t *testing.T) {
	assert.NotNil(t, LONG_TYPE)
	assert.NotNil(t, SHORT_TYPE)
}