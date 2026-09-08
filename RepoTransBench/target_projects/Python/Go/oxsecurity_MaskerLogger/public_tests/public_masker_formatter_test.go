package public_tests

import (
	"strings"
	"testing"
)

type DummyRecordMF struct {
	Msg string
}

type MaskerFormatterMF struct {
	Format string
}

func (m MaskerFormatterMF) FormatMsg(r DummyRecordMF) string {
	return r.Msg
}

func (m MaskerFormatterMF) MaskMsg(msg string, matches ...string) string {
	for _, m := range matches {
		msg = strings.ReplaceAll(msg, m, "***")
	}
	return msg
}

type MaskerFormatterJsonMF struct {
	Format string
}

func (m MaskerFormatterJsonMF) FormatMsg(r DummyRecordMF) string {
	return r.Msg
}

type AbstractMaskedLoggerMF struct{}

func (a AbstractMaskedLoggerMF) MaskSecret(msg string, matches ...string) string {
	for _, m := range matches {
		msg = strings.ReplaceAll(msg, m, "***")
	}
	return msg
}

func TestNoMaskingIfNoMatchPublic(t *testing.T) {
	formatter := MaskerFormatterMF{Format: "%v"}
	rec := DummyRecordMF{Msg: "12345 is a safe message"}
	out := formatter.FormatMsg(rec)
	if out != "12345 is a safe message" {
		t.Errorf("Expected unchanged, got %v", out)
	}
}

func TestMaskingWithRegexMatchPublic(t *testing.T) {
	formatter := MaskerFormatterMF{Format: "%v"}
	rec := DummyRecordMF{Msg: "apikey: mytopsecret"}
	out := formatter.MaskMsg(rec.Msg, "mytopsecret")
	if !strings.Contains(out, "***") {
		t.Errorf("Expected masked secret, got %v", out)
	}
}

func TestSkipMaskPublic(t *testing.T) {
	formatter := MaskerFormatterJsonMF{Format: "%v"}
	rec := DummyRecordMF{Msg: "nothing to mask here"}
	out := formatter.FormatMsg(rec)
	if out != "nothing to mask here" {
		t.Errorf("Expected nothing to mask here, got: %v", out)
	}
}

func TestMaskSecretPublic(t *testing.T) {
	logger := AbstractMaskedLoggerMF{}
	out := logger.MaskSecret("apikey: mytopsecret", "mytopsecret")
	if !strings.Contains(out, "***") {
		t.Errorf("Should contain masked secret, got %v", out)
	}
}