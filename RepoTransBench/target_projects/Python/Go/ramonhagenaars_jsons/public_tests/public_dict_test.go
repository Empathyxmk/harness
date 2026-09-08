package public_tests

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestLoadsDictWithIntegers(t *testing.T) {
	data := `{"g": 20, "h": 30}`
	var loaded map[string]int
	err := jsons.Loads(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, map[string]int{"g": 20, "h": 30}, loaded)
}

func TestLoadsDictWithStringAndFloat(t *testing.T) {
	data := `{"x": "value", "y": 33.8}`
	var loaded map[string]interface{}
	err := jsons.Loads(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"x": "value", "y": 33.8}, loaded)
}

func TestDumpsDictWithVariedTypes(t *testing.T) {
	data := map[string]interface{}{"planet": "Earth", "moons": 1, "has_life": true}
	dumped := jsons.Dumps(data)
	assert.Contains(t, dumped, `"planet":"Earth"`)
	assert.Contains(t, dumped, `"moons":1`)
	assert.Contains(t, dumped, `"has_life":true`)
}