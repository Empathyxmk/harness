package original

import (
	"testing"

	"aegis1980/wifihotspot/hotspot"
)

// Original (private) tests translated from Java's HotSpotManagerTest.java

func TestInitialState(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot initially disabled")
	}
	if got, want := manager.GetSsid(), "defaultSSID"; got != want {
		t.Errorf("Expected default SSID %q, got %q", want, got)
	}
	if got, want := manager.GetPassword(), "password"; got != want {
		t.Errorf("Expected default password %q, got %q", want, got)
	}
}

func TestEnableHotspotValid(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	result := manager.EnableHotspot("MySSID", "MyPass123")
	if !result {
		t.Fatalf("Expected EnableHotspot to return true with valid params")
	}
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled")
	}
	if got, want := manager.GetSsid(), "MySSID"; got != want {
		t.Errorf("Expected SSID %q, got %q", want, got)
	}
	if got, want := manager.GetPassword(), "MyPass123"; got != want {
		t.Errorf("Expected password %q, got %q", want, got)
	}
}

func TestEnableHotspotInvalidSsid(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("", "password123") {
		t.Errorf("Expected EnableHotspot to fail with empty SSID")
	}
	if manager.EnableHotspot("", "password123") {
		t.Errorf("Expected EnableHotspot to fail with empty SSID")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}

func TestEnableHotspotInvalidPassword(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("SSID", "") {
		t.Errorf("Expected EnableHotspot to fail with empty password")
	}
	if manager.EnableHotspot("SSID", "short") {
		t.Errorf("Expected EnableHotspot to fail with short password")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}

func TestDisableHotspot(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	manager.EnableHotspot("SSID", "password123")
	if !manager.IsEnabled() {
		t.Fatalf("Expected hotspot to be enabled after EnableHotspot")
	}
	manager.DisableHotspot()
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to be disabled after DisableHotspot")
	}
}

func TestEnableHotspotPasswordExactly8(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	password8 := "12345678"
	result := manager.EnableHotspot("SSID2", password8)
	if !result {
		t.Errorf("Expected EnableHotspot to succeed with password len 8")
	}
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled")
	}
	if got := manager.GetSsid(); got != "SSID2" {
		t.Errorf("Expected SSID %q, got %q", "SSID2", got)
	}
	if got := manager.GetPassword(); got != password8 {
		t.Errorf("Expected password %q, got %q", password8, got)
	}
}

func TestDisablingTwice(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	manager.DisableHotspot()
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to be disabled")
	}
	manager.EnableHotspot("SSID", "password123")
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled after EnableHotspot")
	}
	manager.DisableHotspot()
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to be disabled after DisableHotspot")
	}
	manager.DisableHotspot()
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to still be disabled after second DisableHotspot")
	}
}

func TestEnableHotspotPasswordWith8ButNullSSID(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("", "12345678") {
		t.Errorf("Expected EnableHotspot to fail with empty SSID")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}

func TestEnableHotspotNullPassword(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("SSID", "") {
		t.Errorf("Expected EnableHotspot to fail with null/empty password")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}

func TestMultipleEnables(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if !manager.EnableHotspot("SSID", "password123") {
		t.Fatalf("Expected EnableHotspot to succeed on first config")
	}
	if got := manager.GetSsid(); got != "SSID" {
		t.Errorf("Expected SSID to be changed to %q, got %q", "SSID", got)
	}
	if got := manager.GetPassword(); got != "password123" {
		t.Errorf("Expected password to be changed to %q, got %q", "password123", got)
	}
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled")
	}

	if !manager.EnableHotspot("SSID2", "password456") {
		t.Fatalf("Expected EnableHotspot to succeed on reconfig")
	}
	if got := manager.GetSsid(); got != "SSID2" {
		t.Errorf("Expected SSID to be changed to %q, got %q", "SSID2", got)
	}
	if got := manager.GetPassword(); got != "password456" {
		t.Errorf("Expected password to be changed to %q, got %q", "password456", got)
	}
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled")
	}
}

func TestEnableHotspotEmptyPassword(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("SSID", "") {
		t.Errorf("Expected EnableHotspot to fail with empty password")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}