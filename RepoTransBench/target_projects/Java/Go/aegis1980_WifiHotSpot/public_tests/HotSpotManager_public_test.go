package publictests

import (
	"testing"

	"aegis1980/wifihotspot/hotspot"
)

// Public tests translated from Java's HotSpotManagerPublicTest.java

func TestInitialStatePublic(t *testing.T) {
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

func TestEnableHotspotValidPublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	result := manager.EnableHotspot("PublicSSID", "Another123")
	if !result {
		t.Fatalf("Expected EnableHotspot to return true with valid params")
	}
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled")
	}
	if got, want := manager.GetSsid(), "PublicSSID"; got != want {
		t.Errorf("Expected SSID %q, got %q", want, got)
	}
	if got, want := manager.GetPassword(), "Another123"; got != want {
		t.Errorf("Expected password %q, got %q", want, got)
	}
}

func TestEnableHotspotInvalidSsidPublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("", "publicpass") {
		t.Errorf("Expected EnableHotspot to fail with empty SSID")
	}
	if manager.EnableHotspot("", "publicpass") {
		t.Errorf("Expected EnableHotspot to fail with empty SSID")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}

func TestEnableHotspotInvalidPasswordPublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("MyNetwork", "") {
		t.Errorf("Expected EnableHotspot to fail with null/empty password")
	}
	if manager.EnableHotspot("MyNetwork", "short1") {
		t.Errorf("Expected EnableHotspot to fail with short password")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}

func TestDisableHotspotPublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	manager.EnableHotspot("Network42", "SuperPass9")
	if !manager.IsEnabled() {
		t.Fatalf("Expected hotspot to be enabled after EnableHotspot")
	}
	manager.DisableHotspot()
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to be disabled after DisableHotspot")
	}
}

func TestEnableHotspotPasswordExactly8Public(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	password8 := "abcdefgh"
	result := manager.EnableHotspot("SSID_Public", password8)
	if !result {
		t.Errorf("Expected EnableHotspot to succeed with password len 8")
	}
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled")
	}
	if got := manager.GetSsid(); got != "SSID_Public" {
		t.Errorf("Expected SSID %q, got %q", "SSID_Public", got)
	}
	if got := manager.GetPassword(); got != password8 {
		t.Errorf("Expected password %q, got %q", password8, got)
	}
}

func TestDisablingTwicePublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	manager.DisableHotspot()
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to be disabled")
	}
	manager.EnableHotspot("PublicSSID2", "ExtraPass2")
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

func TestEnableHotspotPasswordWith8ButNullSSIDPublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("", "abcdefgh") {
		t.Errorf("Expected EnableHotspot to fail with empty SSID")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}

func TestEnableHotspotNullPasswordPublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("AnotherNet", "") {
		t.Errorf("Expected EnableHotspot to fail with null/empty password")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}

func TestMultipleEnablesPublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if !manager.EnableHotspot("FirstSSID", "initPass99") {
		t.Fatalf("Expected EnableHotspot to succeed on first config")
	}
	if got := manager.GetSsid(); got != "FirstSSID" {
		t.Errorf("Expected SSID to be changed to %q, got %q", "FirstSSID", got)
	}
	if got := manager.GetPassword(); got != "initPass99" {
		t.Errorf("Expected password to be changed to %q, got %q", "initPass99", got)
	}
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled")
	}

	if !manager.EnableHotspot("SecondSSID", "reNewPass0") {
		t.Fatalf("Expected EnableHotspot to succeed on reconfig")
	}
	if got := manager.GetSsid(); got != "SecondSSID" {
		t.Errorf("Expected SSID to be changed to %q, got %q", "SecondSSID", got)
	}
	if got := manager.GetPassword(); got != "reNewPass0" {
		t.Errorf("Expected password to be changed to %q, got %q", "reNewPass0", got)
	}
	if !manager.IsEnabled() {
		t.Errorf("Expected hotspot to be enabled")
	}
}

func TestEnableHotspotEmptyPasswordPublic(t *testing.T) {
	manager := hotspot.NewHotSpotManager()
	if manager.EnableHotspot("MyNet", "") {
		t.Errorf("Expected EnableHotspot to fail with empty password")
	}
	if manager.IsEnabled() {
		t.Errorf("Expected hotspot to remain disabled")
	}
}