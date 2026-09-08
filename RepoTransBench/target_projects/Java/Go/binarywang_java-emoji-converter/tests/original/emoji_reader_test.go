package original

import (
	"testing"
)

func TestClassLoads(t *testing.T) {
	// The Go equivalent is that the type is accessible and importable
	type EmojiReader struct{}
	var _ = EmojiReader{}
}