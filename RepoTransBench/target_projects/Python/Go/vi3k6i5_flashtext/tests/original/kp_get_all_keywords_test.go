package original

import (
    "testing"
    "flashtext"
)

func TestGetAllKeywords(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java")
    kp.AddKeyword("python")

    out := kp.GetAllKeywords()
    if len(out) != 2 || !(out["java"] == "java" && out["python"] == "python") {
        t.Errorf("Expected all keywords to be present in map, got %+v", out)
    }
}