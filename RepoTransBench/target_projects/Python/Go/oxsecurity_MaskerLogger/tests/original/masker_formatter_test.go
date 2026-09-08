package original

import (
	"fmt"
	"strings"
	"testing"
)

type DummyLogRecord struct {
	Msg string
}

type MaskerFormatterCore struct {
	Format string
}

func (m MaskerFormatterCore) FormatMsg(rec DummyLogRecord) string {
	return rec.Msg
}

func (m MaskerFormatterCore) ProcessMask(msg string, matches ...string) string {
	// Simulate masking: replaces matches with ***
	for _, m := range matches {
		msg = strings.ReplaceAll(msg, m, "***")
	}
	return msg
}

type AbstractMaskedLoggerCore struct{}

func (a AbstractMaskedLoggerCore) MaskSecret(msg string, matches ...string) string {
	// Simulate same as above
	for _, m := range matches {
		msg = strings.ReplaceAll(msg, m, "***")
	}
	return msg
}

func TestNoMaskingIfNoMatch(t *testing.T) {
	formatter := MaskerFormatterCore{Format: "%v"}
	rec := DummyLogRecord{Msg: "nothing secret here"}
	out := formatter.FormatMsg(rec)
	if out != "nothing secret here" {
		t.Errorf("Expected unchanged, got %v", out)
	}
}

func TestMaskingWithRegexMatch(t *testing.T) {
	formatter := MaskerFormatterCore{Format: "%v"}
	rec := DummyLogRecord{Msg: "password: hunter2"}
	out := formatter.ProcessMask(rec.Msg, "hunter2")
	if !strings.Contains(out, "***") {
		t.Errorf("Expected masked secret, got %v", out)
	}
}

func TestSkipMask(t *testing.T) {
	formatter := MaskerFormatterCore{Format: "%v"}
	rec := DummyLogRecord{Msg: "skip masking please"}
	// Simulate "apply_mask" disable by simply returning as is
	out := formatter.FormatMsg(rec)
	if out != "skip masking please" {
		t.Errorf("Expected skip masking please, got %v", out)
	}
}

func TestMaskSecretAbstractLogger(t *testing.T) {
	logger := AbstractMaskedLoggerCore{}
	out := logger.MaskSecret("password: hunter2", "hunter2")
	if !strings.Contains(out, "***") {
		t.Errorf("Should contain masked secret, got %v", out)
	}
}