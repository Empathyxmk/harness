package original

import (
	"testing"
)

type DummyLogger struct{}

func (l *DummyLogger) Info(msg string)                        {}
func (l *DummyLogger) WriteLog(level int, msg string)         {}
func (l *DummyLogger) WriteLogWithFile(file string, level int, msg string) {
}

var DummyConstant = struct {
	INFO  int
	ERROR int
}{
	INFO:  1,
	ERROR: 3,
}

func GetLogger() *DummyLogger {
	return &DummyLogger{}
}

func TestFloggerUsage(t *testing.T) {
	logger := GetLogger()
	// "Getting singleton"
	logger.Info("Here is your message...")
	// writes with a fixed level
	logger.WriteLog(DummyConstant.INFO, "Here is your customized level message...")
	// writes with a log file name
	logger.WriteLogWithFile("error", DummyConstant.ERROR, "Here is your customized log file and level message...")
}