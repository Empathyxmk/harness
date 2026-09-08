package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsType_FromValueReceived(t *testing.T) {
	assert.Equal(t, RECEIVED, SmsTypeFromValue(1))
}
func TestSmsType_FromValueSent(t *testing.T) {
	assert.Equal(t, SENT, SmsTypeFromValue(2))
}
func TestSmsType_FromValueUnknown(t *testing.T) {
	assert.Equal(t, UNKNOWN, SmsTypeFromValue(-1))
}
func TestSmsType_FromValueInvalid(t *testing.T) {
	assert.Panics(t, func() { SmsTypeFromValue(5) })
}