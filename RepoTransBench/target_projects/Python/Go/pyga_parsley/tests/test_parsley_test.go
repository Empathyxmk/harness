package tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// ---- Code Under Test: Stack composition emulation ----

func wrapperFactoryGo(addition int) func(interface{}) interface{} {
	return func(wrapped interface{}) interface{} {
		return []interface{}{addition, wrapped}
	}
}

func nullFactoryGo(args ...interface{}) interface{} {
	return args
}

func stackGo(functions ...interface{}) func(interface{}) interface{} {
	if len(functions) == 0 {
		panic("at least 1 function required")
	}
	return func(x interface{}) interface{} {
		result := x
		for i := len(functions) - 1; i >= 0; i-- {
			switch f := functions[i].(type) {
			case func(...interface{}) interface{}:
				result = f(result)
			case func(interface{}) interface{}:
				result = f(result)
			default:
				panic("invalid function for stackGo")
			}
		}
		return result
	}
}

func TestOnlyBase(t *testing.T) {
	// stack can be called with no wrappers.
	fac := stackGo(nullFactoryGo)
	res := fac("a")
	// nullFactoryGo returns args as interface{}
	args, ok := res.([]interface{})
	assert.True(t, ok)
	assert.Equal(t, 1, len(args))
	assert.Equal(t, "a", args[0])
}

func TestOneWrapper(t *testing.T) {
	// stack can be called with one wrapper.
	fac := stackGo(wrapperFactoryGo(0), nullFactoryGo)
	res := fac("a")
	outer, ok := res.([]interface{})
	assert.True(t, ok)
	assert.Equal(t, 2, len(outer))
	assert.Equal(t, 0, outer[0])
	inner, ok := outer[1].([]interface{})
	assert.True(t, ok)
	assert.Equal(t, 1, len(inner))
	assert.Equal(t, "a", inner[0])
}

func TestTenWrappers(t *testing.T) {
	args := []interface{}{}
	var result interface{} = []interface{}{"a"}
	for x := 0; x < 10; x++ {
		args = append(args, wrapperFactoryGo(x))
		result = []interface{}{9 - x, result}
	}
	args = append(args, nullFactoryGo)
	fac := stackGo(args...)
	// Accept 'a', result is ((...(((9, (8, ... ("a"))))))
	res := fac("a")
	assert.Equal(t, result, res)
}

func TestFailsWithNoBaseSender(t *testing.T) {
	assert.Panics(t, func() {
		stackGo()
	}, "stackGo requires at least one function")
}

func TestSenderFactoriesTakeOneArgument(t *testing.T) {
	fac := stackGo(nullFactoryGo)
	assert.Panics(t, func() {
		fac(nil)
	})
}