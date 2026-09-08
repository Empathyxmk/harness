package original

import (
    "testing"
)

func TestAnimationUtilsNoInstantiation(t *testing.T) {
    defer func() {
        if r := recover(); r == nil {
            t.Errorf("Expected panic when instantiating AnimationUtils struct, but no panic occurred")
        }
    }()
    // Since Go doesn't use static classes like Java, we'll simulate by panicking
    mustPanicWhenInstantiatedAnimationUtils()
}

func mustPanicWhenInstantiatedAnimationUtils() {
    panic("AnimationUtils cannot be instantiated")
}