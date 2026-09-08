package original

import (
	"errors"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func BenchmarkMain(args []string) error {
	if args == nil || len(args) == 0 {
		return errors.New("Usage: Must supply arguments")
	}
	if len(args) > 0 && args[0] == "--foo" {
		return errors.New("Unrecognized option --foo")
	}
	return nil
}

func TestMainWithNoArgsThrowsRuntimeException(t *testing.T) {
	err := BenchmarkMain([]string{})
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "Usage")
}