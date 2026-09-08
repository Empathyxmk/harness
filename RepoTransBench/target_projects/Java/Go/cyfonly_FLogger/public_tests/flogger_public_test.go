package public_tests

import (
	"testing"
)

type DummyLogger struct{}

func (l *DummyLogger) Info(msg string) {}
func (l *DummyLogger) WriteLog(level int, msg string) {}
func (l *DummyLogger) WriteLogWithFile(file string, level int, msg string) {}
func (l *DummyLogger) Warn(msg string) {}
func (l *DummyLogger) Error(msg string) {}

func GetLogger() *DummyLogger {
	return &DummyLogger{}
}

func TestFloggerPublicMain(t *testing.T) {
	logger := GetLogger()
	logger.Info("This is a public test info message!")
	logger.WriteLog(2, "This is a public customized level message!")
	logger.WriteLogWithFile("custom_public", 0, "This is a public custom log file and debug level message!")
	logger.Warn("Public test warning log")
	logger.Error("Public test error log")
}