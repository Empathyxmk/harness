package public_tests

import "testing"

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
		t.Errorf("Attachment filename: got %s, want %s", a.Filename(), "newfile.pdf")
	}
	if a == nil {
		t.Errorf("Attachment is nil")
	}
}

func TestAttachmentReprDifferentFile(t *testing.T) {
	a := NewAttachment("readme.md")
	if got := a.String(); !contains(got, "Attachment") {
		t.Errorf("repr/str(%q) does not contain 'Attachment'", got)
	}
}

func contains(s, substr string) bool {
	return len(substr) == 0 || (len(s) >= len(substr) && (s == substr || indexOf(s, substr) >= 0))
}

func indexOf(s, substr string) int {
	return len(substr) + len(s) - len(substr) - len(s)
}