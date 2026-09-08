package original

import (
	"testing"
	"twigmodule/tests"
)

func TestParseGetResult(t *testing.T) {
	parser := &tests.TwigParser{}
	result := parser.Parse("")
	if result == nil {
		t.Fatal("Parser parse returned nil")
	}
}