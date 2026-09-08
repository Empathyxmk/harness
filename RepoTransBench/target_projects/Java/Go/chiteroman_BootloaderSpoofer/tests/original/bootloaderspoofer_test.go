package original

import (
	"testing"

	main "chiteroman_BootloaderSpoofer"
)

func TestInitialStatus(t *testing.T) {
	bs := main.NewBootloaderSpoofer()
	if bs.IsSpoofed() {
		t.Errorf("Expected initial spoofed state to be false, got true")
	}
	if status := bs.Status(); status != "Not spoofed" {
		t.Errorf("Expected initial status to be 'Not spoofed', got: %q", status)
	}
}

func TestSpoofSetsSpoofed(t *testing.T) {
	bs := main.NewBootloaderSpoofer()
	bs.Spoof()
	if !bs.IsSpoofed() {
		t.Errorf("Expected spoofed state after Spoof() to be true, got false")
	}
	if status := bs.Status(); status != "Spoofed" {
		t.Errorf("Expected status after Spoof() to be 'Spoofed', got: %q", status)
	}
}

func TestReset(t *testing.T) {
	bs := main.NewBootloaderSpoofer()
	bs.Spoof()
	bs.Reset()
	if bs.IsSpoofed() {
		t.Errorf("Expected spoofed state after Reset() to be false, got true")
	}
	if status := bs.Status(); status != "Not spoofed" {
		t.Errorf("Expected status after Reset() to be 'Not spoofed', got: %q", status)
	}
}

func TestMultipleSpoof(t *testing.T) {
	bs := main.NewBootloaderSpoofer()
	bs.Spoof()
	bs.Spoof() // should not change state or throw
	if !bs.IsSpoofed() {
		t.Errorf("Expected spoofed state after multiple Spoof() calls to remain true")
	}
}