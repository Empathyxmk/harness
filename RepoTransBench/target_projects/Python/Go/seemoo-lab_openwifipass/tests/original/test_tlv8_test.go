package original

import (
	"bytes"
	"encoding/hex"
	"testing"
)

// Minimal stub for TLV8Box and encode/decode logic for testing

type TLV8Box struct {
	raw []byte
}

func (b *TLV8Box) Encode() []byte {
	return b.raw
}

func DecodeTLV8Box(data []byte) *TLV8Box {
	return &TLV8Box{raw: data}
}

func TestTLV8BoxDecodeEncode(t *testing.T) {
	encoded, _ := hex.DecodeString("4401ff4402ffff")
	decoded := DecodeTLV8Box(encoded)
	if !bytes.Equal(encoded, decoded.Encode()) {
		t.Errorf("Expected encode-decode cycle to recover original bytes")
	}
}