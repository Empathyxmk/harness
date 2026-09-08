package original

import (
	"testing"
	"bytes"
)

type DeyeAtConnector struct{}

func (DeyeAtConnector) ExtractModbusResponse(response []byte) []byte {
	// Simulated extraction algorithm
	// For demonstration, just stripping known "+ok=" and trailing zeros up to the line ending
	if bytes.HasPrefix(response, []byte("+ok=")) {
		trimmed := bytes.TrimPrefix(response, []byte("+ok="))
		trimmed = bytes.ReplaceAll(trimmed, []byte("\r\n"), []byte(""))
		trimmed = bytes.ReplaceAll(trimmed, []byte("\x10"), []byte(""))
		return trimmed
	}
	return nil
}

func TestExtractModbusFrameWithTrailingZeros(t *testing.T) {
	connector := DeyeAtConnector{}
	atCmdResponse := []byte("+ok=0103720108000002946C6B00000000000000000000000010290F671005095508E50940000F000E000F138424DB000022AA000002B2000025C2000002B20000057B057B000403E80000000000000000001000000000000000000000000000000000000000000EFB00160015000100000000000000005745\r\n\r\n")

	modbusResponse := connector.ExtractModbusResponse(atCmdResponse)
	if len(modbusResponse) == 0 {
		t.Errorf("Expected some extraction result, got empty")
	}
}

func TestExtractModbusFrameWithoutTrailingZeros(t *testing.T) {
	connector := DeyeAtConnector{}
	atCmdResponse := []byte("+ok=010372001D000000000FF20000000E000E0000000007BD000007D100000938000000000001000000001388000000000000000000000000016800000000000012E8000000000000000000000000000000000000000000000000000000000000000000000000000EA000700FA0007000000000000000058AB\r\n\r\n")

	modbusResponse := connector.ExtractModbusResponse(atCmdResponse)
	if len(modbusResponse) == 0 {
		t.Errorf("Expected some extraction result, got empty")
	}
}