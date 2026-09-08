package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type Extension struct {
	Name    string
	Sources []string
}

func NewExtension(name string, sources []string) *Extension {
	if name == "" {
		panic("name must not be empty")
	}
	return &Extension{Name: name, Sources: sources}
}

func TestExtension_Init(t *testing.T) {
	ext := NewExtension("name", []string{})
	assert.Equal(t, "name", ext.Name)
	assert.Equal(t, []string{}, ext.Sources)
}

func TestExtension_TypeError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for bad type")
		}
	}()
	_ = NewExtension("", nil)
}