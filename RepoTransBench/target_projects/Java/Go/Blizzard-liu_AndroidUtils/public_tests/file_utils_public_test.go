package public_tests

import (
    "testing"
)

func TestGetFileExtensionJsonPublic(t *testing.T) {
    fileName := "myapiresult.json"
    idx := len(fileName) - len(".json")
    ext := fileName[idx:]
    if ext != ".json" {
        t.Errorf("Expected file extension .json, got %s", ext)
    }
}