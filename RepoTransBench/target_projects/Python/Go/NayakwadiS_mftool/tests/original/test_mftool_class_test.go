package original

import (
	"testing"
)

func TestClassDummy(t *testing.T) {
	if true != true {
		t.Errorf("Expected true to be true")
	}
}