package original

import (
    "testing"
    "flashtext"
)

func TestReplacer(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java", "JAVA")
    kp.AddKeyword("python", "PYTHON")

    s := "java python"
    replaced := kp.ReplaceKeywords(s)
    if replaced != "JAVA PYTHON" {
        t.Errorf("expected 'JAVA PYTHON', got '%v'", replaced)
    }
}