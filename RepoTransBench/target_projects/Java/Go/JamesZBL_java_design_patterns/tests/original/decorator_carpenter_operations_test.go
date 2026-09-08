package original

import (
	"testing"
	"jameszbl_java_design_patterns/decorator"
)

// Our fake logger for capturing log messages (simulate InMemoryAppender)
type inMemoryCarpenterLogger struct {
	messages []string
}

func (l *inMemoryCarpenterLogger) log(msg string) {
	l.messages = append(l.messages, msg)
}

func (l *inMemoryCarpenterLogger) getLastMessage() string {
	if len(l.messages) == 0 {
		return ""
	}
	return l.messages[len(l.messages)-1]
}

func (l *inMemoryCarpenterLogger) getLogSize() int {
	return len(l.messages)
}

func TestCarpenterOperations(t *testing.T) {
	logger := &inMemoryCarpenterLogger{}
	carpenter := decorator.NewCarpenterOperationWithLogger(logger.log)

	carpenter.CheckBefore()
	if logger.getLastMessage() != "检查木材" {
		t.Errorf("got %q, want 检查木材", logger.getLastMessage())
	}

	carpenter.Join()
	if logger.getLastMessage() != "打造锤把" {
		t.Errorf("got %q, want 打造锤把", logger.getLastMessage())
	}

	carpenter.CheckAfter()
	if logger.getLastMessage() != "检查成品锤把" {
		t.Errorf("got %q, want 检查成品锤把", logger.getLastMessage())
	}
	if logger.getLogSize() != 3 {
		t.Errorf("expected log size 3, got %d", logger.getLogSize())
	}
}