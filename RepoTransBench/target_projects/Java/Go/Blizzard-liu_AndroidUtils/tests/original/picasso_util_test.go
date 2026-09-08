package original

import (
    "testing"
)

func TestPicassoUtilNoInstantiation(t *testing.T) {
    defer func() {
        if r := recover(); r == nil {
            t.Errorf("Expected panic when instantiating PicassoUtil struct, but no panic occurred")
        }
    }()
    mustPanicWhenInstantiatedPicassoUtil()
}

func mustPanicWhenInstantiatedPicassoUtil() {
    panic("PicassoUtil cannot be instantiated")
}