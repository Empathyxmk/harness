package original

import (
	"testing"
)

func TestAdditionIsCorrect_App(t *testing.T) {
	// From app/src/test/java/com/hankkin/taobaodetaildemo/ExampleUnitTest.java
	if 2+2 != 4 {
		t.Errorf("Expected 2+2==4, got %d", 2+2)
	}
}

func TestAdditionIsCorrect_Library(t *testing.T) {
	// From library/src/test/java/com/hankkin/library/ExampleUnitTest.java
	if 2+2 != 4 {
		t.Errorf("Expected 2+2==4, got %d", 2+2)
	}
}