package original

import (
	"TypeError_secure/secure"
	"testing"
	"strings"
)

func TestDefaultCacheControl(t *testing.T) {
	cacheControl := secure.NewCacheControl()
	if cacheControl.HeaderValue() != "no-store" {
		t.Errorf("Expected default Cache-Control to be 'no-store', got %q", cacheControl.HeaderValue())
	}
}

func TestSetNoCache(t *testing.T) {
	cacheControl := secure.NewCacheControl().NoCache()
	if !strings.Contains(cacheControl.HeaderValue(), "no-cache") {
		t.Errorf("Expected header value to include 'no-cache', got %q", cacheControl.HeaderValue())
	}
}

func TestSetMaxAge(t *testing.T) {
	cacheControl := secure.NewCacheControl().MaxAge(3600)
	if !strings.Contains(cacheControl.HeaderValue(), "max-age=3600") {
		t.Errorf("Expected header value to include 'max-age=3600', got %q", cacheControl.HeaderValue())
	}
}

func TestClearCacheControl(t *testing.T) {
	cacheControl := secure.NewCacheControl().NoCache().Clear()
	if cacheControl.HeaderValue() != "no-store" {
		t.Errorf("Expected Cache-Control to be 'no-store' after clear, got %q", cacheControl.HeaderValue())
	}
}

func TestMultipleDirectives(t *testing.T) {
	cacheControl := secure.NewCacheControl().NoCache().MustRevalidate().MaxAge(3600)
	if cacheControl.HeaderValue() != "no-cache, must-revalidate, max-age=3600" {
		t.Errorf("Expected joined directive string, got %q", cacheControl.HeaderValue())
	}
}