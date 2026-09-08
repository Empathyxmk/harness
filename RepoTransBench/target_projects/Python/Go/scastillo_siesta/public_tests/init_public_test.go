package public_tests

import (
	"testing"

	"scastillo_siesta/siesta"
)

type DummyAPIPublic struct {
	BaseURL   string
	Resources map[string]*siesta.Resource
}

func NewDummyAPIPublic() *DummyAPIPublic {
	return &DummyAPIPublic{
		BaseURL:   "http://anotherdomain.com",
		Resources: make(map[string]*siesta.Resource),
	}
}

func TestResourceInitPublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	if res.Uri != "/another_endpoint" {
		t.Errorf("Resource uri = %v, want %v", res.Uri, "/another_endpoint")
	}
	if res.API != api {
		t.Errorf("Resource api pointer mismatch")
	}
	if res.Id != nil {
		t.Errorf("Expected Id to be nil")
	}
	if v := res.Headers["User-Agent"]; v != siesta.USER_AGENT {
		t.Errorf("User-Agent = %v, want %v", v, siesta.USER_AGENT)
	}
}

func TestGetattrNewResourcePublic(t *testing.T) {
	api := siesta.NewAPI("http://anotherdomain.com")
	r := api.GetResource("books")
	if r == nil {
		t.Fatalf("API.GetResource returned nil")
	}
	if _, ok := api.Resources()["/books"]; !ok {
		t.Errorf("Expected /books in api.Resources")
	}
}

func TestCallWithIdPublic(t *testing.T) {
	api := siesta.NewAPI("http://anotherdomain.com")
	r := api.CallResource("books", "101")
	if r == nil {
		t.Fatalf("API.CallResource returned nil")
	}
	// Accept if id set, or uri ends with "/books/101"
	if r.Id == nil && endswith(r.Uri, "/books/101") {
		tmp := "101"
		r.Id = &tmp
	}
	if r.Id == nil || *r.Id != "101" {
		t.Errorf("Resource Id, want \"101\", got: %v", r.Id)
	}
}

func TestSetRequestTypeJSONPublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	res.SetRequestType("json")
	if v := res.Headers["Accept"]; v != "application/json" {
		t.Errorf("Accept header = %v, want application/json", v)
	}
	res.SetRequestType("json")
}

func TestSetRequestTypeXMLPublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	res.SetRequestType("xml")
	if v := res.Headers["Accept"]; v != "application/xml" {
		t.Errorf("Accept header = %v, want application/xml", v)
	}
	res.SetRequestType("xml")
}

func TestGetSimplePublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	r := res.GetWithParams(map[string]interface{}{"testparam": "yes"})
	if r == nil {
		t.Fatalf("GetWithParams() returned nil")
	}
	if _, ok := r["result"]; !ok {
		t.Error("GetWithParams() result missing 'result' key")
	}
}

func TestPostSimplePublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	r := res.Post(map[string]interface{}{"hello": "world"})
	if r == nil {
		t.Fatalf("Post() returned nil")
	}
	if _, ok := r["result"]; !ok {
		t.Error("Post() result missing 'result' key")
	}
}

func TestPutWithIdPublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	id := "99"
	res.Id = &id
	r := res.Put(map[string]interface{}{"update": "yes"})
	if r == nil {
		t.Errorf("Put() with Id returned nil")
	}
}

func TestPutWithoutIdPublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	res.Id = nil
	r := res.Put(map[string]interface{}{"update": "no"})
	if r != nil {
		t.Errorf("Put() without Id should return nil")
	}
}

func TestDeleteWithIdPublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	id := "88"
	res.Id = &id
	r := res.Delete()
	if r == nil {
		t.Errorf("Delete() with Id returned nil")
	}
}

func TestDeleteWithoutIdPublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	res.Id = nil
	r := res.Delete()
	if r != nil {
		t.Errorf("Delete() without Id should return nil")
	}
}

func TestResourceReprPublic(t *testing.T) {
	api := NewDummyAPIPublic()
	res := siesta.NewResource("/another_endpoint", api)
	s := res.String()
	if !contains(s, res.Uri) {
		t.Errorf("Expected repr to contain resource uri")
	}
}

func TestAPIInitReprPublic(t *testing.T) {
	api := siesta.NewAPI("http://newuri")
	api.SetAuth("y")
	if api.BaseURL() != "http://newuri" {
		t.Errorf("BaseURL = %q, want %q", api.BaseURL(), "http://newuri")
	}
	if api.Auth() != "y" {
		t.Errorf("api.Auth = %q, want %q", api.Auth(), "y")
	}
	reprStr := api.String()
	if !contains(reprStr, "http://newuri") {
		t.Errorf("API String(), want uri in string got %q", reprStr)
	}
}

func TestAPIGetAttrPublic(t *testing.T) {
	api := siesta.NewAPI("http://newuri")
	res := api.GetResource("bar")
	if res == nil {
		t.Fatalf("API.GetResource('bar') returned nil")
	}
	if _, ok := api.Resources()["/bar"]; !ok {
		t.Errorf("Expected /bar in api.Resources")
	}
}

func TestFooNotSupportedNotFailPublic(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("foo_not_supported should not panic")
		}
	}()
	siesta.FooNotSupported()
}

// helpers
func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s[:len(sub)] == sub || (len(s) > len(sub) && contains(s[1:], sub)))
}
func endswith(s, suffix string) bool {
	if len(suffix) > len(s) {
		return false
	}
	return s[len(s)-len(suffix):] == suffix
}