package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsObserverPublic_OnSmsReceivedCallbackDiffData(t *testing.T) {
	trigger := false
	var listener SmsListener = &struct{SmsListener}{
	}
	listener = &fakeSmsListener{onReceived: func(sms Sms) {
		assert.Equal(t, "ObserverName", sms.GetContact())
		assert.Equal(t, "+999999999", sms.GetAddress())
		assert.Equal(t, "ObserverMsg", sms.GetMessage())
		trigger = true
	}}
	sms := NewSms("ObserverName", "+999999999", "ObserverMsg", 1987654321, SENT)
	listener.OnSmsReceived(sms)
	assert.True(t, trigger)
}

type fakeSmsListener struct {
	onReceived func(Sms)
}

func (f *fakeSmsListener) OnSmsReceived(sms Sms) {
	f.onReceived(sms)
}
func (f *fakeSmsListener) OnSmsSent(sms Sms) {}