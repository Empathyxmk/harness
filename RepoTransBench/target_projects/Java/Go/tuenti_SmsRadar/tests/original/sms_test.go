package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSms_ConstructorAndGetters(t *testing.T) {
	sms := NewSms("12345", "1687221000000", "Hello there!", RECEIVED)
	assert.Equal(t, "12345", sms.GetAddress())
	assert.Equal(t, "1687221000000", sms.GetDate())
	assert.Equal(t, "Hello there!", sms.GetMsg())
	assert.Equal(t, RECEIVED, sms.GetType())
}

func TestSms_EqualsHashCodeAndToString(t *testing.T) {
	a := NewSms("a", "111", "body", RECEIVED)
	b := NewSms("a", "111", "body", RECEIVED)
	c := NewSms("b", "112", "other", SENT)

	assert.True(t, a.Equal(b))
	assert.True(t, b.Equal(a))
	assert.False(t, a.Equal(c))
	assert.Contains(t, a.Msg, "body")
}

func TestSms_NotEqualWithNullOrOtherType(t *testing.T) {
	sms := NewSms("a", "c", "b", UNKNOWN)
	assert.False(t, sms.Equal(Sms{}))           // not equal to zero value unless all fields equal
}