package public_tests

import (
	"testing"
)

type DummyLogger struct{}

func (l *DummyLogger) Info(msg string) {}

func GetLogger() *DummyLogger {
	return &DummyLogger{}
}

func TestPublicThroughputDifferentLoop(t *testing.T) {
	logger := GetLogger()
	cnt := 10
	for i := 0; i < cnt; i++ {
		logger.Info("Public throughput message #" + string(rune(i)))
	}
}