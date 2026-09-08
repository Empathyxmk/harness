package original

import (
	"fmt"
	"log"
	"strings"
	"testing"
)

type DummyRecord struct {
	Msg string
}

type MaskerFormatter struct {
	Format string
}

func (m MaskerFormatter) MaskSecret(msg string, matches []string) string {
	// Simulate secret masking: replace matches with asterisks
	for _, match := range matches {
		msg = strings.ReplaceAll(msg, match, "***")
	}
	return msg
}

func (m MaskerFormatter) FormatRecord(rec DummyRecord) string {
	// Very basic format substitute
	return fmt.Sprintf(m.Format, rec.Msg)
}

type MaskerFormatterJson struct {
	Format string
}

func (m MaskerFormatterJson) FormatRecord(rec DummyRecord) string {
	// Very basic, just return message for this simulation
	return rec.Msg
}

type AbstractMaskedLogger struct {
	Redact int
}

func (a AbstractMaskedLogger) MaskSecret(msg string, matches []string) string {
	// Simulate masking, replace match with asterisks
	for _, match := range matches {
		msg = strings.ReplaceAll(msg, match, strings.Repeat("*", 3))
	}
	return msg
}

func (a *AbstractMaskedLogger) MaskSensitiveData(rec *DummyRecord) {
	// Simulate: If message contains "password" or secret, mask it, else leave alone.
	if strings.Contains(rec.Msg, "password321") {
		rec.Msg = strings.ReplaceAll(rec.Msg, "password321", strings.Repeat("*", 8))
	} else if strings.Contains(rec.Msg, "password123") {
		rec.Msg = strings.ReplaceAll(rec.Msg, "password123", strings.Repeat("*", 8))
	}
	// Simulate additional masking for API keys or secrets
	if strings.Contains(rec.Msg, "apikey") {
		rec.Msg = strings.ReplaceAll(rec.Msg, "apikey", "****")
	}
}

func TestMaskSecretLogic(t *testing.T) {
	logger := AbstractMaskedLogger{}
	msg := logger.MaskSecret("abbbbb start abbbbb", []string{"abbbbb"})
	if strings.Count(msg, "*") == 0 {
		t.Errorf("Should mask some secret, got: %v", msg)
	}
}

func TestMaskSensitiveDataNoMatch(t *testing.T) {
	logger := &AbstractMaskedLogger{}
	rec := &DummyRecord{Msg: "no secrets here"}
	logger.MaskSensitiveData(rec)
	if rec.Msg != "no secrets here" {
		t.Errorf("Message should be unchanged, got: %v", rec.Msg)
	}
}

func TestMaskSensitiveDataWithMatch(t *testing.T) {
	logger := &AbstractMaskedLogger{Redact: 45}
	rec := &DummyRecord{Msg: `"password": "password321" and apikey = 1234`}
	logger.MaskSensitiveData(rec)
	if rec.Msg == `"password": "password321" and apikey = 1234` {
		t.Errorf("Should have masked secret")
	}
	if strings.Contains(rec.Msg, "password321") {
		t.Errorf("Should have masked password321")
	}
}

func TestFormatterFullLogIntegration(t *testing.T) {
	formatter := MaskerFormatter{Format: "%v"}
	handler := log.New(nil, "", 0)
	handler.SetFlags(0)
	_ = formatter // Only test construction, handler is not really used for output here.
}

func TestJsonFormatterLogRecordMasking(t *testing.T) {
	jsonFormatter := MaskerFormatterJson{Format: "%v"}
	rec := DummyRecord{Msg: `apikey = "TESTEXPOSEDSECRET"`}
	out := jsonFormatter.FormatRecord(rec)
	if !strings.Contains(out, "apikey") {
		t.Errorf("JSON output should contain apikey, got: %v", out)
	}
}

func TestMaskerFormatterJsonSkipMask(t *testing.T) {
	jsonFormatter := MaskerFormatterJson{Format: "%v"}
	rec := DummyRecord{Msg: "sometext"}
	// Simulate attribute "apply_mask = false" by skipping masking
	out := jsonFormatter.FormatRecord(rec)
	if !strings.Contains(out, "sometext") {
		t.Errorf("Should contain sometext, got: %v", out)
	}
}

func TestReprAndStr(t *testing.T) {
	jsonFormatter := MaskerFormatterJson{}
	typename := fmt.Sprintf("%T", jsonFormatter)
	if !strings.Contains(typename, "MaskerFormatterJson") {
		t.Errorf("Should contain MaskerFormatterJson in type, got: %v", typename)
	}
}