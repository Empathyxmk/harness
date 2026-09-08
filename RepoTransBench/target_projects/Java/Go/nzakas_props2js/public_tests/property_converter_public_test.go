package public_tests

import (
	"testing"

	"nzakas_props2js/props2js"
	"tests"
)

func TestConvertToJson_withString_public(t *testing.T) {
	p := map[string]string{"color": "blue"}
	json := props2js.ConvertToJson(p)
	tests.AssertContains(t, json, `"color":"blue"`)
}

// ... (rest: update calls to props2js.X)