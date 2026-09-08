package public_tests

import (
	"bytes"
	"encoding/gob"
	"testing"
)

func TestSerializationWithDifferentString(t *testing.T) {
	testStr := "PublicTestingStringXYZ"
	var buf bytes.Buffer
	enc := gob.NewEncoder(&buf)
	if err := enc.Encode(testStr); err != nil {
		t.Fatalf("encode error: %v", err)
	}

	var decoded string
	dec := gob.NewDecoder(&buf)
	if err := dec.Decode(&decoded); err != nil {
		t.Fatalf("decode error: %v", err)
	}

	if decoded != testStr {
		t.Errorf("expected %q, got %q", testStr, decoded)
	}
	if decoded == "" {
		t.Error("expected non-empty string")
	}
	if decoded[:6] != "Public" {
		t.Errorf("expected prefix 'Public', got %q", decoded[:6])
	}
}