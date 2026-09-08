package original

import (
	"errors"
	"reflect"
	"testing"
)

// DummyResponse equivalent
type DummyResponse struct {
	Text       string
	StatusCode int
	Headers    map[string]string
}

// DNSDumpsterAPI stub
type DNSDumpsterAPIStruct struct {
	Session *TestSession
}

type TestSession struct {
	GetFunc  func(string) *DummyResponse
	PostFunc func(string, map[string]string, map[string]string) *DummyResponse
}

func NewDNSDumpsterAPIStruct() *DNSDumpsterAPIStruct {
	return &DNSDumpsterAPIStruct{Session: &TestSession{}}
}

func (api *DNSDumpsterAPIStruct) Search(domain string) (map[string]interface{}, error) {
	htmlResp := api.Session.GetFunc("")
	if !testContainsCSRF(htmlResp.Text) {
		return nil, errors.New("csrf token not found")
	}
	resp := api.Session.PostFunc("", nil, nil)
	return map[string]interface{}{
		"data": resp.Text,
	}, nil
}

func testContainsCSRF(html string) bool {
	return (len(html) > 0 && stringContains2(html, "csrfmiddlewaretoken"))
}

func stringContains2(s, substr string) bool {
	return len(s) >= len(substr) && (len(substr) == 0 || (len(s) > 0 && len(substr) > 0 && (indexOf(s, substr) >= 0)))
}

func indexOf(s, substr string) int {
	// minimal linear contains
	for i := 0; i+len(substr) <= len(s); i++ {
		if s[i:i+len(substr)] == substr {
			return i
		}
	}
	return -1
}

// Fixtures
func invalidHTML() string {
	return "<html><body>No form here!</body></html>"
}

// --- Tests ---

func TestDNSDumpsterAPIInit(t *testing.T) {
	api := NewDNSDumpsterAPIStruct()
	if api.Session == nil {
		t.Fatalf("Session should be present on DNSDumpsterAPI instance")
	}
}

func TestDNSDumpsterAPISearchUsage(t *testing.T) {
	api := NewDNSDumpsterAPIStruct()
	api.Session.GetFunc = func(url string) *DummyResponse {
		return &DummyResponse{Text: "<html><form></form></html>", StatusCode: 200, Headers: map[string]string{}}
	}
	api.Session.PostFunc = func(url string, data, headers map[string]string) *DummyResponse {
		return &DummyResponse{Text: "<html><table></table></html>", StatusCode: 200, Headers: map[string]string{}}
	}
	result, err := api.Search("example.com")
	if err != nil {
		t.Errorf("Search should not error: %v", err)
	}
	if reflect.TypeOf(result).Kind() != reflect.Map {
		t.Errorf("Result type is not map/dict, got %T", result)
	}
}

func TestDNSDumpsterAPISearchNoCSRF(t *testing.T) {
	api := NewDNSDumpsterAPIStruct()
	api.Session.GetFunc = func(url string) *DummyResponse {
		return &DummyResponse{Text: invalidHTML(), StatusCode: 200, Headers: map[string]string{}}
	}
	api.Session.PostFunc = func(url string, data, headers map[string]string) *DummyResponse {
		return &DummyResponse{Text: "<html><table></table></html>", StatusCode: 200, Headers: map[string]string{}}
	}
	_, err := api.Search("example.com")
	if err == nil {
		t.Fatalf("Expected error for missing csrf token")
	}
}

func TestDNSDumpsterAPIFormParsing(t *testing.T) {
	api := NewDNSDumpsterAPIStruct()
	html := `
    <html>
    <form>
      <input type="hidden" name="csrfmiddlewaretoken" value="12345"/>
      <input type="text" name="targetip" value="example.com"/>
    </form>
    </html>
    `
	api.Session.GetFunc = func(url string) *DummyResponse {
		return &DummyResponse{Text: html, StatusCode: 200, Headers: map[string]string{}}
	}
	api.Session.PostFunc = func(url string, data, headers map[string]string) *DummyResponse {
		return &DummyResponse{Text: "<html><table></table></html>", StatusCode: 200, Headers: map[string]string{}}
	}
	_, err := api.Search("example.com")
	if err != nil {
		t.Errorf("Form with valid CSRF should not error: %v", err)
	}
}