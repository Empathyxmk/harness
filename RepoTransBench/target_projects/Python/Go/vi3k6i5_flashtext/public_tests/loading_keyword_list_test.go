package public_tests

import (
    "io/ioutil"
    "os"
    "testing"
    "flashtext"
)

func TestPublicLoadingKeywordList(t *testing.T) {
    keywords := []string{"foo", "bar", "baz"}
    f, err := ioutil.TempFile("", "words*.txt")
    if err != nil {
        t.Fatalf("Temp file err: %v", err)
    }
    for _, kw := range keywords {
        _, _ = f.Write([]byte(kw + "\n"))
    }
    _ = f.Close()
    defer os.Remove(f.Name())

    kp := flashtext.NewKeywordProcessor()
    n, err := kp.LoadKeywordsFromFile(f.Name())
    if err != nil || n != 3 {
        t.Errorf("LoadKeywords error or incorrect count: err=%v n=%d", err, n)
    }
    for _, kw := range keywords {
        if !kp.ContainsKeyword(kw) {
            t.Errorf("Test file missing keyword: %v", kw)
        }
    }
}