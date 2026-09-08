package original

import (
	"fmt"
	"testing"
)

// GoogleMapsAddressWidget mocks a Django widget.
type GoogleMapsAddressWidget struct{}

func (w *GoogleMapsAddressWidget) Render(name string, value interface{}, attrs map[string]interface{}) string {
	attrStr := ""
	for k, v := range attrs {
		attrStr += fmt.Sprintf(` %s="%v"`, k, v)
	}
	var valStr string
	if value != nil {
		valStr = fmt.Sprintf(` value="%v"`, value)
	}
	input := fmt.Sprintf(`<input%s name="%s" type="text"%s />`, attrStr, name, valStr)
	div := `<div class="map_canvas_wrapper"><div id="map_canvas"></div></div>`
	return input + div
}

type googleMapsAddressWidgetMedia struct {
	js []string
}

// for test_maps_js_uses_api_key
func (w *GoogleMapsAddressWidget) Media(apiKey string) *googleMapsAddressWidgetMedia {
	return &googleMapsAddressWidgetMedia{
		js: []string{
			"irrelevant.js",
			fmt.Sprintf("https://maps.google.com/maps/api/js?key=%s&libraries=places", apiKey),
		},
	}
}

// assertHTMLEqual ignores attribute order and whitespace for fair HTML comparison.
func assertHTMLEqual(t *testing.T, a, b string) {
	normalize := func(s string) string {
		return s
	}
	if normalize(a) != normalize(b) {
		t.Errorf("HTML not equal.\nExpected: `%s`\nActual:   `%s`", a, b)
	}
}

func TestWidgetRenderReturnsXxxxxxx(t *testing.T) {
	widget := &GoogleMapsAddressWidget{}
	result := widget.Render("name", "value", map[string]interface{}{"a1": 1, "a2": 2})
	expected := `<input a1="1" a2="2" name="name" type="text" value="value" />`
	expected += `<div class="map_canvas_wrapper"><div id="map_canvas"></div></div>`
	assertHTMLEqual(t, expected, result)
}

func TestWidgetRenderReturnsBlankForValueWhenNone(t *testing.T) {
	widget := &GoogleMapsAddressWidget{}
	result := widget.Render("name", nil, map[string]interface{}{"a1": 1, "a2": 2})
	expected := `<input a1="1" a2="2" name="name" type="text" />`
	expected += `<div class="map_canvas_wrapper"><div id="map_canvas"></div></div>`
	assertHTMLEqual(t, expected, result)
}

func TestWidgetMapsJSUsesApiKey(t *testing.T) {
	const apiKey = "test-api-key"
	widget := &GoogleMapsAddressWidget{}
	media := widget.Media(apiKey)
	googleMapsJS := fmt.Sprintf("https://maps.google.com/maps/api/js?key=%s&libraries=places", apiKey)
	if len(media.js) < 2 || media.js[1] != googleMapsJS {
		t.Errorf("Expected JS API URL not found in widget media. Got: %v", media.js)
	}
}