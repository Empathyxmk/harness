package public_tests

import (
	"testing"
)

func TestFruitPublic(t *testing.T) {
	fruits := []string{"orange", "grape"}
	for _, fruit := range fruits {
		_ = fruit
	}
}