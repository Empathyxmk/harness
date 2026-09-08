package original

import (
	"strings"
	"testing"
)

type ConstantType struct {
	DEBUG          int
	INFO           int
	WARN           int
	ERROR          int
	FATAL          int
	LOG_DESC_MAP   map[string]string
	CFG_LOG_LEVEL  string
	CFG_CHARSET_NAME string
	CFG_LOG_PATH   string
}

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
	CFG_LOG_PATH:     "/var/log",
}

func TestLogLevels(t *testing.T) {
	if Constant.DEBUG != 0 {
		t.Errorf("Expected DEBUG to be 0")
	}
	if Constant.INFO != 1 {
		t.Errorf("Expected INFO to be 1")
	}
	if Constant.WARN != 2 {
		t.Errorf("Expected WARN to be 2")
	}
	if Constant.ERROR != 3 {
		t.Errorf("Expected ERROR to be 3")
	}
	if Constant.FATAL != 4 {
		t.Errorf("Expected FATAL to be 4")
	}
}

func TestLogDescMap(t *testing.T) {
	if v, ok := Constant.LOG_DESC_MAP["0"]; !ok || v != "DEBUG" {
		t.Errorf("LOG_DESC_MAP[0]: expected DEBUG, got %v", v)
	}
	if v, ok := Constant.LOG_DESC_MAP["1"]; !ok || v != "INFO" {
		t.Errorf("LOG_DESC_MAP[1]: expected INFO, got %v", v)
	}
	if v, ok := Constant.LOG_DESC_MAP["2"]; !ok || v != "WARN" {
		t.Errorf("LOG_DESC_MAP[2]: expected WARN, got %v", v)
	}
	if v, ok := Constant.LOG_DESC_MAP["3"]; !ok || v != "ERROR" {
		t.Errorf("LOG_DESC_MAP[3]: expected ERROR, got %v", v)
	}
	if v, ok := Constant.LOG_DESC_MAP["4"]; !ok || v != "FATAL" {
		t.Errorf("LOG_DESC_MAP[4]: expected FATAL, got %v", v)
	}
}

func TestConfigDefaults(t *testing.T) {
	if Constant.CFG_LOG_LEVEL == "" {
		t.Errorf("CFG_LOG_LEVEL should not be empty")
	}
	if !strings.EqualFold(Constant.CFG_CHARSET_NAME, "UTF-8") {
		t.Errorf("CFG_CHARSET_NAME should be 'UTF-8' (case insensitive)")
	}
	if Constant.CFG_LOG_PATH == "" {
		t.Errorf("CFG_LOG_PATH should not be empty")
	}
}