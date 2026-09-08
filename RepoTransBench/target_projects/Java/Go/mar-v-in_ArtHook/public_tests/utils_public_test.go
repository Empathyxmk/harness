package public_tests

import (
    "errors"
    "testing"

    "github.com/stretchr/testify/assert"
)

type DummyPublicMain struct {
    Called    *bool
    Throwable *error
}

func (d *DummyPublicMain) Main(args []string) error {
    *d.Called = true
    if d.Throwable != nil && *d.Throwable != nil {
        return *d.Throwable
    }
    return nil
}

// Simulate Utils.callMain behavior
func UtilsCallMainPublic(dummy *DummyPublicMain, className string, args []string) error {
    return dummy.Main(args)
}

func TestCallMainSuccessfulWithDifferentClass(t *testing.T) {
    called := false
    dummy := DummyPublicMain{Called: &called, Throwable: nil}
    err := UtilsCallMainPublic(&dummy, "DummyPublicMain", []string{})
    assert.True(t, called, "DummyPublicMain.main should have been called")
    assert.NoError(t, err)
}

func TestCallMainThrowsTargetRuntimeException(t *testing.T) {
    called := false
    throwErr := errors.New("public test")
    dummy := DummyPublicMain{Called: &called, Throwable: &throwErr}
    err := UtilsCallMainPublic(&dummy, "DummyPublicMain", []string{})
    assert.True(t, called, "DummyPublicMain.main should have been called")
    assert.Error(t, err)
    assert.EqualError(t, err, "public test")
}