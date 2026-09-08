package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsTypePublic_ValueOf(t *testing.T) {
	typ := SmsTypeValueOf("INBOX")
	assert.Equal(t, INBOX, typ)
	typ = SmsTypeValueOf("SENT")
	assert.Equal(t, SENT, typ)
}

func TestSmsTypePublic_OrdinalDifferentFromTest(t *testing.T) {
	assert.NotEqual(t, "SENT", OUTBOX.String())
}

func TestSmsTypePublic_ValuesArrayLength(t *testing.T) {
	values := SmsTypeValues()
	assert.True(t, len(values) > 1)
}