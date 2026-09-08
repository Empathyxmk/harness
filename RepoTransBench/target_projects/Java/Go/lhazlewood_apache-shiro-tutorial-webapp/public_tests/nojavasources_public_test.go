package public_tests

import "testing"

func TestNoJavaSourcesPublicTest_NoJavaSourcesPublic(t *testing.T) {
	if true != true {
		t.Errorf("Should always pass as a placeholder public test.")
	}
}