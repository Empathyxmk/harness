package tests

import (
	"os"
	"testing"
)

func TestSetupPyExists(t *testing.T) {
	if _, err := os.Stat("setup.py"); os.IsNotExist(err) {
		t.Errorf("setup.py does not exist")
	}
}