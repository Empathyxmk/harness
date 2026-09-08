package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// ---- Code Under Test: Stack composition emulation with alternate logic ----

func wrapperFactoryPT(multiplier int) func(interface{}) interface{} {
	return func(wrapped interface{}) interface{} {
		return []interface{}{multiplier * 2, wrapped}
	}
}

func nullFactoryPT(args ...interface{}) interface{} {
	// Reverse args as per original nullFactory from public test
	out := make([]interface{}, len(args))
	for i, v := range args {
		out[len(args)-1-i] = v
	}
	return out
}

func stackPT(functions ...interface{}) func(interface{}) interface{} {
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
				panic("invalid function for stackPT")
			}
		}
		return result
	}
}

func TestOnlyBase(t *testing.T) {
	// identical to "stack can be called with no wrappers, using different base value and output."
	fac := stackPT(nullFactoryPT)
	res := fac("b")
	args, ok := res.([]interface{})
	assert.True(t, ok)
	assert.Equal(t, 1, len(args))
	assert.Equal(t, "b", args[0])
}

func TestOneWrapper(t *testing.T) {
	// one wrapper and a different multiplication
	fac := stackPT(wrapperFactoryPT(3), nullFactoryPT)
	res := fac("b")
	outer, ok := res.([]interface{})
	assert.True(t, ok)
	assert.Equal(t, 2, len(outer))
	assert.Equal(t, 6, outer[0]) // 3*2 per test
	inner, ok := outer[1].([]interface{})
	assert.True(t, ok)
	assert.Equal(t, 1, len(inner))
	assert.Equal(t, "b", inner[0])
}

func TestTenWrappers(t *testing.T) {
	args := []interface{}{}
	var result interface{} = []interface{}{"b"}
	for x := 0; x < 10; x++ {
		args = append(args, wrapperFactoryPT(x+1))
		result = []interface{}{10 - x, result}
	}
	args = append(args, nullFactoryPT)
	fac := stackPT(args...)
	res := fac("b")
	assert.Equal(t, result, res)
}

func TestFailsWithNoBaseSender(t *testing.T) {
	assert.Panics(t, func() {
		stackPT()
	}, "stackPT requires at least one function")
}

func TestSenderFactoriesTakeOneArgument(t *testing.T) {
	fac := stackPT(nullFactoryPT)
	assert.Panics(t, func() {
		fac(nil)
	})
	assert.Panics(t, func() {
		fac("b", "c")
	})
}