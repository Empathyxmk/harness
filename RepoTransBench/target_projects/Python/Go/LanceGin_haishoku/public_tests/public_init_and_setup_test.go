package public_tests

import (
	"os"
	"testing"
)

func TestInitModuleExists(t *testing.T) {
	if _, err := os.Stat("haishoku/init.go"); os.IsNotExist(err) {
		t.Errorf("haishoku/init.go does not exist")
	}
}

func TestAlgModuleExists(t *testing.T) {
	if _, err := os.Stat("haishoku/alg.go"); os.IsNotExist(err) {
		t.Errorf("haishoku/alg.go does not exist")
	}
}