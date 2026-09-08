package original

import (
	"testing"
	"TypeError_secure/secure"
)

func TestSecureWithNoHeaders(t *testing.T) {
	s := secure.NewSecure()
	if len(s.HeadersList()) != 0 {
		t.Errorf("Expected no headers, got %v", s.HeadersList())
	}
}

func TestSecureWithSomeHeaders(t *testing.T) {
	c := secure.NewCacheControl().NoStore()
	s := secure.NewSecureWithCache(c)
	if len(s.HeadersList()) == 0 || s.HeadersList()[0] != c {
		t.Errorf("Expected the first header to be CacheControl instance")
	}
}

func TestSecureWithCustomList(t *testing.T) {
	ch1 := secure.NewCustomHeader("X-Test", "A")
	ch2 := secure.NewCustomHeader("X-Foo", "Bar")
	s := secure.NewSecureWithCustom([]*secure.CustomHeader{ch1, ch2})
	found1 := false
	found2 := false
	for _, h := range s.HeadersList() {
		if h == ch1 {
			found1 = true
		}
		if h == ch2 {
			found2 = true
		}
	}
	if !found1 || !found2 {
		t.Errorf("Custom headers not found in HeadersList: got %v", s.HeadersList())
	}
}

func TestSecureWithAllHeaders(t *testing.T) {
	s := secure.NewSecureFull(
		secure.NewCacheControl().NoStore(),
		secure.NewCrossOriginOpenerPolicy().SameOrigin(),
		secure.NewContentSecurityPolicy().DefaultSrc("'none'"),
		secure.NewStrictTransportSecurity().MaxAge(3600),
		secure.NewPermissionsPolicy().Camera(),
		secure.NewReferrerPolicy().StrictOriginWhenCrossOrigin(),
		secure.NewServer().Set("test"),
		secure.NewXContentTypeOptions().Nosniff(),
		secure.NewXFrameOptions().Deny(),
		[]*secure.CustomHeader{secure.NewCustomHeader("X-A", "B")},
	)
	foundCustom := false
	for _, h := range s.HeadersList() {
		if _, ok := h.(*secure.CustomHeader); ok {
			foundCustom = true
			break
		}
	}
	if !foundCustom {
		t.Errorf("Expected at least one CustomHeader present")
	}
}

func TestSecureWithDefaultHeaders(t *testing.T) {
	s := secure.SecureWithDefaultHeaders()
	names := []string{}
	for _, h := range s.HeadersList() {
		names = append(names, h.HeaderTypeName())
	}
	expectedTypes := map[string]bool{
		"CacheControl":             true,
		"CrossOriginOpenerPolicy":  true,
		"ContentSecurityPolicy":    true,
		"StrictTransportSecurity":  true,
		"PermissionsPolicy":        true,
		"ReferrerPolicy":           true,
		"Server":                   true,
		"XContentTypeOptions":      true,
		"XFrameOptions":            true,
	}
	for tp := range expectedTypes {
		found := false
		for _, name := range names {
			if name == tp {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("Expected header of type %v in default headers, got %v", tp, names)
		}
	}
}