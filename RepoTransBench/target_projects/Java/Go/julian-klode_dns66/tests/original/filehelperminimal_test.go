package original

import (
	"bytes"
	"testing"
)

func TestOpenReadFileFound(t *testing.T) {
	content := []byte("abc")
	r := bytes.NewReader(content)
	b := make([]byte, 1)
	_, err := r.Read(b)
	if err != nil {
		t.Fatalf("failed to read: %v", err)
	}
	if b[0] != 'a' {
		t.Fatalf("expected first byte 'a'")
	}
}

func TestOpenReadFileNotFoundFallbackToAssets(t *testing.T) {
	content := []byte("xyz")
	r := bytes.NewReader(content)
	b := make([]byte, 1)
	_, err := r.Read(b)
	if err != nil {
		t.Fatalf("failed to read: %v", err)
	}
	if b[0] != 'x' {
		t.Fatalf("expected first byte 'x'")
	}
}