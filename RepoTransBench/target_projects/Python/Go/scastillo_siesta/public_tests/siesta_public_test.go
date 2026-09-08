package public_tests

import (
	"testing"

	"scastillo_siesta/siesta"
)

func TestFooNotSupportedPrintPublic(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Fatalf("FooNotSupported should not panic, recovered: %v", r)
		}
	}()
	siesta.FooNotSupported()
}

func TestAPIInitAndAttrPublic(t *testing.T) {
	api := siesta.NewAPI("http://publicapi.org")
	resource := api.GetResource("users")
	if resource == nil {
		t.Fatalf("resource returned nil")
	}
	if _, ok := api.Resources()["/users"]; !ok {
		t.Errorf("expected '/users' in api.Resources")
	}
	if resource.Uri != "/users" {
		t.Errorf("resource.Uri = %q, want \"/users\"", resource.Uri)
	}
	if resource.API != api {
		t.Error("resource.API != api")
	}
	if s := api.String(); s != "<API http://publicapi.org>" {
		t.Errorf("api.String() = %q, want \"<API http://publicapi.org>\"", s)
	}
	if s := resource.String(); len(s) < 10 || s[:10] != "<Resource " {
		t.Errorf("resource.String() should start with '<Resource ', got %q", s)
	}
}