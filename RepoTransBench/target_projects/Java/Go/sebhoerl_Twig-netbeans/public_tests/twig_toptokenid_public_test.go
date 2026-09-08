package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestTokenIdOfContent(t *testing.T) {
    values := tests.AllTwigTopTokenIds
    found := false
    for _, id := range values {
        if string(id) == "TWIG_CONTENT" {
            found = true
            break
        }
    }
    if len(values) == 0 {
        t.Error("Expected at least one token id")
    }
    if !found {
        t.Error("TWIG_CONTENT not found among token ids")
    }
}

func TestValueOfWithAllEnums(t *testing.T) {
    for _, id := range tests.AllTwigTopTokenIds {
        value := tests.ValueOfTwigTopTokenId(string(id))
        if value != id {
            t.Errorf("Expected %v == %v", value, id)
        }
    }
}