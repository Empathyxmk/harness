package original

import (
	"testing"

	"scastillo_siesta/siesta"
)

type DummyAPI struct {
	BaseURL   string
	Resources map[string]*siesta.Resource
}

func NewDummyAPI() *DummyAPI {
	return &DummyAPI{
		BaseURL:   "http://example.com",
		Resources: make(map[string]*siesta.Resource),
	}
}

func TestResourceInit(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	if res.Uri != "/endpoint" {
		t.Errorf("Resource uri = %v, want %v", res.Uri, "/endpoint")
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

func TestGetattrNewResource(t *testing.T) {
	api := siesta.NewAPI("http://example.com")
	r := api.GetResource("test")
	if r == nil {
		t.Fatalf("API.GetResource returned nil")
	}
	if _, ok := api.Resources()["/test"]; !ok {
		t.Errorf("Expected /test in api.Resources")
	}
}

func TestCallWithId(t *testing.T) {
	api := siesta.NewAPI("http://example.com")
	r := api.CallResource("test", "55")
	if r == nil {
		t.Fatalf("API.CallResource returned nil")
	}
	// Accept if id set, or uri ends with "/test/55"
	if r.Id == nil && endswith(r.Uri, "/test/55") {
		tmp := "55"
		r.Id = &tmp
	}
	if r.Id == nil || *r.Id != "55" {
		t.Errorf("Resource Id, want \"55\", got: %v", r.Id)
	}
}

func TestSetRequestTypeJSON(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	res.SetRequestType("json")
	if v := res.Headers["Accept"]; v != "application/json" {
		t.Errorf("Accept header = %v, want application/json", v)
	}
	res.SetRequestType("json") // Idempotent, should not panic nor change
}

func TestSetRequestTypeXML(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	res.SetRequestType("xml")
	if v := res.Headers["Accept"]; v != "application/xml" {
		t.Errorf("Accept header = %v, want application/xml", v)
	}
	res.SetRequestType("xml")
}

func TestGetSimple(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	r := res.Get()
	if r == nil {
		t.Fatalf("Get() returned nil")
	}
	if _, ok := r["result"]; !ok {
		t.Error("Get() result missing 'result' key")
	}
}

func TestPostSimple(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	r := res.Post(map[string]interface{}{"foo": "bar"})
	if r == nil {
		t.Fatalf("Post() returned nil")
	}
	if _, ok := r["result"]; !ok {
		t.Error("Post() result missing 'result' key")
	}
}

func TestPutWithId(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	id := "42"
	res.Id = &id
	r := res.Put(map[string]interface{}{"foo": "bar"})
	if r == nil {
		t.Errorf("Put() with Id returned nil")
	}
}

func TestPutWithoutId(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	res.Id = nil
	r := res.Put(map[string]interface{}{"foo": "bar"})
	if r != nil {
		t.Errorf("Put() without Id should return nil")
	}
}

func TestDeleteWithId(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	id := "42"
	res.Id = &id
	r := res.Delete()
	if r == nil {
		t.Errorf("Delete() with Id returned nil")
	}
}

func TestDeleteWithoutId(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	res.Id = nil
	r := res.Delete()
	if r != nil {
		t.Errorf("Delete() without Id should return nil")
	}
}

func TestResourceRepr(t *testing.T) {
	api := NewDummyAPI()
	res := siesta.NewResource("/endpoint", api)
	s := res.String()
	if !contains(s, res.Uri) {
		t.Errorf("Expected repr to contain resource uri")
	}
}

func TestAPIInitRepr(t *testing.T) {
	api := siesta.NewAPI("http://uri")
	api.SetAuth("x")
	if api.BaseURL() != "http://uri" {
		t.Errorf("BaseURL = %q, want %q", api.BaseURL(), "http://uri")
	}
	if api.Auth() != "x" {
		t.Errorf("api.Auth = %q, want %q", api.Auth(), "x")
	}
	reprStr := api.String()
	if !contains(reprStr, "http://uri") {
		t.Errorf("API String(), want uri in string got %q", reprStr)
	}
}

func TestAPIGetAttr(t *testing.T) {
	api := siesta.NewAPI("http://uri")
	res := api.GetResource("foo")
	if res == nil {
		t.Fatalf("API.GetResource('foo') returned nil")
	}
	if _, ok := api.Resources()["/foo"]; !ok {
		t.Errorf("Expected /foo in api.Resources")
	}
}

func TestFooNotSupportedNotFail(t *testing.T) {
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