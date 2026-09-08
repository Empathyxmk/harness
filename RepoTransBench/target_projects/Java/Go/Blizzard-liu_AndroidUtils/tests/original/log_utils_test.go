package original

import (
    "testing"
)

func TestLogUtilsNoInstantiation(t *testing.T) {
    defer func() {
        if r := recover(); r == nil {
            t.Errorf("Expected panic when instantiating LogUtils struct, but no panic occurred")
        }
    }()
    mustPanicWhenInstantiatedLogUtils()
}

func mustPanicWhenInstantiatedLogUtils() {
    panic("LogUtils cannot be instantiated")
}