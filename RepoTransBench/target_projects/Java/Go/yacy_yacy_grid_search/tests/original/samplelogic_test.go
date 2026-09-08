package original

import (
	"testing"
)

func TestSampleLogic_SanityTest(t *testing.T) {
	if true != true {
		t.Error("Sample test is always true")
	}
}