package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsTestPublic_ConstructorAndGettersDifferentData(t *testing.T) {
	sms := NewSms("PublicTestContact", "+10987654321", "Hello Public Test!", 1440000000, DRAFT)
	assert.Equal(t, "PublicTestContact", sms.GetContact())
	assert.Equal(t, "+10987654321", sms.GetAddress())
	assert.Equal(t, "Hello Public Test!", sms.GetMessage())
	assert.Equal(t, int64(1440000000), sms.GetTime())
	assert.Equal(t, DRAFT, sms.GetType())
}

func TestSmsTestPublic_SmsEqualsDifferentData(t *testing.T) {
	sms1 := NewSms("AA", "BB", "CC", 55555555, OUTBOX)
	sms2 := NewSms("AA", "BB", "CC", 55555555, OUTBOX)
	assert.Equal(t, sms1, sms2)
}

func TestSmsTestPublic_SmsToStringDifferentData(t *testing.T) {
	sms := NewSms("XY", "ZZ", "MessageTest", 66778899, DRAFT)
	str := sms.String()
	assert.Contains(t, str, "XY")
	assert.Contains(t, str, "ZZ")
	assert.Contains(t, str, "MessageTest")
	assert.Contains(t, str, "66778899")
	assert.Contains(t, str, "DRAFT")
}