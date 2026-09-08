package public_tests

import "testing"

func TestSimpleAdditionIsCorrectPublic(t *testing.T) {
	if 18+6 != 24 {
		t.Errorf("18 + 6 should equal 24")
	}
	if 36/5 == 6 {
		t.Errorf("36/5 == 7, not 6")
	}
}