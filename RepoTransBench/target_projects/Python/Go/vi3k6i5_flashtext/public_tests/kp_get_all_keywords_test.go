package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicGetAllKeywords(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("python", "PYTHON")
    all := kp.GetAllKeywords()
    v, ok := all["python"]
    if !ok || v != "PYTHON" {
        t.Errorf("Expected 'python' to map to 'PYTHON', got %+v", v)
    }
}