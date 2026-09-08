package original

import (
    "io/ioutil"
    "os"
    "testing"
    "flashtext"
)

func TestLoadingKeywordList(t *testing.T) {
    keywords := []string{"java", "python", "go"}
    tmpFile, err := ioutil.TempFile("", "keywords*.txt")
    if err != nil {
        t.Fatal("could not create temp file:", err)
    }
    defer os.Remove(tmpFile.Name())

    for _, kw := range keywords {
        tmpFile.Write([]byte(kw + "\n"))
    }
    tmpFile.Close()

    kp := flashtext.NewKeywordProcessor()
    count, err := kp.LoadKeywordsFromFile(tmpFile.Name())
    if err != nil || count != 3 {
        t.Errorf("failed loading 3 keywords: got err=%v, count=%d", err, count)
    }
    for _, kw := range keywords {
        if !kp.ContainsKeyword(kw) {
            t.Errorf("missing keyword: %s", kw)
        }
    }
}