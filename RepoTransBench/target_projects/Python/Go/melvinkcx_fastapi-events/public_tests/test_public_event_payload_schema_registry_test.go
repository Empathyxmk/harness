package public_tests

import (
	"testing"
)

func TestPlaceholderEventPayloadSchemaRegistry(t *testing.T) {
	got := []int{2, 4, 6}
	expected := []int{2, 4, 6}
	for i, v := range got {
		if v != expected[i] {
			t.Errorf("slice content mismatch at %d: got %v, want %v", i, v, expected[i])
		}
	}
}