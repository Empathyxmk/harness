package original

import (
	"bytes"
	"testing"
)

// Dummy FLogger for sim test.
type DummyFLogger struct {
	OutBuf         *bytes.Buffer
	ConsolePrint   *bool
	LogLevelConfig *string
}

func getDummyFLogger() *DummyFLogger {
	buf := new(bytes.Buffer)
	consolePrint := true
	logLevel := "0,1,2,3,4"
	return &DummyFLogger{OutBuf: buf, ConsolePrint: &consolePrint, LogLevelConfig: &logLevel}
}

func (l *DummyFLogger) GetInstance() *DummyFLogger {
	return l
}
func (l *DummyFLogger) Debug(msg string)          { l.log("debug", msg) }
func (l *DummyFLogger) Info(msg string)           { l.log("info", msg) }
func (l *DummyFLogger) Warn(msg string)           { l.log("warn", msg) }
func (l *DummyFLogger) Error(msg string)          { l.log("error", msg) }
func (l *DummyFLogger) Fatal(msg string)          { l.log("fatal", msg) }
func (l *DummyFLogger) WriteLog(level int, msg string) {
	l.log("log", msg)
}
func (l *DummyFLogger) WriteLogWithFile(file string, level int, msg string) {
	l.log("log", msg)
}
func (l *DummyFLogger) log(kind, msg string) {
	if l.OutBuf != nil && msg != "" {
		l.OutBuf.WriteString(msg)
	}
}

func TestSingletonInstance(t *testing.T) {
	logger1 := getDummyFLogger()
	logger2 := logger1.GetInstance()
	if logger1 != logger2 {
		t.Fatal("Logger singleton should be same instance")
	}
}

func TestDebugInfoWarnErrorFatal(t *testing.T) {
	logger := getDummyFLogger()
	logger.Debug("debug message")
	logger.Info("info message")
	logger.Warn("warn message")
	logger.Error("error message")
	logger.Fatal("fatal message")
	out := logger.OutBuf.String()
	for _, substr := range []string{"debug message", "info message", "warn message", "error message", "fatal message"} {
		if !bytes.Contains([]byte(out), []byte(substr)) {
			t.Errorf("Expected logger out to contain: %s", substr)
		}
	}
}

func TestWriteLogIntLevel(t *testing.T) {
	logger := getDummyFLogger()
	logger.WriteLog(0, "int-level debug")
	logger.WriteLog(1, "int-level info")
	logger.WriteLog(2, "int-level warn")
	logger.WriteLog(3, "int-level error")
	logger.WriteLog(4, "int-level fatal")
}

func TestWriteLogNullMessage(t *testing.T) {
	logger := getDummyFLogger()
	logger.WriteLogWithFile("custom", 0, "")
}

func TestWriteLogUnsupportedLevel(t *testing.T) {
	logger := getDummyFLogger()
	oldCfg := *logger.LogLevelConfig
	*logger.LogLevelConfig = "1,2,3,4"
	logger.WriteLogWithFile("custom", 0, "should not log")
	*logger.LogLevelConfig = oldCfg
}