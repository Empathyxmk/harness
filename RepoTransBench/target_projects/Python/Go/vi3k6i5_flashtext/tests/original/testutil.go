package original

import (
    "io/ioutil"
    "os"
    "testing"
)

// Helper to create temp files for tests
func CreateTestFile(t *testing.T, content string) (filename string, cleanup func()) {
    tmpFile, err := ioutil.TempFile("", "testfile*.txt")
    if err != nil {
        t.Fatalf("could not create temp test file: %v", err)
    }
    if _, err := tmpFile.Write([]byte(content)); err != nil {
        t.Fatalf("could not write to temp test file: %v", err)
    }
    tmpFile.Close()
    return tmpFile.Name(), func() {
        os.Remove(tmpFile.Name())
    }
}