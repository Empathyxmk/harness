package public_tests

import (
	"testing"

	main "chiteroman_BootloaderSpoofer"
)

func TestToggleSpoofState(t *testing.T) {
	bs := main.NewBootloaderSpoofer()
	// Sequence: spoof, reset, spoof
	bs.Spoof()
	if !bs.IsSpoofed() {
		t.Errorf("Expected spoofed state after Spoof() to be true")
	}
	if status := bs.Status(); status != "Spoofed" {
		t.Errorf("Expected status after Spoof() to be 'Spoofed', got: %q", status)
	}
	bs.Reset()
	if bs.IsSpoofed() {
		t.Errorf("Expected spoofed state after Reset() to be false")
	}
	if status := bs.Status(); status != "Not spoofed" {
		t.Errorf("Expected status after Reset() to be 'Not spoofed', got: %q", status)
	}
	bs.Spoof()
	if !bs.IsSpoofed() {
		t.Errorf("Expected spoofed state after second Spoof() to be true")
	}
	if status := bs.Status(); status != "Spoofed" {
		t.Errorf("Expected status after second Spoof() to be 'Spoofed', got: %q", status)
	}
}

func TestMultipleReset(t *testing.T) {
	bs := main.NewBootloaderSpoofer()
	// Try resetting before spoofing, then after spoofing
	bs.Reset() // should remain Not spoofed
	if bs.IsSpoofed() {
		t.Errorf("Expected to stay not spoofed after Reset() without Spoof()")
	}
	if status := bs.Status(); status != "Not spoofed" {
		t.Errorf("Expected status to be 'Not spoofed', got: %q", status)
	}
	bs.Spoof()
	if !bs.IsSpoofed() {
		t.Errorf("Expected mocked state after Spoof() to be true")
	}
	bs.Reset()
	bs.Reset() // should stay Not spoofed after two resets
	if bs.IsSpoofed() {
		t.Errorf("Expected to be not spoofed after two consecutive Reset()")
	}
	if status := bs.Status(); status != "Not spoofed" {
		t.Errorf("Expected status after two consecutive Reset() to be 'Not spoofed', got: %q", status)
	}
}

func TestAlternatingSpoofAndReset(t *testing.T) {
	bs := main.NewBootloaderSpoofer()
	// Spoof -> Reset -> Spoof -> Reset
	bs.Spoof()
	if !bs.IsSpoofed() {
		t.Errorf("Expected spoofed after first Spoof()")
	}
	bs.Reset()
	if bs.IsSpoofed() {
		t.Errorf("Expected not spoofed after first Reset()")
	}
	bs.Spoof()
	if !bs.IsSpoofed() {
		t.Errorf("Expected spoofed after second Spoof()")
	}
	bs.Reset()
	if bs.IsSpoofed() {
		t.Errorf("Expected not spoofed after second Reset()")
	}
	if status := bs.Status(); status != "Not spoofed" {
		t.Errorf("Expected status to be 'Not spoofed', got: %q", status)
	}
}

func TestRepeatedResetWithoutSpoof(t *testing.T) {
	bs := main.NewBootloaderSpoofer()
	bs.Reset()
	bs.Reset()
	// Never spoofed
	if bs.IsSpoofed() {
		t.Errorf("Expected not spoofed after repeated Reset() before any Spoof()")
	}
	if status := bs.Status(); status != "Not spoofed" {
		t.Errorf("Expected status to be 'Not spoofed', got: %q", status)
	}
	// Now spoof and test again
	bs.Spoof()
	if !bs.IsSpoofed() {
		t.Errorf("Expected spoofed after Spoof() in repeated reset test")
	}
	bs.Reset()
	if bs.IsSpoofed() {
		t.Errorf("Expected not spoofed after Reset() following Spoof()")
	}
}