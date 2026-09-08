package original

import (
	"testing"
	"twigmodule/tests"
)

func TestFormatterExists(t *testing.T) {
	formatter := &tests.TwigFormatter{}
	if formatter == nil {
		t.Error("Formatter should not be nil")
	}
}