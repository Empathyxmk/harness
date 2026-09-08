package util

import (
	"testing"
)

const (
	DISCONNECTED       = 0
	WIFI_CONNECTED     = 1
	ETHERNET_CONNECTED = 2
)

// Simulated context for network
type DummyContext struct {
	WifiAvailable      bool
	WifiConnected      bool
	EthAvailable       bool
	EthConnected       bool
	NetInfos           []bool // Simulate connection states
}

func GetNetConnStatus(ctx *DummyContext) int {
	if ctx == nil {
		return DISCONNECTED
	}
	if ctx.WifiAvailable && ctx.WifiConnected {
		return WIFI_CONNECTED
	}
	if ctx.EthAvailable && ctx.EthConnected {
		return ETHERNET_CONNECTED
	}
	return DISCONNECTED
}

func IsNetConnected(ctx *DummyContext) bool {
	if ctx == nil {
		return false
	}
	for _, connected := range ctx.NetInfos {
		if connected {
			return true
		}
	}
	return false
}

// Simulate netConnected LiveData<Boolean> with a simple function
func NetConnected(ctx *DummyContext) bool {
	return IsNetConnected(ctx)
}

func TestGetNetConnStatus_NullContext(t *testing.T) {
	status := GetNetConnStatus(nil)
	if status != DISCONNECTED {
		t.Errorf("expected DISCONNECTED for nil context, got %d", status)
	}
}

func TestGetNetConnStatus_WifiConnected(t *testing.T) {
	ctx := &DummyContext{
		WifiAvailable: true, WifiConnected: true,
	}
	status := GetNetConnStatus(ctx)
	if status != WIFI_CONNECTED {
		t.Errorf("expected WIFI_CONNECTED, got %d", status)
	}
}

func TestGetNetConnStatus_EthernetConnected(t *testing.T) {
	ctx := &DummyContext{
		WifiAvailable: false, EthAvailable: true, EthConnected: true,
	}
	status := GetNetConnStatus(ctx)
	if status != ETHERNET_CONNECTED {
		t.Errorf("expected ETHERNET_CONNECTED, got %d", status)
	}
}

func TestGetNetConnStatus_None(t *testing.T) {
	ctx := &DummyContext{
		WifiAvailable: false, EthAvailable: false,
	}
	status := GetNetConnStatus(ctx)
	if status != DISCONNECTED {
		t.Errorf("expected DISCONNECTED, got %d", status)
	}
}

func TestIsNetConnected_NullContext(t *testing.T) {
	if IsNetConnected(nil) {
		t.Error("expected IsNetConnected(nil) to be false")
	}
}

func TestIsNetConnected_Connected(t *testing.T) {
	ctx := &DummyContext{
		NetInfos: []bool{true},
	}
	if !IsNetConnected(ctx) {
		t.Error("expected connected")
	}
}

func TestIsNetConnected_None(t *testing.T) {
	ctx := &DummyContext{
		NetInfos: nil,
	}
	if IsNetConnected(ctx) {
		t.Error("expected not connected")
	}
}

func TestIsNetConnected_NotConnected(t *testing.T) {
	ctx := &DummyContext{
		NetInfos: []bool{false},
	}
	if IsNetConnected(ctx) {
		t.Error("expected not connected")
	}
}

func TestNetConnected_NullContext(t *testing.T) {
	if NetConnected(nil) {
		t.Error("expected NetConnected(nil) to be false")
	}
}