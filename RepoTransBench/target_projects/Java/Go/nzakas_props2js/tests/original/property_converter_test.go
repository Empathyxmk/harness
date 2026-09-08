package original

import (
	"testing"

	"nzakas_props2js/props2js"
	"tests"
)

func TestConvertToJson_withString(t *testing.T) {
	p := map[string]string{"name": "value"}
	json := props2js.ConvertToJson(p)
	tests.AssertContains(t, json, `"name":"value"`)
}

func TestConvertToJson_withInt(t *testing.T) {
	p := map[string]string{"intValue": "123"}
	json := props2js.ConvertToJson(p)
	tests.AssertContains(t, json, `"intValue":123`)
}

// ... (rest of tests, switch call to props2js.ConvertToJson/etc)