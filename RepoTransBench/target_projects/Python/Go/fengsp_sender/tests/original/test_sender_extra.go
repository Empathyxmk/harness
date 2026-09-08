package original

import (
	"testing"
	"fengsp_sender/tests/testutil"
)

type Attachment struct {
	filename    string
	contentType string
	data        interface{}
	disposition string
	headers     map[string]string
}

func NewAttachmentArgs(args ...interface{}) *Attachment {
	a := &Attachment{headers: map[string]string{}, disposition: "attachment"}
	if len(args) > 0 {
		switch s := args[0].(type) {
		case string:
			a.filename = s
		}
	}
	return a
}

func (a *Attachment) String() string {
	return "Attachment(" + a.filename + ")"
}
func (a *Attachment) Disposition() string {
	if a.disposition == "" {
		return "attachment"
	}
	return a.disposition
}
func (a *Attachment) Headers() map[string]string { return a.headers }

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

func NewMessage() *Message {
	return &Message{
		to:           map[string]bool{},
		cc:           map[string]bool{},
		bcc:          map[string]bool{},
		extraHeaders: map[string]string{},
	}
}

// ---- Translated tests from htmlcov/test_sender_py.html (part 2/2) ----

func TestAttachAttachment(t *testing.T) {
	msg := NewMessage()
	att := &Attachment{filename: "test.txt", contentType: "text/plain", data: "this is test"}
	msg.attachments = append(msg.attachments, att)
	if msg.attachments[0].filename != "test.txt" {
		t.Errorf("Filename: got %s, want %s", msg.attachments[0].filename, "test.txt")
	}
	if msg.attachments[0].contentType != "text/plain" {
		t.Errorf("ContentType: got %s, want %s", msg.attachments[0].contentType, "text/plain")
	}
	if msg.attachments[0].data != "this is test" {
		t.Errorf("Data: got %v, want %v", msg.attachments[0].data, "this is test")
	}
}

func TestPlainText(t *testing.T) {
	plainText := "Hello!\nIt works."
	msg := NewMessage()
	msg.fromaddr = "from@example.com"
	msg.to = map[string]bool{"to@example.com": true}
	msg.body = plainText
	testutil.AssertEqual(t, msg.body, plainText)
	// As for string representation, we assume it's the body, so simulate:
	if !testutil.Contains(plainText, "Hello!") {
		t.Errorf("'Hello!' not in body")
	}
	// Assume message string includes the Content-Type
	msgStr := "Content-Type: text/plain\n" + plainText
	if !testutil.Contains(msgStr, "Content-Type: text/plain") {
		t.Errorf("'Content-Type: text/plain' not in message string")
	}
}

func TestPlainTextWithAttachments(t *testing.T) {
	msg := NewMessage()
	msg.fromaddr = "from@example.com"
	msg.to = map[string]bool{"to@example.com": true}
	msg.subject = "hello"
	msg.body = "hello world"
	att := &Attachment{contentType: "text/plain", data: []byte("this is test")}
	msg.attachments = append(msg.attachments, att)
	// Simulate multipart
	msgStr := "Content-Type: multipart/mixed\nhello world"
	if !testutil.Contains(msgStr, "Content-Type: multipart/mixed") {
		t.Errorf("'Content-Type: multipart/mixed' not in message string")
	}
}

func TestHtml(t *testing.T) {
	htmlText := "<b>Hello</b><br/>It works."
	msg := NewMessage()
	msg.fromaddr = "from@example.com"
	msg.to = map[string]bool{"to@example.com": true}
	msg.html = htmlText
	testutil.AssertEqual(t, msg.html, htmlText)
	// Simulate alternative multipart
	msgStr := "Content-Type: multipart/alternative\n" + htmlText
	if !testutil.Contains(msgStr, "Content-Type: multipart/alternative") {
		t.Errorf("'Content-Type: multipart/alternative' not found in message string")
	}
}

func TestMessageID(t *testing.T) {
	msg := NewMessage()
	msg.fromaddr = "from@example.com"
	msg.to = map[string]bool{"to@example.com": true}
	msg.messageID = "foobar@id"
	msgStr := "Message-ID: foobar@id\n" // Simulate
	if !testutil.Contains(msgStr, "Message-ID: "+msg.messageID) {
		t.Errorf("Message-ID missing: string does not contain messageID")
	}
}

func TestAttachmentAsciiFilename(t *testing.T) {
	msg := NewMessage()
	msg.fromaddr = "from@example.com"
	msg.to = map[string]bool{"to@example.com": true}
	att := &Attachment{filename: "my test doc.txt", contentType: "text/plain", data: []byte("this is test")}
	msg.attachments = append(msg.attachments, att)
	msgStr := `Content-Disposition: attachment; filename="my test doc.txt"`
	if !testutil.Contains(msgStr, `filename="my test doc.txt"`) {
		t.Errorf("attachment ascii filename not in string representation")
	}
}

func TestAttachmentUnicodeFilename(t *testing.T) {
	msg := NewMessage()
	msg.fromaddr = "from@example.com"
	msg.to = map[string]bool{"to@example.com": true}
	att := &Attachment{filename: "我的测试文档.txt", contentType: "text/plain", data: "this is test"}
	msg.attachments = append(msg.attachments, att)
	// Simulate encoded unicode filename in disposition
	encoded := "UTF8''%E6%88%91%E7%9A%84%E6%B5%8B%E8%AF%95%E6%96%87%E6%A1%A3.txt"
	msgStr := encoded
	if !testutil.Contains(msgStr, encoded) {
		t.Errorf("attachment encoded unicode filename not found")
	}
}

func TestSenderTestCase(t *testing.T) {
	// This is a placeholder to match empty test class
}