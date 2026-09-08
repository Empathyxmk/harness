package original

import (
	"testing"

	"redisgraph/util"

	"github.com/stretchr/testify/assert"
)

func TestRandomStringLength(t *testing.T) {
	lengths := []int{1, 5, 10, 32}
	for _, n := range lengths {
		s := util.RandomString(n)
		assert.IsType(t, "", s)
		assert.Equal(t, n, len(s))
	}
}

func TestQuoteStringBasic(t *testing.T) {
	assert.Equal(t, `"abc"`, util.QuoteString("abc"))
	assert.Equal(t, `"bytes"`, util.QuoteString([]byte("bytes")))
	assert.Equal(t, `""`, util.QuoteString(""))
	assert.Equal(t, `"he\"llo"`, util.QuoteString(`he"llo`))
	assert.Equal(t, `"back\\slash"`, util.QuoteString(`back\slash`))
	assert.Equal(t, 123, util.QuoteString(123))
}

func TestStringifyParamValueBasic(t *testing.T) {
	assert.Equal(t, `"foo"`, util.StringifyParamValue("foo"))
	assert.Equal(t, "null", util.StringifyParamValue(nil))
	assert.Equal(t, `[1,null,"x"]`, util.StringifyParamValue([]interface{}{1, nil, "x"}))
	assert.Equal(t, `[2,3]`, util.StringifyParamValue([2]int{2, 3}))
	m1 := util.StringifyParamValue(map[string]interface{}{"a": 1, "b": "z"})
	assert.Contains(t, []string{`{a:1,b:"z"}`, `{b:"z",a:1}`}, m1)
	assert.Equal(t, "3.14", util.StringifyParamValue(3.14))
	assert.Equal(t, "7", util.StringifyParamValue(7))
}