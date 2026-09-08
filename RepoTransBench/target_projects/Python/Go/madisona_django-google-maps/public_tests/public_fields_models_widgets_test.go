package public_tests

import (
	"errors"
	"fmt"
	"testing"
)

func TestGeoptFieldToPythonAndGetPrepValuePublic(t *testing.T) {
	type FakeGeoPtField struct{}
	var f FakeGeoPtField
	toPython := func(value interface{}) (interface{}, error) {
		switch typ := value.(type) {
		case nil:
			return nil, nil
		case string:
			var lat, lon float64
			n, err := fmt.Sscanf(typ, "%f,%f", &lat, &lon)
			if err != nil || n != 2 {
				return nil, errors.New("invalid value for GeoPtField")
			}
			return [2]float64{lat, lon}, nil
		case [2]float64:
			return typ, nil
		default:
			return nil, errors.New("invalid value for GeoPtField")
		}
	}
	getPrepValue := func(value interface{}) (string, error) {
		switch typ := value.(type) {
		case nil:
			return "", nil
		case string:
			return typ, nil
		case [2]float64:
			return fmt.Sprintf("%.8f,%.8f", typ[0], typ[1]), nil
		default:
			return "", errors.New("invalid value for GeoPtField")
		}
	}

	rawVal := "1.111,-2.222"
	pyVal, err := toPython(rawVal)
	if err != nil || pyVal != ([2]float64{1.111, -2.222}) {
		t.Errorf("expected [1.111,-2.222], got %v error %v", pyVal, err)
	}
	s, err := getPrepValue([2]float64{3.333, -4.444})
	if err != nil || s != "3.33300000,-4.44400000" {
		t.Errorf("expected '3.33300000,-4.44400000', got %s err=%v", s, err)
	}
}

func TestModelsAddressAndLocationFieldReprAndStrPublic(t *testing.T) {
	type DummyAddressField struct {
		MaxLength int
	}
	type DummyLocationField struct {
		MaxLength int
	}
	(fieldsAndVals := []struct {
		Field interface{}
		Val   string
	}{
		{DummyAddressField{150}, "456 road ave"},
		{DummyLocationField{150}, "85.63,-172.54"},
	})
	for _, fv := range fieldsAndVals {
		_ = fmt.Sprintf("%v", fv.Field)
		_ = fmt.Sprintf("%#v", fv.Field)
	}
}

func TestWidgetsRenderAttrsInstantiationPublic(t *testing.T) {
	type DummyMapWidget struct {
		Attrs map[string]string
	}
	var mapWidget = DummyMapWidget{Attrs: map[string]string{"placeholder": "Enter city"}}
	render := func(name, value string, attrs map[string]string) string {
		return fmt.Sprintf(`<input type="text" name="%s" value="%s" %v>`, name, value, attrs)
	}
	html := render("sample_location", "21.44,13.33", map[string]string{"id": "map-field"})
	if !(contains(html, "sample_location") && contains(html, "21.44,13.33") && contains(html, "id")) {
		t.Errorf("expected input fields in html, got: %s", html)
	}
	if contains(html, "placeholder") {
		t.Errorf("unexpected 'placeholder' found in output")
	}
}

func contains(haystack, needle string) bool {
	return len(haystack) >= len(needle) && (haystack == needle || contains(haystack[1:], needle))
}

func TestCustomCleanValidationPublic(t *testing.T) {
	type DummyGeoPtField struct{}
	clean := func(value interface{}) (interface{}, error) {
		switch typ := value.(type) {
		case [2]float64:
			return typ, nil
		case string:
			var lat, lon float64
			n, err := fmt.Sscanf(typ, "%f,%f", &lat, &lon)
			if n != 2 || err != nil {
				return nil, errors.New("bad value")
			}
			return [2]float64{lat, lon}, nil
		default:
			return nil, errors.New("bad value")
		}
	}
	// Valid value
	v, err := clean([2]float64{12.34, -56.78})
	if err != nil || v != ([2]float64{12.34, -56.78}) {
		t.Errorf("expected (12.34,-56.78), got %v err=%v", v, err)
	}
	// Valid value as string
	v, err = clean("0.987,-0.654")
	if err != nil || v != ([2]float64{0.987, -0.654}) {
		t.Errorf("expected (0.987,-0.654), got %v err=%v", v, err)
	}
	_, err = clean("notacoord")
	if err == nil {
		t.Error("expected error for non-coord string")
	}
	_, err = clean([1]float64{1.2})
	if err == nil {
		t.Error("expected error for single-element tuple")
	}
}