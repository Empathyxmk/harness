package original

import (
	"os"
	"path/filepath"
	"testing"
)

func TestDemoFileExists(t *testing.T) {
	demoPy := filepath.Join(filepath.Dir("../demo"), "demo.py")
	if _, err := os.Stat(demoPy); os.IsNotExist(err) {
		t.Fatalf("demo.py does not exist at %s", demoPy)
	}
}

func TestDemoPngExists(t *testing.T) {
	demoPng := filepath.Join(filepath.Dir("../demo"), "demo_01.png")
	if _, err := os.Stat(demoPng); os.IsNotExist(err) {
		t.Fatalf("demo_01.png does not exist at %s", demoPng)
	}
}