package tests

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

type AllIntBean struct {
	Value [32]int
}

func (a *AllIntBean) SetValue(idx, val int) {
	a.Value[idx] = val
}
func (a *AllIntBean) GetValue(idx int) int {
	return a.Value[idx]
}

func TestUnsafeTestFields(t *testing.T) {
	bean := &AllIntBean{}
	for i := 0; i < 32; i++ {
		bean.SetValue(i, i)
	}
	for i := 0; i < 32; i++ {
		assert.Equal(t, i, bean.GetValue(i))
	}
	typ := reflect.TypeOf(*bean)
	assert.Equal(t, 1, typ.NumField())
}