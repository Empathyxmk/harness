package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type PublicPlain struct{}

type AnotherUnknown struct {
	X int
}

type FeatherPublic struct{}

func (f *FeatherPublic) Instance(t string) (interface{}, error) {
	if t == "PublicPlain" {
		return &PublicPlain{}, nil
	}
	if t == "AnotherUnknown" {
		return nil, &FeatherException{}
	}
	return nil, &FeatherException{}
}

func (f *FeatherPublic) Provider(t string) func() (interface{}, error) {
	return func() (interface{}, error) {
		if t == "PublicPlain" {
			return &PublicPlain{}, nil
		}
		return nil, &FeatherException{}
	}
}

type FeatherException struct{}

func (e *FeatherException) Error() string {
	return "FeatherException"
}

func TestDependencyInstancePublic(t *testing.T) {
	feather := &FeatherPublic{}
	res, err := feather.Instance("PublicPlain")
	assert.NotNil(t, res)
	assert.NoError(t, err)
}

func TestProviderPublic(t *testing.T) {
	feather := &FeatherPublic{}
	provider := feather.Provider("PublicPlain")
	val, err := provider()
	assert.NotNil(t, val)
	assert.NoError(t, err)
}

func TestUnknownPublic(t *testing.T) {
	feather := &FeatherPublic{}
	_, err := feather.Instance("AnotherUnknown")
	assert.Error(t, err)
	_, ok := err.(*FeatherException)
	if !ok {
		t.Errorf("Expected FeatherException, got %T", err)
	}
}