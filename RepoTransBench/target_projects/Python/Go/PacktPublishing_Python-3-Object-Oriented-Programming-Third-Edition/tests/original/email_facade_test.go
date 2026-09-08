package original

import (
	"testing"
	"github.com/packt-oop3/goport/internal/chapter11"
)

type DummySMTP struct {
	Host     string
	Sent     bool
	LoggedIn interface{}
	LastArgs []interface{}
}

func (d *DummySMTP) Login(user, pw string) {
	d.LoggedIn = []string{user, pw}
}
func (d *DummySMTP) SendMail(fromEmail string, toList []string, msg string) {
	d.Sent = true
	d.LastArgs = []interface{}{fromEmail, toList, msg}
}

type DummyIMAP4 struct {
	Host     string
	Logged   interface{}
	Selected bool
	Fetched  bool
}

func (d *DummyIMAP4) Login(user, pw string) {
	d.Logged = []string{user, pw}
}
func (d *DummyIMAP4) Select() { d.Selected = true }
func (d *DummyIMAP4) Search(args ...interface{}) (string, [][]byte) {
	return "OK", [][]byte{[]byte("1 2")}
}
func (d *DummyIMAP4) Fetch(num []byte, what string) (string, [][]byte) {
	val := []byte("Message" + string(num))
	return "OK", [][]byte{val}
}

func TestSendEmailMonkeypatch(t *testing.T) {
	ef := chapter11.NewEmailFacade("host.com", "user", "pw")
	dummy := &DummySMTP{Host: "host.com"}
	chapter11.SMTPFactory = func(host string) chapter11.SMTPClient { return dummy }
	ef.SendEmail("dest@host.com", "Hi", "Message body")
	logged := dummy.LoggedIn.([]string)
	if logged[0] != "user" || logged[1] != "pw" {
		t.Error("Expected logged_in to be ('user', 'pw')")
	}
	if !dummy.Sent {
		t.Error("Email not sent")
	}
	if msg, ok := dummy.LastArgs[2].(string); !ok || !contains(msg, "From: user@host.com") {
		t.Error("Missing From: user@host.com in email message")
	}
	if to, ok := dummy.LastArgs[1].([]string); !ok || to[0] != "dest@host.com" {
		t.Error("Expected dest@host.com in recipient list")
	}
}

func TestSendEmailWithFullAddress(t *testing.T) {
	ef := chapter11.NewEmailFacade("host.com", "auser@domain.com", "pw")
	dummy := &DummySMTP{Host: "host.com"}
	chapter11.SMTPFactory = func(host string) chapter11.SMTPClient { return dummy }
	ef.SendEmail("to@host.com", "Subj", "Body")
	logged := dummy.LoggedIn.([]string)
	if logged[0] != "auser@domain.com" {
		t.Error("Expected auser@domain.com as from")
	}
	if !dummy.Sent {
		t.Error("Email not sent")
	}
	if msg, ok := dummy.LastArgs[2].(string); !ok || !contains(msg, "From: auser@domain.com") {
		t.Error("From field mismatch for full address")
	}
}

func TestGetInboxMonkeypatch(t *testing.T) {
	ef := chapter11.NewEmailFacade("s", "u", "p")
	dummy := &DummyIMAP4{Host: "s"}
	chapter11.IMAPFactory = func(host string) chapter11.IMAPClient { return dummy }
	result := ef.GetInbox()
	if dummy.Logged == nil {
		t.Error("Login on IMAP not called")
	}
	if !dummy.Selected {
		t.Error("IMAP select not called")
	}
	if len(result) != 2 {
		t.Errorf("Expected 2 messages in inbox, got %d", len(result))
	}
}