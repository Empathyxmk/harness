package public_tests

import (
	"testing"
)

// Translated from: app/src/test/java/com/cheng/sample/ExampleUnitPublicTest.java
func TestSubtractionIsCorrect(t *testing.T) {
	if 5-3 != 2 {
		t.Errorf("expected 2, got %d", 5-3)
	}
}

// Translated from: channelview/src/test/java/com/cheng/channel/ExampleUnitPublicTest.java
func TestMultiplicationIsCorrect(t *testing.T) {
	if 3*5 != 15 {
		t.Errorf("expected 15, got %d", 3*5)
	}
}