package public_tests

import (
	"reflect"
	"testing"

	"scastillo_siesta/siesta"
)

type DummyRequestPublic struct {
	Headers map[string]string
}

func NewDummyRequestPublic() *DummyRequestPublic {
	return &DummyRequestPublic{Headers: make(map[string]string)}
}

func (r *DummyRequestPublic) SetHeader(key, value string) {
	r.Headers[key] = value
}

func (r *DummyRequestPublic) GetHeaders() map[string]string {
	return r.Headers
}

func TestBasicAuthPublic(t *testing.T) {
	a := siesta.NewBasicAuth("alice", "wonderland")
	hdrs := a.GenerateHeaders()
	val, ok := hdrs["Authorization"]
	if !ok {
		t.Errorf("Authorization header not present in generated headers")
	}
	if len(val) < len("Basic ") || val[:6] != "Basic " {
		t.Errorf("Expected Authorization to start with 'Basic ', got %v", val)
	}
}

func TestCallSetsHeadersPublic(t *testing.T) {
	a := siesta.NewBasicAuth("alice", "wonderland")
	req := NewDummyRequestPublic()
	a.Attach(req)
	if _, ok := req.Headers["Authorization"]; !ok {
		t.Errorf("Expected Authorization header set in DummyRequest after attach")
	}
}

func TestReprBasicAuthPublic(t *testing.T) {
	ba := siesta.NewBasicAuth("someone", "secret")
	rep := ba.String()
	if !(len(rep) >= 8 && rep[:8] == "BasicAuth") && !contains(rep, "BasicAuth") {
		t.Errorf("Expected repr to contain 'BasicAuth', got: %q", rep)
	}
}

func TestBearerTokenPublic(t *testing.T) {
	bt := siesta.NewBearerToken("publictoken456")
	hdrs := bt.GenerateHeaders()
	if val, ok := hdrs["Authorization"]; !ok || val != "Bearer publictoken456" {
		t.Errorf("Expected Authorization header 'Bearer publictoken456', got %v", val)
	}
	req := NewDummyRequestPublic()
	bt.Attach(req)
	if _, ok := req.Headers["Authorization"]; !ok {
		t.Errorf("Expected Authorization header in request after attach")
	}
}

func TestReprBearerTokenPublic(t *testing.T) {
	bt := siesta.NewBearerToken("pubtoken")
	rep := bt.String()
	if !contains(rep, "BearerToken") {
		t.Errorf("Expected repr to contain 'BearerToken', got: %v", rep)
	}
}

func TestAPIKeyHeaderOnlyPublic(t *testing.T) {
	ak := siesta.NewApiKey("pubkey", "pubval", true)
	hdrs := ak.GenerateHeaders()
	if _, ok := hdrs["pubkey"]; !ok {
		t.Errorf("ApiKey in header mode should set key in headers")
	}
	req := NewDummyRequestPublic()
	ak.Attach(req)
	if _, ok := req.Headers["pubkey"]; !ok {
		t.Errorf("ApiKey attach should set header key in request")
	}
}

func TestAPIKeyInQueryNotSupportedPublic(t *testing.T) {
	ak := siesta.NewApiKey("querykey", "queryval", false)
	hdrs := ak.GenerateHeaders()
	if len(hdrs) != 0 || !reflect.DeepEqual(hdrs, map[string]string{}) {
		t.Errorf("ApiKey with in_header=false should return empty header map")
	}
}

func TestReprApiKeyPublic(t *testing.T) {
	ak := siesta.NewApiKey("pubapi", "pubvalue", true)
	rep := ak.String()
	if !contains(rep, "ApiKey") {
		t.Errorf("Expected repr to contain 'ApiKey', got: %v", rep)
	}
}

func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s[:len(sub)] == sub || (len(s) > len(sub) && contains(s[1:], sub)))
}