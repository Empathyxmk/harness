package public_tests

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/inloop-easygcm/go-easygcm/tests/original"
)

func TestCreateGcmRegistrationIntentWithWakeLockPublic(t *testing.T) {
    ctx := new(original.MockContext)
    serviceIntent := original.CreateGcmRegistrationIntentWithWakeLock(ctx, false)
    assert.NotNil(t, serviceIntent)
}

func TestCreateGcmRegistrationIntentWithWakeLockPublicDifferent(t *testing.T) {
    ctx := new(original.MockContext)
    serviceIntent := original.CreateGcmRegistrationIntentWithWakeLock(ctx, true)
    assert.NotNil(t, serviceIntent)
}