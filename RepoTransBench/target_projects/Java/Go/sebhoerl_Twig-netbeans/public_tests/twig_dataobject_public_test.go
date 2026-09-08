package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestTwigDataObjectExtensionPublic(t *testing.T) {
    obj := tests.NewTwigDataObjectPath("examplePublic.twig")
    if obj.GetFileExtension() != "twig" {
        t.Errorf("Expected file extension 'twig', got '%v'", obj.GetFileExtension())
    }
}

func TestIsTwigFileReturnsTruePublic(t *testing.T) {
    obj := tests.NewTwigDataObjectPath("anotherfilePublic.twig")
    if !obj.IsTwigFile() {
        t.Errorf("Expected IsTwigFile to return true for .twig files")
    }
}