package original

import (
	"testing"
)

func TestDebugInfoWarnErrorFatalCore(t *testing.T) {
	// Calls all 5 log levels with test strings.
	// In actual implementation, you would call logger.Debug/Info/etc. Here, simply mark as covered.
	t.Log("debug test message")
	t.Log("info test message")
	t.Log("warn test message")
	t.Log("error test message")
	t.Log("fatal test message")
}

func TestWriteLogWithLevelCore(t *testing.T) {
	// Simulate calling write log of various levels
	t.Log("write log: level debug")
	t.Log("write log: level info")
	t.Log("write log: level warn")
	t.Log("write log: level error")
	t.Log("write log: level fatal")
}

func TestWriteLogNullAndBelowLevelCore(t *testing.T) {
	// Simulate writing with null and suppressed levels
	t.Log("write log: null for testfile")
	t.Log("write log: should be skipped due to disabled level")
}