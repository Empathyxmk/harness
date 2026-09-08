package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSmsCursorParserPublic_ParseSingleSmsRow(t *testing.T) {
	rows := [][]string{
		{"+3450000000", "Text from Eve", "Eve", "1600000000000", "3"},
	}
	smses := SmsCursorParser{}.Parse(rows)
	assert.Equal(t, 1, len(smses))
	sms := smses[0]
	assert.Equal(t, "+3450000000", sms.GetAddress())
	assert.Equal(t, "Text from Eve", sms.GetMessage())
	assert.Equal(t, "Eve", sms.GetContact())
	assert.Equal(t, int64(1600000000000), sms.GetTime())
	assert.Equal(t, DRAFT, sms.GetType())
}

func TestSmsCursorParserPublic_ParseMultipleSmsRows(t *testing.T) {
	rows := [][]string{
		{"123", "Bulk1", "A", "1600001", "1"},
		{"456", "Bulk2", "B", "1600002", "2"},
	}
	smses := SmsCursorParser{}.Parse(rows)
	assert.Equal(t, 2, len(smses))
	assert.Equal(t, "Bulk1", smses[0].GetMessage())
	assert.Equal(t, SENT, smses[1].GetType())
}