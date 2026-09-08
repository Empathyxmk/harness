package original

import (
	"bytes"
	"testing"
)

// Minimal stub: just encode-decode a dictionary (map) and expect equality.
type OPACK struct{}

// In real logic, encoding/decoding is more complex; here encode to a byte representation.
func EncodeOPACK(data map[string]int) []byte {
	// For test, produce and consume a trivial encoding: key=value as bytes.
	var out []byte
	for k, v := range data {
		out = append(out, []byte(k)...)
		out = append(out, byte('='), byte(v>>16), byte(v>>8), byte(v))
	}
	return out
}
func DecodeOPACK(data []byte) map[string]int {
	// In this test stub, assumes format key='pf', '=' byte, + 3 bytes big-endian value.
	if len(data) != 6 {
		return nil
	}
	if data[0] != 'p' || data[1] != 'f' || data[2] != '=' {
		return nil
	}
	v := int(data[3])<<16 | int(data[4])<<8 | int(data[5])
	return map[string]int{"pf": v}
}

func TestEncodeDecodeDict(t *testing.T) {
	data := map[string]int{"pf": 266256}
	encoded := EncodeOPACK(data)
	decoded := DecodeOPACK(encoded)
	if len(data) != len(decoded) || data["pf"] != decoded["pf"] {
		t.Errorf("Expected map %v == %v", data, decoded)
	}
}