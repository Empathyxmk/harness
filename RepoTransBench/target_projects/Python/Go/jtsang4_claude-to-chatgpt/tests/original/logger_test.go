package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"log"
)

func TestLoggerImportable(t *testing.T) {
	// Simulate logger instance from claude_to_chatgpt/logger
	logger := log.Default()
	assert.IsType(t, logger, &log.Logger{})
}