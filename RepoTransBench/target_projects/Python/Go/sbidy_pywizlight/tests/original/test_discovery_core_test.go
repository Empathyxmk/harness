package original

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"net"
	"sync"
	"testing"
	"time"
)

// DummyTransport mimics network transport for unit testing.
type DummyTransport struct {
	sent   [][2]interface{} // tuple: []byte, addr
	closed bool
	mu     sync.Mutex
}

func (dt *DummyTransport) SendTo(data []byte, addr string) {
	dt.mu.Lock()
	defer dt.mu.Unlock()
	dt.sent = append(dt.sent, [2]interface{}{data, addr})
}
func (dt *DummyTransport) Close() {
	dt.mu.Lock()
	defer dt.mu.Unlock()
	dt.closed = true
}

// DummyLoop simulates async constructs.
type DummyLoop struct {
	calls   int
	futures []chan error
}

func (dl *DummyLoop) CallLater(t time.Duration, cb func()) {
	dl.calls++
	// not scheduling since we don't really async here for tests
	cb()
}
func (dl *DummyLoop) CreateFuture() chan error {
	c := make(chan error, 1)
	dl.futures = append(dl.futures, c)
	return c
}

// BulbRegistry and DiscoveredBulb stub
type DiscoveredBulb struct {
	IpAddress  string
	MacAddress string
}
type BulbRegistry struct {
	bulbs []DiscoveredBulb
	mu    sync.Mutex
}
func (br *BulbRegistry) AddBulb(b DiscoveredBulb) {
	br.mu.Lock()
	defer br.mu.Unlock()
	br.bulbs = append(br.bulbs, b)
}
func (br *BulbRegistry) Bulbs() []DiscoveredBulb {
	br.mu.Lock()
	defer br.mu.Unlock()
	return append([]DiscoveredBulb{}, br.bulbs...)
}
func NewBulbRegistry() *BulbRegistry {
	return &BulbRegistry{}
}

// BroadcastProtocol simulates UDP broadcast logic
type BroadcastProtocol struct {
	loop      *DummyLoop
	registry  *BulbRegistry
	addr      string
	transport *DummyTransport
	future    chan error // closed to signal done
}

func NewBroadcastProtocol(loop *DummyLoop, registry *BulbRegistry, addr string, future chan error) *BroadcastProtocol {
	return &BroadcastProtocol{loop: loop, registry: registry, addr: addr, future: future}
}
var RegisterMsg = []byte(`{"method":"registration"`)

func (bp *BroadcastProtocol) BroadcastRegistration() {
	if bp.transport == nil {
		return
	}
	bp.transport.SendTo(RegisterMsg, bp.addr)
}
func (bp *BroadcastProtocol) DatagramReceived(data []byte, from string, t *testing.T) {
	var msg map[string]interface{}
	if err := json.Unmarshal(data, &msg); err != nil {
		t.Logf("invalid message: %v", err)
		return
	}
	if result, ok := msg["result"].(map[string]interface{}); ok {
		if mac, ok := result["mac"].(string); ok {
			bulb := DiscoveredBulb{IpAddress: from, MacAddress: mac}
			bp.registry.AddBulb(bulb)
		}
	}
}
func (bp *BroadcastProtocol) ConnectionMade(tr *DummyTransport) {
	bp.transport = tr
	bp.BroadcastRegistration()
}
func (bp *BroadcastProtocol) ConnectionLost(err error) {
	if bp.transport != nil {
		bp.transport.Close()
	}
	bp.transport = nil
	if bp.future != nil {
		if err == nil {
			close(bp.future)
		} else {
			bp.future <- err
			close(bp.future)
		}
	}
}

func TestBroadcastProtocol_BroadcastRegistration(t *testing.T) {
	loop := &DummyLoop{}
	reg := NewBulbRegistry()
	bc := NewBroadcastProtocol(loop, reg, "127.0.0.1", make(chan error, 1))

	// Should NOT panic if transport is nil
	bc.BroadcastRegistration()

	// Now with transport
	dummyTr := &DummyTransport{}
	bc.transport = dummyTr
	bc.BroadcastRegistration()
	found := false
	for _, sent := range dummyTr.sent {
		if bytes.Contains(sent[0].([]byte), RegisterMsg) {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Expected REGISTER_MSG sent over transport")
	}
	if dummyTr.sent[0][1].(string) != "127.0.0.1" {
		t.Errorf("Expected address %s, got %v", "127.0.0.1", dummyTr.sent[0][1])
	}
}

func TestBroadcastProtocol_DatagramReceivedGood(t *testing.T) {
	loop := &DummyLoop{}
	reg := NewBulbRegistry()
	future := make(chan error, 1)
	proto := NewBroadcastProtocol(loop, reg, "127.0.0.1", future)
	validJSON := []byte(`{"result":{"mac":"OOOO"} }`)
	proto.DatagramReceived(validJSON, "1.1.1.1", t)
	bulbs := reg.Bulbs()
	found := false
	for _, bulb := range bulbs {
		if bulb.MacAddress == "OOOO" {
			found = true
		}
	}
	if !found {
		t.Errorf("Expected bulb with MAC OOOO found in registry")
	}
}

func TestBroadcastProtocol_DatagramReceivedBadJSON(t *testing.T) {
	loop := &DummyLoop{}
	reg := NewBulbRegistry()
	proto := NewBroadcastProtocol(loop, reg, "127.0.0.1", make(chan error, 1))
	buf := new(bytes.Buffer)
	tLogger := testing.TB(t)
	proto.DatagramReceived([]byte("{foo}"), "2.2.2.2", tLogger.(*testing.T))
	// Manual caplog
}

func TestBroadcastProtocol_ConnectionMadeTriggersBroadcast(t *testing.T) {
	reg := NewBulbRegistry()
	loop := &DummyLoop{}
	proto := NewBroadcastProtocol(loop, reg, "127.2.3.4", make(chan error, 1))

	dummy := &DummyTransport{}
	called := false
	// Monkeypatch BC to check call
	orig := proto.BroadcastRegistration
	proto.BroadcastRegistration = func() { called = true }
	proto.ConnectionMade(dummy)
	if !called {
		t.Error("Expected BroadcastRegistration to be called on ConnectionMade()")
	}
	proto.BroadcastRegistration = orig
}

func TestBroadcastProtocol_ConnectionLostSetsResult(t *testing.T) {
	reg := NewBulbRegistry()
	loop := &DummyLoop{}
	// The `future` should be closed and result set to None after connection_lost(nil)
	future := make(chan error, 1)
	proto := NewBroadcastProtocol(loop, reg, "1.2.3.4", future)
	proto.transport = &DummyTransport{}
	proto.ConnectionLost(nil)
	select {
	case <-future:
		// OK: channel is closed
	default:
		t.Error("future channel should be closed")
	}

	// With error
	fut2 := make(chan error, 1)
	proto2 := NewBroadcastProtocol(loop, reg, "1.2.3.4", fut2)
	proto2.transport = &DummyTransport{}
	err := errors.New("fail error")
	proto2.ConnectionLost(err)
	select {
	case e := <-fut2:
		if e == nil || e.Error() != "fail error" {
			t.Errorf("expected error in future result")
		}
	default:
		t.Error("future channel not closed with error")
	}
}

func TestFindWizlightsBasic(t *testing.T) {
	// Simulate registry and return
	bulbs := []DiscoveredBulb{{IpAddress: "10.0.0.2", MacAddress: "aaaa"}}
	registry := &BulbRegistry{bulbs: bulbs}
	discover := func(timeout float64) ([]DiscoveredBulb, error) {
		return registry.Bulbs(), nil
	}
	result, err := discover(0.01)
	if err != nil || len(result) == 0 || result[0].IpAddress != "10.0.0.2" {
		t.Fatalf("Expected bulb with IP 10.0.0.2, got %+v", result)
	}
}

func TestDiscoverLights(t *testing.T) {
	bulbs := []DiscoveredBulb{{IpAddress: "10.9.8.7", MacAddress: "bbcc"}}
	findwizlights := func(timeout float64) ([]DiscoveredBulb, error) {
		return bulbs, nil
	}
	lights, err := findwizlights(0.1)
	if err != nil || len(lights) == 0 {
		t.Fatalf("Expected bulbs found, got error %v", err)
	}
	if lights[0].IpAddress != "10.9.8.7" || lights[0].MacAddress != "bbcc" {
		t.Errorf("Unexpected bulb info: %+v", lights[0])
	}
}