package public_tests

import (
	"fmt"
	"testing"
)

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

type widgetMedia struct{ js []string }

func (w *GoogleMapsAddressWidget) Media(apiKey string) *widgetMedia {
	return &widgetMedia{
		js: []string{
			"foo.js",
			fmt.Sprintf("https://maps.google.com/maps/api/js?key=%s&libraries=places", apiKey),
		},
	}
}

func assertHTMLEqual(t *testing.T, a, b string) {
	normalize := func(s string) string { return s }
	if normalize(a) != normalize(b) {
		t.Errorf("HTML not equal.\nExpected: `%s`\nActual:   `%s`", a, b)
	}
}

func TestRenderReturnsCustomHTML(t *testing.T) {
	widget := &GoogleMapsAddressWidget{}
	result := widget.Render("adam", "customvalue", map[string]interface{}{"id": "unique", "class": "css-test"})
	expected := `<input id="unique" class="css-test" name="adam" type="text" value="customvalue" />`
	expected += `<div class="map_canvas_wrapper"><div id="map_canvas"></div></div>`
	assertHTMLEqual(t, expected, result)
}

func TestRenderReturnsBlankForValueWhenNonePublic(t *testing.T) {
	widget := &GoogleMapsAddressWidget{}
	result := widget.Render("foo", nil, map[string]interface{}{"style": "color:red;", "data-bar": "hello"})
	expected := `<input style="color:red;" data-bar="hello" name="foo" type="text" />`
	expected += `<div class="map_canvas_wrapper"><div id="map_canvas"></div></div>`
	assertHTMLEqual(t, expected, result)
}

func TestMapsJSApiKeyDifferent(t *testing.T) {
	apiKey := "public-api-key"
	widget := &GoogleMapsAddressWidget{}
	media := widget.Media(apiKey)
	googleMapsJS := fmt.Sprintf("https://maps.google.com/maps/api/js?key=%s&libraries=places", apiKey)
	if len(media.js) < 2 || media.js[1] != googleMapsJS {
		t.Errorf("Expected JS API URL not found in widget media. Got: %v", media.js)
	}
}