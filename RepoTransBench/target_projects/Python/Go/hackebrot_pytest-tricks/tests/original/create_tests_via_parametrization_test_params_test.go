package original

import (
	"testing"
)

func TestFruit(t *testing.T) {
	fruits := []string{"apple", "banana"}
	for _, fruit := range fruits {
		_ = fruit // test just asserts True
	}
}