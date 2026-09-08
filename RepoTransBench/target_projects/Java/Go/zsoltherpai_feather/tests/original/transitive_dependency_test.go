package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type TransitiveA struct {
	B *TransitiveB
}

type TransitiveB struct {
	C *TransitiveC
}

type TransitiveC struct{}

type TransitiveFeather struct{}

func (f *TransitiveFeather) Instance(t string) interface{} {
	switch t {
	case "A":
		return &TransitiveA{B: &TransitiveB{C: &TransitiveC{}}}
	default:
		return nil
	}
}

func TestTransitive(t *testing.T) {
	feather := &TransitiveFeather{}
	a := feather.Instance("A").(*TransitiveA)
	assert.NotNil(t, a.B.C)
}