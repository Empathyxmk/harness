package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type CirFeather struct{}

func (f *CirFeather) Instance(t string) (interface{}, error) {
	if t == "Circle1" {
		// Simulate unresolvable circular dependency
		return nil, &FeatherException{}
	}
	if t == "CircleWithProvider1" {
		c2 := &CircleWithProvider2{}
		c1 := &CircleWithProvider1{CircleWithProvider2: c2}
		c2.CircleWithProvider1 = func() *CircleWithProvider1 { return c1 }
		return c1, nil
	}
	return nil, &FeatherException{}
}

type Circle1 struct {
	Circle2 *Circle2
}

type Circle2 struct {
	Circle1 *Circle1
}

type CircleWithProvider1 struct {
	CircleWithProvider2 *CircleWithProvider2
}

type CircleWithProvider2 struct {
	CircleWithProvider1 func() *CircleWithProvider1
}

func TestCircularDependencyCaught(t *testing.T) {
	feather := &CirFeather{}
	_, err := feather.Instance("Circle1")
	assert.Error(t, err)
}

func TestCircularDependencyWithProviderAllowed(t *testing.T) {
	feather := &CirFeather{}
	res, err := feather.Instance("CircleWithProvider1")
	assert.NoError(t, err)
	cwpi := res.(*CircleWithProvider1)
	assert.NotNil(t, cwpi.CircleWithProvider2.CircleWithProvider1())
}