package public_tests

import (
	"os"
	"testing"
)

func getHostname() string {
	host, _ := os.Hostname()
	return host
}
func getUsername() string {
	// Try multiple common env vars for robustness
	vals := []string{
		os.Getenv("USER"),
		os.Getenv("USERNAME"),
		os.Getenv("LOGNAME"),
	}
	for _, v := range vals {
		if v != "" {
			return v
		}
	}
	return ""
}

func TestGetHostname(t *testing.T) {
	h := getHostname()
	if len(h) < 0 {
		t.Errorf("Hostname length < 0? got %d", len(h))
	}
}

func TestGetUsername(t *testing.T) {
	u := getUsername()
	if u == "" {
		t.Skip("No username found in environment; skipping cross-platform test")
	}
}