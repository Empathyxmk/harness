package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsStoragePublic_StoreAndGetSingleSms(t *testing.T) {
	smsStorage := NewSmsStorage()
	sms := NewSms("Charlie", "+1987654321", "Hey there!", 1357924680, INBOX)
	smsStorage.StoreSms(sms)
	retrieved := smsStorage.GetAllSms()
	assert.Equal(t, 1, len(retrieved))
	out := retrieved[0]
	assert.Equal(t, "Charlie", out.GetContact())
	assert.Equal(t, "+1987654321", out.GetAddress())
	assert.Equal(t, "Hey there!", out.GetMessage())
}

func TestSmsStoragePublic_StoreMultipleSms(t *testing.T) {
	smsStorage := NewSmsStorage()
	s1 := NewSms("Delta", "+1234509876", "First msg", 1000000100, SENT)
	s2 := NewSms("Echo", "+1987654322", "Second msg", 1000000200, OUTBOX)
	smsStorage.StoreSms(s1)
	smsStorage.StoreSms(s2)
	list := smsStorage.GetAllSms()
	assert.Equal(t, 2, len(list))
	assert.Equal(t, "First msg", list[0].GetMessage())
	assert.Equal(t, "Second msg", list[1].GetMessage())
}

func TestSmsStoragePublic_StorageIsCleared(t *testing.T) {
	smsStorage := NewSmsStorage()
	smsStorage.StoreSms(NewSms("Foxtrot", "+1324354657", "To clear", 1234000000, DRAFT))
	smsStorage.ClearAll()
	assert.True(t, len(smsStorage.GetAllSms()) == 0)
}