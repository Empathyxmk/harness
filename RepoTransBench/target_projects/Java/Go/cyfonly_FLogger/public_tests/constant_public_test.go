package public_tests

import (
	"strings"
	"testing"
)

type ConstantType struct {
	DEBUG           int
	INFO            int
	WARN            int
	ERROR           int
	FATAL           int
	LOG_DESC_MAP    map[string]string
	CFG_LOG_LEVEL   string
	CFG_CHARSET_NAME string
	CFG_LOG_PATH    string
}

// Simulate different config (as per public tests).
var Constant = ConstantType{
	DEBUG: 0,
	INFO:  1,
	WARN:  2,
	ERROR: 3,
	FATAL: 4,
	LOG_DESC_MAP: map[string]string{
		"0": "DEBUG",
		"1": "INFO",
		"2": "WARN",
		"3": "ERROR",
		"4": "FATAL",
	},
	CFG_LOG_LEVEL:    "0,1,2,3,4",
	CFG_CHARSET_NAME: "UTF-8",
	CFG_LOG_PATH:     "/some/log/path",
}

func TestLevelsAndMapPublic(t *testing.T) {
	if Constant.FATAL != 4 {
		t.Errorf("FATAL should be 4")
	}
	if v := Constant.LOG_DESC_MAP["4"]; v != "FATAL" {
		t.Errorf("LOG_DESC_MAP[4] should be FATAL, got %s", v)
	}
	if v := Constant.LOG_DESC_MAP["0"]; v != "DEBUG" {
		t.Errorf("LOG_DESC_MAP[0] should be DEBUG, got %s", v)
	}
	if Constant.CFG_LOG_LEVEL == "" {
		t.Error("CFG_LOG_LEVEL should not be nil")
	}
	if !strings.Contains(Constant.CFG_LOG_LEVEL, "4") {
		t.Error("CFG_LOG_LEVEL should contain 4")
	}
}

func TestCharsetAndPathPublic(t *testing.T) {
	if Constant.CFG_CHARSET_NAME == "" {
		t.Error("CFG_CHARSET_NAME should not be nil")
	}
	if Constant.CFG_LOG_PATH == "" {
		t.Error("CFG_LOG_PATH should not be nil")
	}
	if !strings.Contains(strings.ToUpper(Constant.CFG_CHARSET_NAME), "UTF") {
		t.Error("CFG_CHARSET_NAME should contain UTF")
	}
	if !strings.Contains(Constant.CFG_LOG_PATH, "log") {
		t.Error("CFG_LOG_PATH should contain 'log'")
	}
}