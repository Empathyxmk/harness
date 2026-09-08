package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// TypeDescriptor emulation for test illustration
type TypeDescriptor struct{}

var (
	BOOLEAN_TYPE *TypeDescriptor = &TypeDescriptor{}
	BYTE_TYPE    *TypeDescriptor = &TypeDescriptor{}
	CHAR_TYPE    *TypeDescriptor = &TypeDescriptor{}
	DOUBLE_TYPE  *TypeDescriptor = &TypeDescriptor{}
	FLOAT_TYPE   *TypeDescriptor = &TypeDescriptor{}
	INT_TYPE     *TypeDescriptor = &TypeDescriptor{}
)

func TestPrimitiveTypesAreSingletons(t *testing.T) {
	assert.NotNil(t, BOOLEAN_TYPE)
	assert.NotNil(t, BYTE_TYPE)
	assert.NotNil(t, CHAR_TYPE)
	assert.NotNil(t, DOUBLE_TYPE)
	assert.NotNil(t, FLOAT_TYPE)
	assert.NotNil(t, INT_TYPE)
}