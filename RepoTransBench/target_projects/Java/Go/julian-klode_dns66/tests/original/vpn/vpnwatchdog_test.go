package vpn

import "testing"

type Watchdog struct {
	lastPacketReceived int
	lastPacketSent     int
	initPenalty        int
	enabled            bool
}

func (v *Watchdog) getPollTimeout() int {
	if !v.enabled {
		return -1
	}
	if v.lastPacketReceived > 0 && v.lastPacketSent > 0 {
		return 7000
	}
	return 1000
}

func TestGetTimeout(t *testing.T) {
	wg := &Watchdog{enabled: true}
	if got := wg.getPollTimeout(); got != 1000 {
		t.Errorf("Expected 1000, got %d", got)
	}
	wg.lastPacketSent = 2
	wg.lastPacketReceived = 1
	if got := wg.getPollTimeout(); got != 7000 {
		t.Errorf("Expected 7000, got %d", got)
	}
}

func TestDisabledWatchdog(t *testing.T) {
	wg := &Watchdog{enabled: false}
	if got := wg.getPollTimeout(); got != -1 {
		t.Errorf("Expected -1, got %d", got)
	}
}