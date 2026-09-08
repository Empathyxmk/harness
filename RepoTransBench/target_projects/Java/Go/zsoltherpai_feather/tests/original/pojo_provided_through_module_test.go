package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Pojo struct {
	Foo string
}

type PojoFeather struct {
	hasModule bool
}

func (f *PojoFeather) Instance(t string) (interface{}, error) {
	if t == "Pojo" && f.hasModule {
		return &Pojo{Foo: "foo"}, nil
	}
	return nil, &FeatherException{}
}

func TestPojoNotProvided(t *testing.T) {
	feather := &PojoFeather{}
	_, err := feather.Instance("Pojo")
	assert.Error(t, err)
}

func TestPojoProvided(t *testing.T) {
	feather := &PojoFeather{hasModule: true}
	result, err := feather.Instance("Pojo")
	assert.NoError(t, err)
	assert.NotNil(t, result)
}