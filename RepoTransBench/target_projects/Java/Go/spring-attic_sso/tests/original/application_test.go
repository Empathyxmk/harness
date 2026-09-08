package original

import (
	"testing"
)

func TestSanityCheck(t *testing.T) {
	if true != true {
		t.Errorf("Sanity check should always pass")
	}
}