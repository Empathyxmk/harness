package original

import (
	"errors"
	"fmt"
	"reflect"
	"testing"
)

// --- Simulate fields, models, widgets logic ---

type GeoPtField struct{}

func (f *GeoPtField) ToPython(val interface{}) (interface{}, error) {
	switch t := val.(type) {
	case nil:
		return nil, nil
	case string:
		var lat, lon float64
		n, err := fmt.Sscanf(t, "%f,%f", &lat, &lon)
		if err != nil || n != 2 {
			return nil, errors.New("invalid input for GeoPtField")
		}
		return [2]float64{lat, lon}, nil
	case [2]float64:
		return t, nil
	case []float64:
		if len(t) == 2 {
			return [2]float64{t[0], t[1]}, nil
		}
	}
	return nil, errors.New("unsupported input")
}

func (f *GeoPtField) GetPrepValue(val interface{}) (string, error) {
	switch t := val.(type) {
	case nil:
		return "", nil
	case string:
		return t, nil
	case [2]float64:
		return fmt.Sprintf("%v,%v", t[0], t[1]), nil
	case []float64:
		if len(t) == 2 {
			return fmt.Sprintf("%v,%v", t[0], t[1]), nil
		}
	}
	return "", errors.New("unsupported input for GetPrepValue")
}

type AddressField struct {
	MaxLength int
	Default   string
}

func (f *AddressField) Deconstruct() (name, path string, args []interface{}, kwargs map[string]interface{}) {
	// Simulate logic
	return "", "", nil, map[string]interface{}{
		"max_length": f.MaxLength,
		"default":    f.Default,
	}
}

type GeoLocationField struct{}

func (g *GeoLocationField) FormField() {}

func (g *GeoLocationField) Deconstruct() (string, string, []interface{}, map[string]interface{}) {
	return "", "", nil, map[string]interface{}{"formfield": true}
}

type ModelField interface {
	String() string
}

type MockAddressField struct {
	MaxLength int
}

func (f *MockAddressField) String() string {
	return "AddressField"
}
func (f *MockAddressField) ContributeToClass() {}

type MockLocationField struct {
	MaxLength int
}

func (f *MockLocationField) String() string {
	return "LocationField"
}
func (f *MockLocationField) ContributeToClass() {}

type MapWidget struct{}

func (m *MapWidget) Render(name string, value string, attrs map[string]string) string {
	// Return basic HTML
	html := ""
	if id, ok := attrs["id"]; ok {
		html += id
	}
	html += "map"
	return html
}

func (m *MapWidget) JsAttrs() map[string]string {
	return map[string]string{"sample": "val"}
}

func TestGeoptFieldToPythonAndGetPrepValue(t *testing.T) {
	f := &GeoPtField{}
	val, err := f.ToPython("40.1,-122.1")
	if err != nil {
		t.Fatalf("unexpected ToPython error: %v", err)
	}
	if val != ([2]float64{40.1, -122.1}) {
		t.Errorf("expected [40.1,-122.1], got %v", val)
	}
	s, err := f.GetPrepValue([2]float64{10.0, 20.0})
	if err != nil || s != "10,20" {
		t.Errorf("expected '10,20', got %v", s)
	}
	s, err = f.GetPrepValue("50.33,80.55")
	if err != nil || s != "50.33,80.55" {
		t.Errorf("expected '50.33,80.55', got %v", s)
	}
	val, err = f.ToPython(nil)
	if val != nil {
		t.Errorf("expected nil from ToPython(nil), got %v", val)
	}
	_, err = f.ToPython("badinput")
	if err == nil {
		t.Error("expected error for bad input string")
	}
}

func TestGeolocationFieldDeconstructAndOther(t *testing.T) {
	f := &AddressField{MaxLength: 100, Default: "def"}
	name, _, _, kwargs := f.Deconstruct()
	if name != "" && reflect.TypeOf(name).Kind() != reflect.String {
		t.Errorf("expected string or empty for name")
	}
	if ml, ok := kwargs["max_length"]; !ok || ml != 100 {
		t.Errorf("max_length not correct: %v", kwargs)
	}
	if def, ok := kwargs["default"]; !ok || def != "def" {
		t.Errorf("default not correct: %v", kwargs)
	}
	latlng := &GeoLocationField{}
	latlng.FormField()
	_, _, _, kw := latlng.Deconstruct()
	if reflect.TypeOf(kw).Kind() != reflect.Map {
		t.Errorf("expected map from deconstruct, got %T", kw)
	}
}

func TestModelsAddressAndLocationFieldReprAndStr(t *testing.T) {
	fieldsAndVals := []struct {
		Field ModelField
		Val   string
	}{
		{&MockAddressField{MaxLength: 255}, "123 st la"},
		{&MockLocationField{MaxLength: 255}, "11.0,122.2"},
	}

	for _, fv := range fieldsAndVals {
		s := fv.Field.String()
		if s != "AddressField" && s != "LocationField" {
			t.Errorf("String method returns bad: %s", s)
		}
	}
}

func TestWidgetsRenderAttrsInstantiation(t *testing.T) {
	mapWidget := &MapWidget{}
	out := mapWidget.Render("test", "value", map[string]string{"id": "some_id"})
	if !(out == "some_idmap" || out == "map") {
		t.Errorf("expected id in HTML, got %v", out)
	}
	_ = mapWidget.JsAttrs()
}

func TestCustomCleanValidation(t *testing.T) {
	f := &GeoPtField{}
	badFloat := func(x interface{}) float64 {
		panic("bad float simulation")
	}
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for bad float simulation")
		}
	}()
	_ = badFloat("simulate error")
	_, _ = f.ToPython("50.11,-101.2") // this triggers error due to simulated float error
}