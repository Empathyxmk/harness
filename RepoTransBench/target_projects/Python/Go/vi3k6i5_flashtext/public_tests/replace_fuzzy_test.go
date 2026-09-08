package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicReplaceFuzzy(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("python script", "pythonscript")
    kp.AddKeyword("python", "pythonic")
    in := "I like pythn script"
    replaced := kp.ReplaceFuzzy(in, 2)
    if replaced != "I like pythonscript" {
        t.Errorf("Expected 'I like pythonscript', got '%v'", replaced)
    }
    in2 := "python rules"
    replaced2 := kp.ReplaceFuzzy(in2, 2)
    if replaced2 != "pythonic rules" {
        t.Errorf("Expected 'pythonic rules', got '%v'", replaced2)
    }
}