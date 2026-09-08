package original

import (
    "errors"
    "testing"

    "github.com/stretchr/testify/assert"
)

type DummyMain struct {
    Called    *bool
    Throwable *error
}

// Simulate static method main behavior.
func (d *DummyMain) Main(args []string) error {
    *d.Called = true
    if d.Throwable != nil && *d.Throwable != nil {
        return *d.Throwable
    }
    return nil
}

// Simulate Utils.callMain implementation.
func UtilsCallMain(dummy *DummyMain, className string, args []string) error {
    // In real: use reflection by className. Here just call dummy.Main.
    return dummy.Main(args)
}

func TestUtilsCallMainSuccessful(t *testing.T) {
    called := false
    // No error
    dummy := DummyMain{Called: &called, Throwable: nil}
    err := UtilsCallMain(&dummy, "DummyMain", []string{})
    assert.True(t, called, "DummyMain.main should have been called")
    assert.NoError(t, err)
}

func TestUtilsCallMainThrowsTargetException(t *testing.T) {
    called := false
    throwErr := errors.New("test")
    dummy := DummyMain{Called: &called, Throwable: &throwErr}
    err := UtilsCallMain(&dummy, "DummyMain", []string{})
    assert.True(t, called, "DummyMain.main should have been called")
    assert.Error(t, err)
    assert.EqualError(t, err, "test")
}