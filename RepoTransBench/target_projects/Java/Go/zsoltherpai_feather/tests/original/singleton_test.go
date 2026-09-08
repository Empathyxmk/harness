package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type SingletonObj struct{}

type SingletonFeather struct {
	singleton   *SingletonObj
	used        bool
	plainCalled int
}

func (f *SingletonFeather) Instance(t string) (interface{}, error) {
	switch t {
	case "Plain":
		f.plainCalled++
		return &Plain{}, nil
	case "SingletonObj":
		if f.singleton == nil {
			f.singleton = &SingletonObj{}
		}
		return f.singleton, nil
	default:
		return nil, &FeatherException{}
	}
}

func (f *SingletonFeather) Provider(t string) func() (interface{}, error) {
	return func() (interface{}, error) {
		return f.Instance(t)
	}
}

func TestNonSingleton(t *testing.T) {
	feather := &SingletonFeather{}
	v1, _ := feather.Instance("Plain")
	v2, _ := feather.Instance("Plain")
	assert.NotEqual(t, v1, v2)
}

func TestSingleton(t *testing.T) {
	feather := &SingletonFeather{}
	v1, _ := feather.Instance("SingletonObj")
	v2, _ := feather.Instance("SingletonObj")
	assert.Equal(t, v1, v2)
}

func TestSingletonThroughProvider(t *testing.T) {
	feather := &SingletonFeather{}
	provider := feather.Provider("SingletonObj")
	v1, _ := provider()
	v2, _ := provider()
	assert.Equal(t, v1, v2)
}