package public_tests

import (
	"testing"
)

func TestAdditionIsCorrectPublic_App(t *testing.T) {
	// From ExamplePublicUnitTest.java (app)
	if 5+3 != 8 {
		t.Errorf("Expected 5+3==8, got %d", 5+3)
	}
}
func TestAdditionIsCorrectPublic_Library(t *testing.T) {
	// From ExamplePublicUnitTest.java (library)
	if 7+3 != 10 {
		t.Errorf("Expected 7+3==10, got %d", 7+3)
	}
}