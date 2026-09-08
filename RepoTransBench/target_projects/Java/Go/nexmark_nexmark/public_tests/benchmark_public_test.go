package public_tests

import (
	"errors"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func BenchmarkMain(args []string) error {
	if args == nil {
		return errors.New("Usage: args must not be nil")
	}
	if len(args) == 0 {
		return errors.New("Usage: Must supply arguments")
	}
	if len(args) > 0 && args[0] == "--foo" {
		return errors.New("Unrecognized option --foo")
	}
	return nil
}

func TestMainWithNullArgsThrowsRuntimeException(t *testing.T) {
	err := BenchmarkMain(nil)
	assert.Error(t, err)
	assert.Contains(t, strings.ToLower(err.Error()), "usage")
}

func TestMainWithInvalidArgsThrowsParseExceptionOrRuntime(t *testing.T) {
	err := BenchmarkMain([]string{"--foo"})
	assert.Error(t, err)
	assert.NotNil(t, err.Error())
}