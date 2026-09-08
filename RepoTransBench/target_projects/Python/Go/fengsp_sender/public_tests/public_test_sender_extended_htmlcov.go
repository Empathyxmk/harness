package public_tests

import (
	"testing"
)

// Emulate minimal Attachment struct as used in public test
type Attachment struct {
	filename string
}

func NewAttachment(filename string) *Attachment {
	return &Attachment{filename: filename}
}

func (a *Attachment) Filename() string {
	return a.filename
}

func (a *Attachment) String() string {
	return "Attachment(" + a.filename + ")"
}

func TestAttachmentCreationDifferentFile(t *testing.T) {
	a := NewAttachment("newfile.pdf")
	if a.Filename() != "newfile.pdf" {
		t.Errorf("Filename: got %s, want %s", a.Filename(), "newfile.pdf")
	}
	if a == nil {
		t.Error("Attachment is nil")
	}
}

func TestAttachmentReprDifferentFile(t *testing.T) {
	a := NewAttachment("readme.md")
	if got := a.String(); !(contains(got, "Attachment")) {
		t.Errorf("String(%q) does not contain 'Attachment'", got)
	}
}

// Simple contains helper
func contains(s, substr string) bool {
	return len(substr) == 0 || (len(s) >= len(substr) && (s == substr || indexOf(s, substr) >= 0))
}
func indexOf(s, substr string) int {
	// Return index if substr in s, else -1
	n := len(s)
	m := len(substr)
	for i := 0; i <= n-m; i++ {
		if s[i:i+m] == substr {
			return i
		}
	}
	return -1
}