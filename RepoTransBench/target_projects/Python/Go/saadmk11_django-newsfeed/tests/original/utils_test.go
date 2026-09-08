package original

import (
	"errors"
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// Fake for mail sending
type MailMessage struct {
	Subject string
	To      []string
	Body    string
}

type Outbox struct {
	Messages []MailMessage
}

func (o *Outbox) Add(msg MailMessage) {
	o.Messages = append(o.Messages, msg)
}

func (o *Outbox) Reset() {
	o.Messages = []MailMessage{}
}

var mailOutbox = &Outbox{}

func sendSubscriptionVerificationEmail(url string, email string) {
	mailOutbox.Add(MailMessage{
		Subject: "Please Confirm Your Subscription",
		To:      []string{email},
		Body:    "Visit " + url,
	})
}

type Newsletter struct{ Subject string }
type Subscriber struct {
	EmailAddress string
	Subscribed   bool
	Verified     bool
}

type NewsletterEmailSender struct {
	connection struct {
		SendMessages func() error
	}
	batchSize int
}

func (s *NewsletterEmailSender) sendEmails() error {
	if s.connection.SendMessages != nil {
		return s.connection.SendMessages()
	}
	return nil
}

type LoggerMock struct {
	mock.Mock
}

func (l *LoggerMock) Error(args ...interface{}) {
	l.Called(args)
}

func TestSendSubscriptionVerificationEmail(t *testing.T) {
	mailOutbox.Reset()
	sub := Subscriber{EmailAddress: "test@mail", Subscribed: false, Verified: false}
	sendSubscriptionVerificationEmail("/verify/test-token/", sub.EmailAddress)

	assert.Equal(t, 1, len(mailOutbox.Messages))
	assert.Equal(t, "Please Confirm Your Subscription", mailOutbox.Messages[0].Subject)
	assert.Equal(t, []string{sub.EmailAddress}, mailOutbox.Messages[0].To)
	assert.Contains(t, mailOutbox.Messages[0].Body, "/verify/test-token/")
}

func TestSendNewsletterEmail_WithError(t *testing.T) {
	mockLogger := new(LoggerMock)
	mockLogger.On("Error", mock.Anything).Return()
	sender := &NewsletterEmailSender{}
	sender.connection.SendMessages = func() error {
		mockLogger.Error(errors.New("fail"))
		return errors.New("fail")
	}
	_ = sender.sendEmails()
	mockLogger.AssertCalled(t, "Error", mock.Anything)
}

func TestCheckAjax_IsAjax(t *testing.T) {
	isAjax := func(headers map[string]string) bool {
		return headers["X-Requested-With"] == "XMLHttpRequest"
	}
	headers := map[string]string{
		"X-Requested-With": "XMLHttpRequest",
	}
	assert.True(t, isAjax(headers))
}

func TestCheckAjax_IsNotAjax(t *testing.T) {
	isAjax := func(headers map[string]string) bool {
		return headers["X-Requested-With"] == "XMLHttpRequest"
	}
	headers := map[string]string{}
	assert.False(t, isAjax(headers))
}