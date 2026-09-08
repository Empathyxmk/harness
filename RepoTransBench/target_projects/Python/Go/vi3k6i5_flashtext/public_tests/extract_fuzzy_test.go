package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicExtractFuzzy(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("javascript", "JS")
    kp.AddKeyword("java", "JavaLang")

    out := kp.ExtractFuzzy("pythn javascript", 2)
    if len(out) != 1 || out[0] != "JS" {
        t.Errorf("Expected [JS], got %v", out)
    }
    out2 := kp.ExtractFuzzy("pythn java", 2)
    if len(out2) != 1 || out2[0] != "JavaLang" {
        t.Errorf("Expected [JavaLang], got %v", out2)
    }
}