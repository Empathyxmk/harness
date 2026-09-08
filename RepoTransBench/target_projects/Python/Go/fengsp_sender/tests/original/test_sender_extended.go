package original

import (
	"testing"
	"fengsp_sender/tests/testutil"
)

// Attachment dummy struct until full implementation exists elsewhere
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

func TestAttachmentCreation(t *testing.T) {
	a := NewAttachment("test.txt")
	if a.Filename() != "test.txt" {
		t.Errorf("Attachment filename: got %s, want %s", a.Filename(), "test.txt")
	}
	if a == nil {
		t.Errorf("Attachment was nil")
	}
}

func TestAttachmentRepr(t *testing.T) {
	a := NewAttachment("test.txt")
	if got := a.String(); !(testutil.Contains(got, "Attachment")) {
		t.Errorf("repr/str(%q) does not contain 'Attachment'", got)
	}
}