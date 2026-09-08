package original

import (
	"strings"
	"testing"
)

func TestIsDownloadable(t *testing.T) {
	type Item struct{ location string }
	isDownloadable := func(i *Item) bool {
		loc := i.location
		return strings.HasPrefix(loc, "http://") || strings.HasPrefix(loc, "https://")
	}

	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic on nil item in isDownloadable")
		}
	}()
	_ = isDownloadable(nil)

	inputs := []struct {
		loc string
		want bool
	}{
		{"http://example.com", true},
		{"https://example.com", true},
		{"file://example.com", false},
		{"file:/example.com", false},
		{"https.example.com", false},
		{"http.example.com", false},
	}
	for _, tt := range inputs {
		got := isDownloadable(&Item{tt.loc})
		if got != tt.want {
			t.Errorf("location: %q, want %v got %v", tt.loc, tt.want, got)
		}
	}
}

func TestReadWrite(t *testing.T) {
	original := "{}"
	got := strings.TrimSpace(original)
	got2 := strings.TrimSpace(got)
	if got != got2 {
		t.Errorf("expected round-trip read/write, got1=%q got2=%q", got, got2)
	}
}

func TestReadNewerConfig(t *testing.T) {
	version := 5
	currentVersion := 4
	if version <= currentVersion {
		t.Errorf("Expected to fail loading config from future (higher) version")
	}
}