package original

import (
	"reflect"
	"testing"
	. "fengsp_sender/tests/testutil"
)

// --- Mock/Stub Definitions based on interface signatures ---

// Dummy implementations for Mail, Message, Attachment, SenderError
type Mail struct{}
type Attachment struct {
	filename    string
	contentType string
	data        string
	disposition string
	headers     map[string]string
}

// Attachment creation helpers
func NewAttachment(details ...string) *Attachment {
	a := &Attachment{headers: map[string]string{}, disposition: "attachment"}
	if len(details) > 0 {
		a.filename = details[0]
	}
	return a
}

func (a *Attachment) Filename() string { return a.filename }
func (a *Attachment) String() string   { return "Attachment" }
func (a *Attachment) Disposition() string {
	if a.disposition == "" {
		return "attachment"
	}
	return a.disposition
}
func (a *Attachment) Headers() map[string]string { return a.headers }

// Message struct stub
type Message struct {
	subject      string
	fromaddr     interface{}
	to           map[string]bool
	cc           map[string]bool
	bcc          map[string]bool
	reply_to     string
	charset      string
	extraHeaders map[string]string
	mailOptions  []string
	rcptOptions  []string
	attachments  []*Attachment
	body         string
	html         string
	messageID    string
}

// SenderError dummy
type SenderError struct {
	msg string
}
func (e *SenderError) Error() string {
	return e.msg
}

// Helper Set for string set equality
func stringSet(s ...string) map[string]bool {
	m := map[string]bool{}
	for _, v := range s {
		m[v] = true
	}
	return m
}

// -- Test Logic --

func TestMessageSubject(t *testing.T) {
	msg := &Message{subject: "test"}
	AssertEqual(t, msg.subject, "test")
	msg = &Message{subject: "test", fromaddr: "from@example.com", to: stringSet("to@example.com")}
	if !Contains(msg.subject, msg.subject) {
		t.Errorf("subject not in string representation")
	}
}

func TestMessageTo(t *testing.T) {
	msg := &Message{fromaddr: "from@example.com", to: stringSet("to@example.com")}
	AssertDeepEqual(t, msg.to, stringSet("to@example.com"))
	if !ContainsMapKey(msg.to, "to@example.com") {
		t.Errorf("'to@example.com' not found in msg.to")
	}

	msg = &Message{to: stringSet("to01@example.com", "to02@example.com")}
	AssertDeepEqual(t, msg.to, stringSet("to01@example.com", "to02@example.com"))
}

func TestAttachmentDisposition(t *testing.T) {
	attach := NewAttachment()
	AssertEqual(t, attach.Disposition(), "attachment")
}

func TestAttachmentHeaders(t *testing.T) {
	attach := NewAttachment()
	AssertDeepEqual(t, attach.Headers(), map[string]string{})
}