package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestFormatKeepsInputWhenNoTwig(t *testing.T) {
    formatter := &tests.TwigFormatter{}
    input := "<h2>No Twig public!</h2>"
    if output := formatter.Format(input); output != input {
        t.Errorf("Expected output to match input when no twig, got '%s'", output)
    }
}

func TestFormatHandlesTwigBlock(t *testing.T) {
    formatter := &tests.TwigFormatter{}
    input := "{% for item in items %}<li>{{ item }}</li>{% endfor %}"
    formatted := formatter.Format(input)
    if formatted == "" {
        t.Error("Expected formatted output to be non-empty")
    }
}