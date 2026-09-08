package public_tests

import (
    "strings"
    "testing"
)

func TestUrlIsJpegPublic(t *testing.T) {
    url := "https://example.org/altpic.jpeg"
    if !strings.HasSuffix(url, ".jpeg") {
        t.Errorf("Expected URL to end with .jpeg, got %s", url)
    }
}