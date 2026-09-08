package original

import (
	"testing"
	"spring5webapp"
)

func TestContextLoads(t *testing.T) {
	// Just calls the main method
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Calling main panicked: %v", r)
		}
	}()
	spring5webapp.Main([]string{})
}