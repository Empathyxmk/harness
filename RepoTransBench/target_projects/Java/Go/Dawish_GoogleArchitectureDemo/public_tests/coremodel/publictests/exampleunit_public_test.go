package publictests

import "testing"

func TestAdditionIsAlsoCorrectWithDiffData(t *testing.T) {
	if 10+5 != 15 {
		t.Errorf("expected 10 + 5 == 15")
	}
}