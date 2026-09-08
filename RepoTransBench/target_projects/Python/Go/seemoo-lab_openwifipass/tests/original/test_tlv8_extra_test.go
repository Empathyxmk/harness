package original

import (
	"bytes"
	"testing"
)

// Test helpers to mimic TLV8/TLV8Box logic for testing.
// In actual use, these would call into real code – here, we provide stand-ins for test logic.

type TLV8 struct {
	Type   byte
	Payload []byte
}
type TLV8Box struct {
	tlv8s []TLV8
}

func NewTLV8(t byte, payload []byte) TLV8 {
	return TLV8{Type: t, Payload: payload}
}

func (t TLV8) Encode() []byte {
	l := len(t.Payload)
	b := []byte{t.Type, byte(l)}
	b = append(b, t.Payload...)
	return b
}

// Real world decode logic would be robust and handle error cases
func DecodeTLV8Box(data []byte) *TLV8Box {
	out := []TLV8{}
	for len(data) >= 2 {
		typ := data[0]
		ln := int(data[1])
		if len(data) < 2+ln {
			break
		}
		payload := data[2 : 2+ln]
		out = append(out, TLV8{Type: typ, Payload: payload})
		data = data[2+ln:]
	}
	return &TLV8Box{tlv8s: out}
}

func (t TLV8) String() string {
	return "TLV8(type: " + string(int(t.Type)+'0') + ", payload...)"
}

func (b *TLV8Box) String() string {
	return "TLV8Box(...)"
}

func (b *TLV8Box) ToDict() map[byte][]byte {
	out := make(map[byte][]byte)
	for _, tlv := range b.tlv8s {
		if v, exists := out[tlv.Type]; exists {
			out[tlv.Type] = append(v, tlv.Payload...)
		} else {
			out[tlv.Type] = make([]byte, len(tlv.Payload))
			copy(out[tlv.Type], tlv.Payload)
		}
	}
	return out
}

func (b *TLV8Box) Encode() []byte {
	var out []byte
	for _, tlv := range b.tlv8s {
		out = append(out, tlv.Encode()...)
	}
	return out
}

func TestTLV8EncodeDecodeStrAndToDict(t *testing.T) {
	tlv := NewTLV8(0x01, []byte{0xAA, 0xBB})
	encoded := tlv.Encode()
	box := DecodeTLV8Box(encoded)
	if box == nil {
		t.Fatalf("DecodeTLV8Box returned nil")
	}
	if len(box.tlv8s) == 0 {
		t.Fatalf("No TLV8 decoded")
	}
	decoded := box.tlv8s[0]
	if decoded.Type != 0x01 {
		t.Errorf("Expected type 0x01, got %x", decoded.Type)
	}
	if !bytes.Equal(decoded.Payload, []byte{0xAA, 0xBB}) {
		t.Errorf("Expected payload [0xAA,0xBB], got %v", decoded.Payload)
	}
	if s := tlv.String(); len(s) < 13 || s[:11] != "TLV8(type: " {
		t.Errorf("TLV8.String() format mismatch: %s", s)
	}
	if s := box.String(); s == "" {
		t.Error("TLV8Box.String() returned empty string")
	}
	dct := box.ToDict()
	if _, ok := dct[0x01]; !ok {
		t.Errorf("Expected key 0x01 in dict")
	}
	if !bytes.Equal(dct[0x01], []byte{0xAA, 0xBB}) {
		t.Errorf("Expected dict[1]=[0xAA,0xBB], got %v", dct[0x01])
	}
}

func TestTLV8BoxMultipleEntriesToDictMerging(t *testing.T) {
	t1 := NewTLV8(7, []byte{0x01})
	t2 := NewTLV8(7, []byte{0x02})
	box := &TLV8Box{tlv8s: []TLV8{t1, t2}}
	dct := box.ToDict()
	want := []byte{0x01, 0x02}
	if !bytes.Equal(dct[7], want) {
		t.Errorf("Expected dict[7]=[0x01,0x02], got %v", dct[7])
	}
}

func TestTLV8BoxDecodeFromDataBoundary(t *testing.T) {
	// data shorter than expected should not panic
	data1 := []byte{0x22}
	box1 := DecodeTLV8Box(data1)
	if box1 == nil {
		t.Fatalf("DecodeTLV8Box returned nil")
	}
	if len(box1.tlv8s) != 0 {
		t.Errorf("Expected 0 TLV8s for short data, got %d", len(box1.tlv8s))
	}
	data2 := []byte{0x22, 0x01}
	box2 := DecodeTLV8Box(data2)
	if box2 == nil {
		t.Fatalf("DecodeTLV8Box returned nil")
	}
	if len(box2.tlv8s) != 0 {
		t.Errorf("Expected 0 TLV8s for insufficient payload, got %d", len(box2.tlv8s))
	}
}

func TestTLV8BoxEmptyEncode(t *testing.T) {
	box := &TLV8Box{}
	if res := box.Encode(); len(res) != 0 {
		t.Errorf("Expected empty encoding for empty TLV8Box, got %v", res)
	}
	if str := box.String(); str == "" {
		t.Error("Expected non-empty string from TLV8Box.String() on empty box")
	}
}