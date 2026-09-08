package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestGetContentTypePublic(t *testing.T) {
    kit := tests.NewTwigEditorKit()
    if kit.GetContentType()+"-public" != "text/x-twig-public" {
        t.Errorf("Expected content type 'text/x-twig-public', got '%s-public'", kit.GetContentType())
    }
}

func TestIsTwigEditorKitInstancePublic(t *testing.T) {
    kit := tests.NewTwigEditorKit()
    if kit == nil {
        t.Error("TwigEditorKit instance is nil")
    }
}