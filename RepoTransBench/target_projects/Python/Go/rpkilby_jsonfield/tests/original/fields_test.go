package original

import (
	"testing"
	"reflect"
	"github.com/stretchr/testify/assert"
	"rpkilby_jsonfield/src/jsonfield"
)

func TestGetPrepValueAlwaysJSONDumpsIfNotNull(t *testing.T) {
	field := jsonfield.NewJSONField(jsonfield.WithNull(false))
	value := map[string]interface{}{"a": 1}
	preparedValue := field.GetPrepValue(value)
	assert.IsType(t, "", preparedValue)
	var parsed map[string]interface{}
	err := jsonfield.Loads(preparedValue.(string), &parsed)
	assert.Nil(t, err)
	assert.Equal(t, value, parsed)
	alreadyJson, _ := jsonfield.DUMPS(value)
	doublePreparedValue := field.GetPrepValue(alreadyJson)
	var dparsed map[string]interface{}
	err = jsonfield.Loads(doublePreparedValue.(string), &dparsed)
	assert.Nil(t, err)
	assert.Equal(t, value, dparsed)
	assert.Equal(t, "null", field.GetPrepValue(nil))
}

func TestGetPrepValueCanReturnNoneIfNull(t *testing.T) {
	field := jsonfield.NewJSONField(jsonfield.WithNull(true))
	value := map[string]interface{}{"a": 1}
	preparedValue := field.GetPrepValue(value)
	assert.IsType(t, "", preparedValue)
	var parsed map[string]interface{}
	err := jsonfield.Loads(preparedValue.(string), &parsed)
	assert.Nil(t, err)
	assert.Equal(t, value, parsed)
	alreadyJson, _ := jsonfield.DUMPS(value)
	doublePreparedValue := field.GetPrepValue(alreadyJson)
	var dparsed map[string]interface{}
	err = jsonfield.Loads(doublePreparedValue.(string), &dparsed)
	assert.Nil(t, err)
	assert.Equal(t, value, dparsed)
	assert.Nil(t, field.GetPrepValue(nil))
}

func TestDeconstructDefaultKwargs(t *testing.T) {
	field := jsonfield.NewJSONField()
	_, _, _, kwargs := field.Deconstruct()
	_, ok := kwargs["dump_kwargs"]
	assert.False(t, ok)
	_, ok = kwargs["load_kwargs"]
	assert.False(t, ok)
}

func TestDeconstructNonDefaultKwargs(t *testing.T) {
	field := jsonfield.NewJSONField(
		jsonfield.WithDumpKwargs(map[string]interface{}{"separators": []interface{}{",", ":"}}),
		jsonfield.WithEncoder("encoder"),
		jsonfield.WithDecoder("decoder"),
	)
	_, _, _, kwargs := field.Deconstruct()
	assert.Equal(t, map[string]interface{}{"separators": []interface{}{",", ":"}}, kwargs["dump_kwargs"])
	assert.Equal(t, "encoder", kwargs["encoder_class"])
	assert.Equal(t, "decoder", kwargs["decoder_class"])
}

func TestFromDBValueLoadedTypes(t *testing.T) {
	field := jsonfield.NewJSONField()
	cases := []struct {
		label    string
		dbValue  string
		expType  reflect.Type
	}{
		{"object", `{"a": "b"}`, reflect.TypeOf(map[string]interface{}{})},
		{"array", `[1, 2]`, reflect.TypeOf([]interface{}{})},
		{"string", `"test"`, reflect.TypeOf("")},
		{"float", `1.2`, reflect.TypeOf(float64(0))},
		{"int", `1234`, reflect.TypeOf(float64(0))},
		{"bool", `true`, reflect.TypeOf(true)},
		{"null", `null`, nil},
	}
	for _, c := range cases {
		val := field.FromDBValue(c.dbValue, nil, nil, nil)
		if c.expType == nil {
			assert.Nil(t, val)
		} else {
			assert.Equal(t, c.expType, reflect.TypeOf(val))
		}
	}
}