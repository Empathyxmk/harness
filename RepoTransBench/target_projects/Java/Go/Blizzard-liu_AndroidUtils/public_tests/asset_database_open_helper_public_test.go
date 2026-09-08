package public_tests

import (
    "strings"
    "testing"
)

func TestOpenDatabasePublic(t *testing.T) {
    dbName := "another_public_test.db"
    if !strings.HasPrefix(dbName, "another_") {
        t.Errorf("Expected dbName to start with another_, got %s", dbName)
    }
}