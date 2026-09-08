package original

import (
    "io/ioutil"
    "os"
    "strings"
    "testing"
)

func TestWriteAndReadFile(t *testing.T) {
    tmp, err := ioutil.TempFile("", "FileUtilsTest_*.txt")
    if err != nil {
        t.Fatalf("Failed to create temp file: %v", err)
    }
    defer os.Remove(tmp.Name())
    defer tmp.Close()

    testStr := "hello"
    if _, err := tmp.Write([]byte(testStr)); err != nil {
        t.Fatalf("Failed to write to temp file: %v", err)
    }
    tmp.Sync()

    data, err := ioutil.ReadFile(tmp.Name())
    if err != nil {
        t.Fatalf("Failed to read back: %v", err)
    }
    res := string(data)
    if !strings.Contains(res, "hello") {
        t.Errorf("Result %q does not contain 'hello'", res)
    }
}