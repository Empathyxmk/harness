package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestParseWhitespacePublic(t *testing.T) {
    parser := &tests.TwigParser{}
    result := parser.Parse("   ")
    if result == nil {
        t.Fatal("Parse returned nil for whitespace")
    }
    if len(result.GetErrors()) != 0 {
        t.Errorf("Expected no errors on whitespace")
    }
}

func TestParseOutputTwigPublic(t *testing.T) {
    parser := &tests.TwigParser{}
    input := "{{ 987 }}"
    result := parser.Parse(input)
    if result == nil {
        t.Fatal("Parse returned nil")
    }
    if result.GetParsedData() == nil {
        t.Error("Expected parsed data to be not nil")
    }
}