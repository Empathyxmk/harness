package public_tests

import (
	"os"
	"testing"
	"newbeginning6subdir/org/example"
)

func TestTxtFileApiPublic(t *testing.T) {
	fname := "txtfilepublictest.txt"
	text := "foo\nbar\nbaz"
	tf := example.TxtFile{}
	if err := tf.Write(fname, text, false); err != nil {
		t.Fatalf("Write failed: %v", err)
	}

	lines, err := tf.Read(fname)
	if err != nil {
		t.Fatalf("Read failed: %v", err)
	}
	if lines == nil {
		t.Fatalf("Read returned nil")
	}
	if len(lines) != 3 {
		t.Fatalf("Expected 3 lines, got %v", len(lines))
	}
	if lines[0] != "foo" {
		t.Errorf("Line 0 wrong: got %q", lines[0])
	}
	if lines[1] != "bar" {
		t.Errorf("Line 1 wrong: got %q", lines[1])
	}
	if lines[2] != "baz" {
		t.Errorf("Line 2 wrong: got %q", lines[2])
	}
	_ = os.Remove(fname)
}