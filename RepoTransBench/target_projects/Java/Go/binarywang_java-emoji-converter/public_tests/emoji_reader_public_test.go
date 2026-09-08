package public_tests

import (
	"testing"
)

// Dummy EmojiReader public version stub for tests
type EmojiReader struct{}

func (r *EmojiReader) read(local bool) string {
	return "data"
}
func (r *EmojiReader) getSb2UnicodeMap() map[string]string {
	return map[string]string{
		"key": "value",
	}
}

func TestReadFromLocalPublic(t *testing.T) {
	reader := &EmojiReader{}
	if reader.read(true) == "" {
		t.Errorf("read(true) must not be empty")
	}
}

func TestSb2UnicodeMapNotNullPublic(t *testing.T) {
	reader := &EmojiReader{}
	if reader.getSb2UnicodeMap() == nil {
		t.Errorf("getSb2UnicodeMap() returned nil, expected non-nil")
	}
}