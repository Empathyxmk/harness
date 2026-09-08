package original

import (
	"testing"
)

// Translated from: app/src/test/java/com/cheng/sample/ExampleUnitTest.java
func TestAdditionIsCorrect(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("expected 4, got %d", 2+2)
	}
}

// Translated from: channelview/src/test/java/com/cheng/channel/ExampleUnitTest.java
func TestChannelAdditionIsCorrect(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("expected 4, got %d", 2+2)
	}
}