package public_tests

import (
	"os"
	"testing"
)

// Simulate the is_flatpak logic from the Python version.
func publicIsFlatpak() bool {
	return os.Getenv("FLATPAK_ID") != "" ||
		os.Getenv("STEAM_FLATPAK_PRIME") != "" ||
		os.Getenv("PROTONTRICKS_FLATPAK") == "1"
}

func TestPublicIsFlatpak(t *testing.T) {
	os.Setenv("FLATPAK_ID", "foo.bar.publicprotontricks")
	defer os.Unsetenv("FLATPAK_ID")
	if !publicIsFlatpak() {
		t.Error("publicIsFlatpak() with FLATPAK_ID = foo.bar.publicprotontricks must return true")
	}
}

func TestPublicIsFlatpakFallback(t *testing.T) {
	os.Unsetenv("FLATPAK_ID")
	os.Setenv("STEAM_FLATPAK_PRIME", "1")
	defer os.Unsetenv("STEAM_FLATPAK_PRIME")
	if !publicIsFlatpak() {
		t.Error("publicIsFlatpak() with STEAM_FLATPAK_PRIME should return true")
	}
}

func TestPublicNotFlatpak(t *testing.T) {
	os.Unsetenv("FLATPAK_ID")
	os.Unsetenv("STEAM_FLATPAK_PRIME")
	os.Setenv("PROTONTRICKS_FLATPAK", "0")
	defer os.Unsetenv("PROTONTRICKS_FLATPAK")
	if publicIsFlatpak() {
		t.Error("publicIsFlatpak() with all vars off, should return false")
	}
}

func TestPublicNotFlatpakFallback(t *testing.T) {
	os.Unsetenv("FLATPAK_ID")
	os.Unsetenv("STEAM_FLATPAK_PRIME")
	os.Setenv("PROTONTRICKS_FLATPAK", "0")
	defer os.Unsetenv("PROTONTRICKS_FLATPAK")
	if publicIsFlatpak() {
		t.Error("publicIsFlatpak() with all vars off, should return false")
	}
}