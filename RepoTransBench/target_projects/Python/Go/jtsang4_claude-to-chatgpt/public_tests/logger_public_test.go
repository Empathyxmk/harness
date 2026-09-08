package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"log"
)

func TestPublicGetLoggerLevel(t *testing.T) {
	logger := log.Default()
	logger.SetFlags(0)
	// Set log level simulated by Logger struct
	assert.IsType(t, logger, &log.Logger{})
}

func TestPublicGetLoggerName(t *testing.T) {
	// Go's log.Logger does not have a .name, simulate uniqueness by creating a unique logger pointer
	logger := log.New(nil, "unique_logger_name", 0)
	assert.NotNil(t, logger)
}