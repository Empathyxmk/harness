package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestBlankInputPublic(t *testing.T) {
    result := tests.NewTwigParserResult("   ")
    if result == nil {
        t.Fatal("NewTwigParserResult('   ') returned nil")
    }
    if len(result.GetErrors()) != 0 {
        t.Errorf("Expected errors to be empty on blank input")
    }
    if result.GetParsedData() == nil {
        t.Error("Expected parsed data to be not nil")
    }
}

func TestSimpleTwigInputPublic(t *testing.T) {
    result := tests.NewTwigParserResult("{% include 'header.twig' %}")
    if result.GetParsedData() == nil {
        t.Error("Expected parsed data to be not nil")
    }
    if result.GetErrors() == nil {
        t.Error("Expected errors slice to be not nil")
    }
}