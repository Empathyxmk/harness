package public_tests

import (
	"os"
	"testing"
)

func TestDemoPngExists(t *testing.T) {
	if _, err := os.Stat("demo/demo_01.png"); os.IsNotExist(err) {
		t.Errorf("demo/demo_01.png does not exist")
	}
}