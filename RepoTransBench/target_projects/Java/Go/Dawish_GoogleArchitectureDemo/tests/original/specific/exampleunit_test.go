package specific

import (
	"testing"
)

func TestAdditionIsCorrect_GoogleArchitectureSpecific(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("2 + 2 should equal 4")
	}
}