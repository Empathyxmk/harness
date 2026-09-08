package original

import (
	"reflect"
	"testing"

	"scastillo_siesta/siesta"
)

type DummyRequest struct {
	Headers map[string]string
}

func NewDummyRequest() *DummyRequest {
	return &DummyRequest{Headers: make(map[string]string)}
}

func (r *DummyRequest) SetHeader(key, value string) {
	r.Headers[key] = value
}

func (r *DummyRequest) GetHeaders() map[string]string {
	return r.Headers
}

func TestBasicAuth(t *testing.T) {
	a := siesta.NewBasicAuth("foo", "bar")
	hdrs := a.GenerateHeaders()
	val, ok := hdrs["Authorization"]
	if !ok {
		t.Errorf("Authorization header not present in generated headers")
	}
	if len(val) < len("Basic ") || val[:6] != "Basic " {
		t.Errorf("Expected Authorization to start with 'Basic ', got %v", val)
	}
}

func TestCallSetsHeaders(t *testing.T) {
	a := siesta.NewBasicAuth("foo", "bar")
	req := NewDummyRequest()
	a.Attach(req)
	if _, ok := req.Headers["Authorization"]; !ok {
		t.Errorf("Expected Authorization header set in DummyRequest after attach")
	}
}

func TestReprBasicAuth(t *testing.T) {
	ba := siesta.NewBasicAuth("username", "pw")
	rep := ba.String()
	if found := (len(rep) >= 8 && rep[:8] == "BasicAuth"); !found && !contains(rep, "BasicAuth") {
		t.Errorf("Expected repr to contain 'BasicAuth', got: %q", rep)
	}
}

func TestBearerToken(t *testing.T) {
	bt := siesta.NewBearerToken("tok123")
	hdrs := bt.GenerateHeaders()
	if val, ok := hdrs["Authorization"]; !ok || val != "Bearer tok123" {
		t.Errorf("Expected Authorization header 'Bearer tok123', got %v", val)
	}
	req := NewDummyRequest()
	bt.Attach(req)
	if _, ok := req.Headers["Authorization"]; !ok {
		t.Errorf("Expected Authorization header in request after attach")
	}
}

func TestReprBearerToken(t *testing.T) {
	bt := siesta.NewBearerToken("tk")
	rep := bt.String()
	if !contains(rep, "BearerToken") {
		t.Errorf("Expected repr to contain 'BearerToken', got: %v", rep)
	}
}

func TestAPIKeyHeaderOnly(t *testing.T) {
	ak := siesta.NewApiKey("mykey", "myval", true)
	hdrs := ak.GenerateHeaders()
	if _, ok := hdrs["mykey"]; !ok {
		t.Errorf("ApiKey in header mode should set key in headers")
	}
	req := NewDummyRequest()
	ak.Attach(req)
	if _, ok := req.Headers["mykey"]; !ok {
		t.Errorf("ApiKey attach should set header key in request")
	}
}

func TestAPIKeyInQueryNotSupported(t *testing.T) {
	ak := siesta.NewApiKey("qkey", "qval", false)
	hdrs := ak.GenerateHeaders()
	if len(hdrs) != 0 || !reflect.DeepEqual(hdrs, map[string]string{}) {
		t.Errorf("ApiKey with in_header=false should return empty header map")
	}
}

func TestReprApiKey(t *testing.T) {
	ak := siesta.NewApiKey("api", "value", true)
	rep := ak.String()
	if !contains(rep, "ApiKey") {
		t.Errorf("Expected repr to contain 'ApiKey', got: %v", rep)
	}
}

// Go lacks python's "in" operator, so define our own
func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s[:len(sub)] == sub || (len(s) > len(sub) && contains(s[1:], sub)))
}