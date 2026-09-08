package public_tests

import (
	"TypeError_secure/secure"
	"testing"
)

func TestSecureWithNoCustomHeadersPublic(t *testing.T) {
	s := secure.NewSecure()
	if len(s.HeadersList()) != 0 {
		t.Errorf("Expected no headers, got %v", s.HeadersList())
	}
}

func TestSecureWithOneHeaderPublic(t *testing.T) {
	c := secure.NewCacheControl().MaxAge(1234)
	s := secure.NewSecureWithCache(c)
	if len(s.HeadersList()) == 0 || s.HeadersList()[0] != c {
		t.Errorf("Expected the first header to be CacheControl")
	}
}

func TestSecureWithMultipleCustomHeadersPublic(t *testing.T) {
	ch1 := secure.NewCustomHeader("X-Public-Header", "Val1")
	ch2 := secure.NewCustomHeader("X-Diff-Header", "DiffVal")
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

func TestSecureWithVariousHeadersPublic(t *testing.T) {
	s := secure.NewSecureVaried(
		secure.NewCacheControl().MaxAge(500),
		nil,
		secure.NewCrossOriginEmbedderPolicy().RequireCorp(),
		secure.NewContentSecurityPolicy().DefaultSrc("'self'"),
		secure.NewStrictTransportSecurity().MaxAge(1800),
		secure.NewPermissionsPolicy().Microphone(),
		secure.NewReferrerPolicy().NoReferrer(),
		secure.NewServer().Set("Different"),
		secure.NewXContentTypeOptions().Nosniff(),
		secure.NewXFrameOptions().Sameorigin(),
		[]*secure.CustomHeader{secure.NewCustomHeader("X-B", "C")},
	)
	foundCustom := false
	foundXFO := false
	for _, h := range s.HeadersList() {
		switch h.(type) {
		case *secure.CustomHeader:
			foundCustom = true
		case *secure.XFrameOptions:
			foundXFO = true
		}
	}
	if !foundCustom {
		t.Errorf("Expected at least one CustomHeader present")
	}
	if !foundXFO {
		t.Errorf("Expected at least one XFrameOptions present")
	}
}

func TestSecureWithPartialHeadersPublic(t *testing.T) {
	s := secure.NewSecurePartial(
		secure.NewXContentTypeOptions().Nosniff(),
		secure.NewServer().Set("PublicTest"),
		secure.NewReferrerPolicy().Origin(),
		[]*secure.CustomHeader{secure.NewCustomHeader("X-Y", "Z")},
		nil,
	)
	foundXCTO := false
	foundServer := false
	foundRef := false
	foundCustom := false
	for _, h := range s.HeadersList() {
		switch h.(type) {
		case *secure.XContentTypeOptions:
			foundXCTO = true
		case *secure.Server:
			foundServer = true
		case *secure.ReferrerPolicy:
			foundRef = true
		case *secure.CustomHeader:
			foundCustom = true
		}
	}
	if !foundXCTO || !foundServer || !foundRef || !foundCustom {
		t.Errorf("Expected partial/typed headers, got %#v", s.HeadersList())
	}
}