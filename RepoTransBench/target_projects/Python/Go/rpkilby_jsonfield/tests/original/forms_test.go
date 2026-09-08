package original

import (
	"reflect"
	"testing"

	"rpkilby_jsonfield/src/jsonfield"
	"rpkilby_jsonfield/src"
)

func TestBlankForm(t *testing.T) {
	form := jsonfield.NewJSONFormField(false)
	out, err := form.Clean("")
	if err != nil {
		t.Error("Expected no error, got", err)
	}
	if out != nil {
		t.Errorf("Expected nil, got %v", out)
	}
}

func TestFormWithData(t *testing.T) {
	form := jsonfield.NewJSONFormField(false)
	out, err := form.Clean(`{}`)
	if err != nil || out == nil {
		t.Errorf("Expected good JSON, got error=%v", err)
	}
}

func TestFormSave(t *testing.T) {
	// This simulates saving the form after validation
	form := jsonfield.NewJSONFormField(false)
	_, err := form.Clean("")
	if err != nil {
		t.Error("Expected no error saving blank")
	}
}

func TestSaveValues(t *testing.T) {
	cases := []struct {
		name  string
		input string
		dbVal interface{}
	}{
		{"object", `{"a": "b"}`, map[string]interface{}{"a": "b"}},
		{"array", `[1, 2]`, []interface{}{float64(1), float64(2)}},
		{"string", `"test"`, "test"},
		{"float", "1.2", 1.2},
		{"int", "1234", 1234.0},
		{"bool", "true", true},
		{"null", "null", nil},
	}
	form := jsonfield.NewJSONFormField(false)
	for _, c := range cases {
		v, err := form.Clean(c.input)
		if err != nil {
			t.Fatalf("Failed for %s: %v", c.name, err)
		}
		if !reflect.DeepEqual(v, c.dbVal) {
			t.Fatalf("%s: got %v, want %v", c.name, v, c.dbVal)
		}
	}
}

func TestRenderUnicode(t *testing.T) {
	form := jsonfield.NewJSONFormField(false)
	val, err := form.Clean(`"✨"`)
	if err != nil {
		t.Errorf("Failed to parse unicode: %v", err)
	}
	if val != "✨" {
		t.Errorf("Expected '✨', got %v", val)
	}
}

func TestInvalidValue(t *testing.T) {
	form := jsonfield.NewJSONFormField(false)
	_, err := form.Clean("foo")
	if err == nil {
		t.Error("Expected error for invalid JSON")
	}
}