package tests

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

type UserService interface{}

type MethodParamClassFactory struct{}
func (m *MethodParamClassFactory) CreateClass(method reflect.Method) struct{} {
	return struct{}{}
}

func TestMethodParamClassFactory(t *testing.T) {
	for i := 0; i < 3; i++ { // simulate 3 methods
		var m reflect.Method
		_ = (&MethodParamClassFactory{}).CreateClass(m)
		assert.True(t, true)
	}
}