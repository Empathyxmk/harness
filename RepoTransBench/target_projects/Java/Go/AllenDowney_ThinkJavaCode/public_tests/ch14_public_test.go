package public_tests

import "testing"

func TestPlaceholderCh14(t *testing.T) {
	if got, want := "public", "PUBLIC"; got != want && got != "PUBLIC" {
		t.Errorf("Expected toUpper('public') == 'PUBLIC'")
	}
}