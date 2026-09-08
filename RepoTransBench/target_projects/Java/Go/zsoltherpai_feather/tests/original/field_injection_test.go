package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type FieldA struct{}
type FieldTarget struct {
	A *FieldA
}

type FieldFeather struct{}

func (f *FieldFeather) InjectFields(target *FieldTarget) {
	target.A = &FieldA{}
}

func TestFieldsInjected(t *testing.T) {
	feather := &FieldFeather{}
	target := &FieldTarget{}
	feather.InjectFields(target)
	assert.NotNil(t, target.A)
}