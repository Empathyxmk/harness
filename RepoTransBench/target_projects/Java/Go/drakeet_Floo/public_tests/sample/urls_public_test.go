package sample

import "testing"

type URLs struct{}

func (URLs) Scheme() string { return "floo" }

const (
	WEB           = "https://m.drakeet.me/web"
	NOT_REGISTERED = "floo://m.drakeet.me/not_registered"
)

// Test that URLs.Scheme() returns "floo"
func TestSchemeIsFlooPublic(t *testing.T) {
	urls := URLs{}
	if urls.Scheme() != "floo" {
		t.Errorf("URLs.Scheme() = %q, want %q", urls.Scheme(), "floo")
	}
}

// Test that WEB and NOT_REGISTERED constants have correct values and prefixes
func TestConstantsPublic(t *testing.T) {
	if WEB != "https://m.drakeet.me/web" {
		t.Errorf("WEB = %q, want %q", WEB, "https://m.drakeet.me/web")
	}
	if NOT_REGISTERED != "floo://m.drakeet.me/not_registered" {
		t.Errorf("NOT_REGISTERED = %q, want %q", NOT_REGISTERED, "floo://m.drakeet.me/not_registered")
	}
	if len(WEB) < 8 || WEB[:8] != "https://" {
		t.Errorf("WEB = %q, should start with \"https://\"", WEB)
	}
	if len(NOT_REGISTERED) < 7 || NOT_REGISTERED[:7] != "floo://" {
		t.Errorf("NOT_REGISTERED = %q, should start with \"floo://\"", NOT_REGISTERED)
	}
}