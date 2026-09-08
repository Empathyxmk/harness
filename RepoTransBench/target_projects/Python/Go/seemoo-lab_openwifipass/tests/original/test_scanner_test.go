package original

import (
	"encoding/hex"
	"testing"
)

// Dummy structures for the tests.
type DummyTLVBox struct {
	d map[int][]byte
}
func (b *DummyTLVBox) ToDict() map[int][]byte { return b.d }

type PWSScanner struct {
	ssid     string
	ssidHash []byte
	result   interface{}
}

func NewPWSScanner(ssid string) *PWSScanner {
	return &PWSScanner{
		ssid:     ssid,
		ssidHash: []byte{0xAA, 0xBB, 0xCC}, // arbitrary hash for test
	}
}

func (s *PWSScanner) getPWSTLV(data []byte) []byte {
	if len(data) >= 2 && data[0] == 0x4c && data[1] == 0x00 {
		return []byte("PAYLOAD")
	}
	return nil
}

func (s *PWSScanner) isSSIDInTLV(data []byte) bool {
	val := s.ssidHash[:3]
	if len(data) < 3 {
		return false
	}
	return (data[len(data)-3] == val[0] && data[len(data)-2] == val[1] && data[len(data)-1] == val[2])
}

func (s *PWSScanner) handleDiscovery(scanEntry ScanEntry, allowAny bool, _ bool) {
	adList := scanEntry.GetScanData()
	for _, ad := range adList {
		adtype := ad.AdType
		val := ad.Value
		if adtype == 255 {
			bytesVal, _ := hex.DecodeString(val)
			payload := s.getPWSTLV(bytesVal)
			if payload != nil && s.isSSIDInTLV(payload) {
				s.result = scanEntry
				return
			}
		}
	}
	s.result = nil
}

// Needed for mimicry in test
type ScanEntry interface {
	GetScanData() []AdvData
}
type AdvData struct {
	AdType int
	Descr  interface{}
	Value  string
}

type DummyScanEntry struct {
	addr     string
	scanData []AdvData
}
func (d *DummyScanEntry) GetScanData() []AdvData { return d.scanData }

func TestGetPWSTLV_WrongCompany(t *testing.T) {
	scanner := NewPWSScanner("testssid")
	if scanner.getPWSTLV([]byte{0x00, 0x00, 'A', 'B', 'C'}) != nil {
		t.Errorf("Expected nil for getPWSTLV on wrong company bytes")
	}
}

func TestGetPWSTLV_RightCompany(t *testing.T) {
	scanner := NewPWSScanner("testssid")
	if got := scanner.getPWSTLV([]byte{0x4c, 0x00, 0xAB, 0xCD, 0xEF}); string(got) != "PAYLOAD" {
		t.Errorf("Expected 'PAYLOAD' for correct prefix, got %v", got)
	}
}

func TestIsSSIDInTLV(t *testing.T) {
	scanner := NewPWSScanner("SSID42")
	val := scanner.ssidHash[:3]
	// last 3 match
	testData := append([]byte("xxxx"), val...)
	if !scanner.isSSIDInTLV(testData) {
		t.Error("Expected isSSIDInTLV to be true for matching suffix")
	}
	// not matching
	if scanner.isSSIDInTLV([]byte("abc123")) {
		t.Error("Expected isSSIDInTLV to be false for non-matching suffix")
	}
}

func TestHandleDiscoverySetsResult(t *testing.T) {
	scanner := NewPWSScanner("ssidX")
	val := scanner.ssidHash[:3]
	payload := append(val, val...) // Satisfies isSSIDInTLV
	entry := &DummyScanEntry{
		addr: "Z",
		scanData: []AdvData{
			{AdType: 255, Descr: nil, Value: "4c00abcdef"},
		},
	}
	// Monkeypatch: override getPWSTLV and isSSIDInTLV
	origGetPWSTLV := scanner.getPWSTLV
	origIsSSIDInTLV := scanner.isSSIDInTLV
	scanner.getPWSTLV = func([]byte) []byte { return payload }
	scanner.isSSIDInTLV = func([]byte) bool { return true }
	scanner.handleDiscovery(entry, true, true)
	if scanner.result != entry {
		t.Error("Expected scanner result to be scanEntry")
	}
	// restore for next tests
	scanner.getPWSTLV = origGetPWSTLV
	scanner.isSSIDInTLV = origIsSSIDInTLV
}

func TestHandleDiscoveryNonmatching(t *testing.T) {
	scanner := NewPWSScanner("ssid")
	entry := &DummyScanEntry{
		scanData: []AdvData{
			{AdType: 255, Descr: nil, Value: "4c00abcdef"},
		},
	}
	// Monkeypatch: getPWSTLV returns nil
	scanner.getPWSTLV = func([]byte) []byte { return nil }
	scanner.handleDiscovery(entry, true, true)
	if scanner.result != nil {
		t.Error("Expected scanner result to be nil for nonmatching entry")
	}
}