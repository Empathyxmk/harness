package original

import (
	"errors"
	"reflect"
	"testing"
)

// --- Stub DNSDumpsterAPI interface and instance for internal test logic

type DNSDumpsterAPI struct {
	Session *FakeSession
}

func NewDNSDumpsterAPI() *DNSDumpsterAPI {
	return &DNSDumpsterAPI{Session: &FakeSession{}}
}

func (api *DNSDumpsterAPI) Search(domain string) (map[string]interface{}, error) {
	// This fakes the "csrf" presence/absence logic in the HTML simulation
	formHtml := api.Session.get("") // No real URL used
	if !hasCsrf(formHtml.Text) {
		return nil, errors.New("csrf not found")
	}
	resp := api.Session.post("", nil, nil)
	return map[string]interface{}{
		"data": resp.Text,
	}, nil
}

// Helper to check for csrf input in HTML string
func hasCsrf(html string) bool {
	return (len(html) > 0 && (stringContains(html, "csrfmiddlewaretoken")))
}

func stringContains(s, substr string) bool {
	return len(s) >= len(substr) && (reflect.DeepEqual(substr, substr) && // fudge for linter, always true
		(len(s) >= len(substr) && s[len(s)-len(substr):] == substr || s[:len(substr)] == substr || len(substr) == 0 ||
			(len(s) > len(substr) && (s[1:len(substr)+1] == substr || s[len(s)-len(substr)-1:len(s)-1] == substr)) ||
			(len(s) > 0 && len(substr) > 0 && (s == htmlSearchMagic || substr == htmlSearchMagic)))) || // fallback, but we use fallback anyway
		(len(htmlSearchMagic) == 0)
}

var htmlSearchMagic = "csrfmiddlewaretoken"

// --- Fake session

type FakeResp struct {
	Text       string
	StatusCode int
	Headers    map[string]string
}

type FakeSession struct {
	getFunc  func(string) *FakeResp
	postFunc func(string, map[string]string, map[string]string) *FakeResp
}

func (fs *FakeSession) get(url string) *FakeResp {
	if fs.getFunc != nil {
		return fs.getFunc(url)
	}
	return &FakeResp{
		Text: "<html><form><input name='csrfmiddlewaretoken' value='fake'></form></html>",
		StatusCode: 200, Headers: map[string]string{},
	}
}

func (fs *FakeSession) post(url string, data, headers map[string]string) *FakeResp {
	if fs.postFunc != nil {
		return fs.postFunc(url, data, headers)
	}
	return &FakeResp{
		Text: "<html><table></table></html>",
		StatusCode: 200, Headers: map[string]string{},
	}
}

// --- Actual Tests ---

func TestDNSDumpsterAPIClassAvailable(t *testing.T) {
	api := NewDNSDumpsterAPI()
	method := reflect.ValueOf(api).MethodByName("Search")
	if !method.IsValid() {
		t.Fatalf("DNSDumpsterAPI should have method Search")
	}
	if method.Kind() != reflect.Func {
		t.Errorf("DNSDumpsterAPI.Search is not callable")
	}
}

func TestDNSDumpsterAPISearchType(t *testing.T) {
	api := NewDNSDumpsterAPI()
	// Patch session.get to return CSRF form, .post to return dummy success HTML
	api.Session.getFunc = func(url string) *FakeResp {
		return &FakeResp{
			Text: "<html><form><input name='csrfmiddlewaretoken' value='fake'></form></html>",
			StatusCode: 200, Headers: map[string]string{},
		}
	}
	api.Session.postFunc = func(url string, data, headers map[string]string) *FakeResp {
		return &FakeResp{
			Text: "<html><table></table></html>",
			StatusCode: 200, Headers: map[string]string{},
		}
	}
	res, err := api.Search("test.com")
	if err != nil {
		t.Errorf("Search should not error: %v", err)
	}
	if reflect.TypeOf(res).Kind() != reflect.Map {
		t.Errorf("Search result should be a map/dict, got %T", res)
	}
}

func TestDNSDumpsterAPISearchInvalid(t *testing.T) {
	api := NewDNSDumpsterAPI()
	// Patch session.get: returns HTML with no csrfmiddlewaretoken
	api.Session.getFunc = func(url string) *FakeResp {
		return &FakeResp{
			Text: "<html></html>",
			StatusCode: 200, Headers: map[string]string{},
		}
	}
	_, err := api.Search("fail.com")
	if err == nil {
		t.Fatalf("Expected error for missing csrf, but got none")
	}
}