package public_tests

import (
	"testing"
)

type DummyLogger struct{}

func (l *DummyLogger) Debug(msg string) {}
func (l *DummyLogger) Fatal(msg string) {}
func (l *DummyLogger) WriteLogWithFile(file string, level int, msg string) {
}

func GetLogger() *DummyLogger {
	return &DummyLogger{}
}

func TestVariousLevelsPublic(t *testing.T) {
	logger := GetLogger()
	logger.Debug("Debugging - public core test!")
	logger.Fatal("This is a public fatal log!")
	logger.WriteLogWithFile("public_logfile", 2, "This is a public WARN log in a special file!")
}