package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

type Animal struct {
	Species string `json:"species"`
	Age     int    `json:"age"`
}

func TestJsonSerializable_DumpPublic(t *testing.T) {
	a := Animal{Species: "cat", Age: 4}
	result := jsons.Dump(a)
	assert.Equal(t, map[string]interface{}{"species": "cat", "age": 4}, result)
}

func TestJsonSerializable_LoadPublic(t *testing.T) {
	input := map[string]interface{}{"species": "dog", "age": 10}
	obj := Animal{}
	err := jsons.Load(input, &obj)
	assert.NoError(t, err)
	assert.Equal(t, "dog", obj.Species)
	assert.Equal(t, 10, obj.Age)
}