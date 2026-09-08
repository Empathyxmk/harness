package original

import (
	"os"
	"testing"
	"newbeginning6subdir/org/example"
)

func TestTxtFileApi(t *testing.T) {
	fname := "txtfiletest.txt"
	text := "hello\nworld"
	tf := example.TxtFile{}
	// Write
	err := tf.Write(fname, text, false)
	if err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	// Read
	lines, err := tf.Read(fname)
	if err != nil {
		t.Fatalf("Read failed: %v", err)
	}
	if len(lines) != 2 {
		t.Fatalf("Expected 2 lines, got %v", len(lines))
	}
	if lines[0] != "hello" {
		t.Errorf("First line wrong: got %q", lines[0])
	}
	if lines[1] != "world" {
		t.Errorf("Second line wrong: got %q", lines[1])
	}
	_ = os.Remove(fname)
}