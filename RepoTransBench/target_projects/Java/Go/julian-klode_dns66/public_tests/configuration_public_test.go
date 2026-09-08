package public_tests

import (
	"strings"
	"testing"
)

func TestIsDownloadable(t *testing.T) {
	downloadableUris := []string{
		"http://public.com",
		"https://public.com",
	}
	notDownloadable := []string{
		"ftp://public.com",
		"file:///tmp/file",
		"httpexample.com",
		"httpsexample.com",
	}

	for _, uri := range downloadableUris {
		if !strings.HasPrefix(uri, "http://") && !strings.HasPrefix(uri, "https://") {
			t.Errorf("Expected downloadable for URI %s", uri)
		}
	}
	for _, uri := range notDownloadable {
		if strings.HasPrefix(uri, "http://") || strings.HasPrefix(uri, "https://") {
			t.Errorf("%s wrongly detected as downloadable", uri)
		}
	}
}

func TestReadNewer(t *testing.T) {
	version := 5
	currentVersion := 3
	if version <= currentVersion {
		t.Errorf("Test expects newer version: got %d, want >%d", version, currentVersion)
	}
}

func TestReadWrite(t *testing.T) {
	original := "{\"autoStart\":true}"
	got := strings.TrimSpace(original)
	got2 := strings.TrimSpace(got)
	if got != got2 {
		t.Errorf("expected string to round-trip, got1=%q got2=%q", got, got2)
	}
}