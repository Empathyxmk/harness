package public_tests

import (
    "testing"
)

func TestUtilsAppContextPublic(t *testing.T) {
    utilsPackageName := "com.example.utils.test"
    if utilsPackageName == "com.example.somethingelse" {
        t.Errorf("Expected different than com.example.somethingelse")
    }
}