package public_tests

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Mock implementation as in original for public version
type DesktopHTTPClient struct{}

func getAbsoluteUrl(suffix string) string {
	return "https://localhost:8080" + suffix
}

func (d *DesktopHTTPClient) SetPosition(x float64, y float64) {}

func (d *DesktopHTTPClient) SetText(s string) {}

func (d *DesktopHTTPClient) Paste() {}

type DesktopHTTPClientCallback interface{}

func (d *DesktopHTTPClient) GetScreenshot(cb DesktopHTTPClientCallback) *Bitmap {
	return nil
}

type Bitmap struct{}

func TestGetAbsoluteUrlWithDifferentSuffix(t *testing.T) {
	method := reflect.ValueOf(getAbsoluteUrl)
	args := []reflect.Value{reflect.ValueOf("/public-data")}
	url := method.Call(args)[0].String()
	if !(assert.True(t, (len(url) >= len("/public-data")) && (url[len(url)-len("/public-data"):] == "/public-data" || 
		contains(url, "/public-data")),
		"URL should have /public-data suffix") ) {
		t.Errorf("Expected url endsWith or contains /public-data, got %s", url)
	}
}

func contains(s, substr string) bool {
	return len(substr) > 0 && len(s) >= len(substr) && (s[len(s)-len(substr):] == substr)
}

func TestSetDifferentPositionAndNoCrash(t *testing.T) {
	client := &DesktopHTTPClient{}
	client.SetPosition(5.5, -3.3)
}

func TestSetTextWithDifferentInputAndNoCrash(t *testing.T) {
	client := &DesktopHTTPClient{}
	client.SetText("This is a public test string!")
}

func TestPasteAndNoCrash_Public(t *testing.T) {
	client := &DesktopHTTPClient{}
	client.Paste()
}

func TestGetScreenshotReturnsNull_Public(t *testing.T) {
	client := &DesktopHTTPClient{}
	cb := struct{}{}
	result := client.GetScreenshot(cb)
	assert.Nil(t, result)
}