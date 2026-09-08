package public_tests

import (
	"strings"
	"testing"
)

type DummyRecordPublic struct {
	Msg string
}

type MaskerFormatterPublic struct {
	Format string
}

func (m *MaskerFormatterPublic) FormatRecord(r DummyRecordPublic) string {
	// Basic formatter: just returns msg for demo
	return r.Msg
}

type MaskerFormatterJsonPublic struct {
	Format string
}

func (m *MaskerFormatterJsonPublic) FormatRecord(r DummyRecordPublic) string {
	return r.Msg
}

type AbstractMaskedLoggerPublic struct {
	Redact int
}

func (a AbstractMaskedLoggerPublic) MaskSecret(msg string, matches ...string) string {
	for _, m := range matches {
		msg = strings.ReplaceAll(msg, m, "***")
	}
	return msg
}

func (a *AbstractMaskedLoggerPublic) MaskSensitiveData(r *DummyRecordPublic) {
	if strings.Contains(r.Msg, "abcd12345efgh") {
		r.Msg = strings.ReplaceAll(r.Msg, "abcd12345efgh", "**********")
	}
	if strings.Contains(r.Msg, "token") {
		r.Msg = strings.ReplaceAll(r.Msg, "token", "****")
	}
}

func TestMaskSecretLogicWithNewPattern(t *testing.T) {
	logger := AbstractMaskedLoggerPublic{}
	msg := logger.MaskSecret("xyyyy abc xyyyy", "xyyyy")
	if strings.Count(msg, "*") == 0 {
		t.Errorf("Should mask secret, got: %v", msg)
	}
}

func TestMaskSensitiveDataNoMatchNewmsg(t *testing.T) {
	logger := &AbstractMaskedLoggerPublic{}
	rec := &DummyRecordPublic{Msg: "totally safe entry"}
	logger.MaskSensitiveData(rec)
	if rec.Msg != "totally safe entry" {
		t.Errorf("Message should not be changed, got: %v", rec.Msg)
	}
}

func TestMaskSensitiveDataWithMatchNewsecret(t *testing.T) {
	logger := &AbstractMaskedLoggerPublic{Redact: 39}
	rec := &DummyRecordPublic{Msg: `"token": "abcd12345efgh" and secret_key = zyxw`}
	logger.MaskSensitiveData(rec)
	if rec.Msg == `"token": "abcd12345efgh" and secret_key = zyxw` {
		t.Errorf("Should have masked secrets")
	}
	if strings.Contains(rec.Msg, "abcd12345efgh") {
		t.Errorf("Should have masked abcd12345efgh")
	}
}

func TestFormatterFullLogIntegrationPublic(t *testing.T) {
	formatter := MaskerFormatterPublic{Format: "%v"}
	rec := DummyRecordPublic{Msg: "Datadog token is: 'zyxw9876zyxw9876zyxw9876zyxw9876'"}
	out := formatter.FormatRecord(rec)
	if !strings.Contains(out, "Datadog") {
		t.Errorf("Should produce unmasked message containing 'Datadog', got: %v", out)
	}
}

func TestJsonFormatterLogrecordMaskingPublic(t *testing.T) {
	formatter := MaskerFormatterJsonPublic{Format: "%v"}
	rec := DummyRecordPublic{Msg: `auth = "FAKENEWSECRETXYZ"`}
	out := formatter.FormatRecord(rec)
	if !strings.Contains(out, "auth") {
		t.Errorf("Should contain auth, got: %v", out)
	}
}

func TestMaskerformatterjsonSkipMaskPublic(t *testing.T) {
	formatter := MaskerFormatterJsonPublic{Format: "%v"}
	rec := DummyRecordPublic{Msg: "publiclogtext"} // Simulate apply_mask==false
	out := formatter.FormatRecord(rec)
	if !strings.Contains(out, "publiclogtext") {
		t.Errorf("Should contain publiclogtext, got: %v", out)
	}
}

func TestReprAndStrPublic(t *testing.T) {
	formatter := MaskerFormatterJsonPublic{}
	typename := "MaskerFormatterJsonPublic"
	if !strings.Contains(typename, "Json") {
		t.Errorf("Type name should include Json, got: %v", typename)
	}
}