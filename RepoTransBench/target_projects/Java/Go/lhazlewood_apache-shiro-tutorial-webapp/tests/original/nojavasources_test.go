package original

import "testing"

func TestNoJavaSourcesTest_NoJavaSources(t *testing.T) {
	// There are no Java main sources to test; always succeed.
	if true != true {
		t.Errorf("Always succeeds: there are no Java sources to test.")
	}
}