package public_tests

import (
	"testing"
)

type DummyLogger struct{}

func (l *DummyLogger) Info(msg string) {}
func (l *DummyLogger) Warn(msg string) {}

func GetLogger() *DummyLogger {
	return &DummyLogger{}
}

func TestLoggerInfoAndWarnPublic(t *testing.T) {
	logger := GetLogger()
	logger.Info("Public INFO message for FLoggerTestPublic")
	logger.Warn("Public WARN message for FLoggerTestPublic")
}