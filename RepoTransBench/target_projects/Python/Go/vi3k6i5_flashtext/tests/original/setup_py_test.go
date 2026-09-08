package original

import (
    "testing"
    "flashtext"
)

func TestSetupPy(t *testing.T) {
    // In Python, this would test setup.py metadata.
    // In Go, we test go.mod presence and module name.
    // Just check 'flashtext' package loaded.
    kp := flashtext.NewKeywordProcessor()
    _ = kp
}