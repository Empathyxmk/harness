package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestGetMimeTypeIsNotHtml(t *testing.T) {
    if tests.MIME_TYPE == "text/html" {
        t.Error("MIME_TYPE should not be 'text/html'")
    }
}

func TestGetInstanceIsIdentical(t *testing.T) {
    langA := tests.TwigLanguageGetInstance()
    langB := tests.TwigLanguageGetInstance()
    if langA != langB {
        t.Error("TwigLanguage.GetInstance should return the same instance")
    }
}