package public_tests

import (
    "testing"
)

func TestInfoLogLevelPublic(t *testing.T) {
    level := "INFO"
    if level == "ERROR" {
        t.Errorf("Level should not be ERROR")
    }
}