package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Plain struct{}

type Unknown struct {
	Msg string
}

type Feather struct{}

func (f *Feather) Instance(t string) (interface{}, error) {
	if t == "Plain" {
		return &Plain{}, nil
	}
	if t == "Unknown" {
		return nil, &FeatherException{}
	}
	return nil, &FeatherException{}
}

func (f *Feather) Provider(t string) func() (interface{}, error) {
	return func() (interface{}, error) {
		if t == "Plain" {
			return &Plain{}, nil
		}
		return nil, &FeatherException{}
	}
}

type FeatherException struct{}

func (e *FeatherException) Error() string {
	return "FeatherException"
}

func TestDependencyInstance(t *testing.T) {
	feather := &Feather{}
	res, err := feather.Instance("Plain")
	assert.NotNil(t, res)
	assert.NoError(t, err)
}

func TestProvider(t *testing.T) {
	feather := &Feather{}
	provider := feather.Provider("Plain")
	val, err := provider()
	assert.NotNil(t, val)
	assert.NoError(t, err)
}

func TestUnknownDependency(t *testing.T) {
	feather := &Feather{}
	_, err := feather.Instance("Unknown")
	assert.Error(t, err)
	_, ok := err.(*FeatherException)
	if !ok {
		t.Errorf("Expected FeatherException, got %T", err)
	}
}