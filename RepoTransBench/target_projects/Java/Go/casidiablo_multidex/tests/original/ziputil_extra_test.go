package original

import (
	"os"
	"testing"
)

func TestFindCentralDirectoryShortFile(t *testing.T) {
	// This should produce an error; attempt to read a 1-byte file as a zip
	tmp, err := os.CreateTemp("", "shortzip*.zip")
	if err != nil {
		t.Fatal(err)
	}
	tmp.Close()
	defer os.Remove(tmp.Name())
	err = os.Truncate(tmp.Name(), 1)
	if err != nil {
		t.Fatal(err)
	}
	_, err = os.Open(tmp.Name()) // Tries to open, but reading will fail for a zip.Reader
	if err != nil {
		t.Fatal("Should still be able to open, but if parsing as zip it should fail (simulating exception)")
	}
	// Try parsing it as a zip file, expect failure
	_, err = os.Stat(tmp.Name())
	if err != nil {
		t.Fatal("Temporary file vanished")
	}
	// In Go zip.NewReader expects a size >= 22 bytes, fails on short file
	f, err := os.Open(tmp.Name())
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	// This should fail
	_, err = f.Read(make([]byte, 100))
}