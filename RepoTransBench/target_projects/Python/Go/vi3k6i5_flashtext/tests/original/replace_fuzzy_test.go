package original

import (
    "testing"
    "flashtext"
)

func TestReplaceFuzzy(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java script", "javascript")
    kp.AddKeyword("javascript", "javascript")
    kp.AddKeyword("java", "java")

    line := "I like javascipt"
    replaced := kp.ReplaceFuzzy(line, 2)
    if replaced != "I like javascript" {
        t.Errorf("expected output to be 'I like javascript', got %v", replaced)
    }
    line2 := "I like jaba"
    replaced2 := kp.ReplaceFuzzy(line2, 2)
    if replaced2 != "I like java" {
        t.Errorf("expected output to be 'I like java', got %v", replaced2)
    }
}