package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestGetClassNameWithoutName(t *testing.T) {
	className := jsons.GetClassName(struct{ x int }{})
	assert.Equal(t, "struct", className)
	fq := jsons.GetClassNameFullyQualified(struct{ x int }{})
	assert.Contains(t, fq, "struct")
}

func TestGetClassNameOfNone(t *testing.T) {
	noneName := jsons.GetClassName(nil)
	assert.Equal(t, "NoneType", noneName)
}

func TestGetClsFromStr(t *testing.T) {
	assert.Equal(t, "string", jsons.GetClsFromStr("str", nil, nil).(string))
	assert.Equal(t, 123, jsons.GetClsFromStr("int", nil, nil).(int))
	assert.Equal(t, []int{}, jsons.GetClsFromStr("list", nil, nil))
}