package original

import (
	"testing"

	"scastillo_siesta/siesta"
)

func TestFooNotSupportedPrint(t *testing.T) {
	// Just makes sure it runs without panic/exception
	defer func() {
		if r := recover(); r != nil {
			t.Fatalf("FooNotSupported should not panic, recovered: %v", r)
		}
	}()
	siesta.FooNotSupported()
}

func TestAPIInitAndAttr(t *testing.T) {
	api := siesta.NewAPI("http://api.com")
	resource := api.GetResource("books")
	if resource == nil {
		t.Fatalf("resource returned nil")
	}
	if _, ok := api.Resources()["/books"]; !ok {
		t.Errorf("expected '/books' in api.Resources")
	}
	if resource.Uri != "/books" {
		t.Errorf("resource.Uri = %q, want \"/books\"", resource.Uri)
	}
	if resource.API != api {
		t.Error("resource.API != api")
	}
	if s := api.String(); s != "<API http://api.com>" {
		t.Errorf("api.String() = %q, want \"<API http://api.com>\"", s)
	}
	if s := resource.String(); len(s) < 10 || s[:10] != "<Resource " {
		t.Errorf("resource.String() should start with '<Resource ', got %q", s)
	}
}