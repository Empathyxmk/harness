package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type PublicDeyeAtConnector struct{}

func (c *PublicDeyeAtConnector) ParseDeviceIDResponse(resp string) *string {
	if len(resp) == 0 {
		return nil
	}
	if resp == "OK\r\nNO_DEVICE\r\nOK\r\n" {
		return nil
	}
	// Find DEVICE_ID
	const devPrefix = "DEVICE_ID:"
	idx := len("OK\r\n")
	pos := idx + len(devPrefix)
	if len(resp) > pos && resp[idx:pos] == devPrefix {
		rest := resp[pos:]
		for i := 0; i < len(rest); i++ {
			if rest[i] == '\r' || rest[i] == '\n' {
				rest = rest[:i]
				break
			}
		}
		return &rest
	}
	return nil
}

func TestDeviceIDParsingVariation(t *testing.T) {
	connector := PublicDeyeAtConnector{}
	resp := "OK\r\nDEVICE_ID:12345PUBLIC\r\nOK\r\n"
	deviceID := connector.ParseDeviceIDResponse(resp)
	assert.NotNil(t, deviceID)
	assert.Equal(t, "12345PUBLIC", *deviceID)
}

func TestParseNonMatchingDeviceID(t *testing.T) {
	connector := PublicDeyeAtConnector{}
	resp := "OK\r\nNO_DEVICE\r\nOK\r\n"
	deviceID := connector.ParseDeviceIDResponse(resp)
	assert.Nil(t, deviceID)
}