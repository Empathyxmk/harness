package original

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestFlag(t *testing.T) {
	const (
		A = 0
		B = 10
		C = 20
		D = 40
		E = 80
	)
	type Flag int
	const (
		FlagA Flag = A
		FlagB Flag = B
		FlagC Flag = C
		FlagD Flag = D
		FlagE Flag = E
	)
	fc := FlagC
	assert.Equal(t, 20, int(fc))
	orVal := FlagB | FlagC
	assert.Equal(t, 30, int(orVal))
	assert.True(t, fc&(FlagB|FlagC) == fc)
	assert.True(t, FlagB&(FlagB|FlagC) == FlagB)
	assert.True(t, FlagC&(FlagB|FlagC) == FlagC)
	assert.True(t, FlagD&(FlagB|FlagC) != FlagD)
	assert.True(t, FlagC&(FlagB|FlagD) != FlagC)
	assert.True(t, FlagE&(FlagB|FlagD) != FlagE)
}

func TestGetTypeHints(t *testing.T) {
	globalns := map[string]interface{}{"foo": 42}
	getTypeHintsMock := func(fn interface{}, ns map[string]interface{}) map[string]interface{} {
		if ns == nil {
			panic("no ns")
		}
		return ns
	}
	defer func() {
		recover()
	}()
	_ = getTypeHintsMock(func() int { return 42 }, globalns)
	assert.Equal(t, 42, globalns["foo"])
}