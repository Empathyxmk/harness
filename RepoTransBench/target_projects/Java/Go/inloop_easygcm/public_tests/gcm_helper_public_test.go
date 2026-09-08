package public_tests

import (
    "testing"

    "github.com/inloop-easygcm/go-easygcm/tests/original"
    "github.com/stretchr/testify/require"
)

func TestInitDelegatesToEasyGcmPublic(t *testing.T) {
    ctx := new(original.MockContext)
    original.GcmHelper_init(ctx) // Should not panic
}

func TestSetGcmListenerPublic(t *testing.T) {
    l := new(struct{})
    original.GcmHelper_setGcmListener(l)
}

func TestSetCheckServicesHandlerPublic(t *testing.T) {
    h := new(struct{})
    original.GcmHelper_setCheckServicesHandler(h)
}

func TestIsRegisteredPublicDifferentInput(t *testing.T) {
    ctx := new(original.MockContext)
    original.GcmHelper_isRegistered(ctx)
}

func TestGetRegistrationIdPublicDifferentInput(t *testing.T) {
    ctx := new(original.MockContext)
    original.GcmHelper_getRegistrationId(ctx)
}

func TestRemoveRegistrationIdPublicDifferentInput(t *testing.T) {
    ctx := new(original.MockContext)
    original.GcmHelper_removeRegistrationId(ctx)
}

func TestGetGcmSenderIdPublicDifferentInput(t *testing.T) {
    ctx := new(original.MockContext)
    original.GcmHelper_getGcmSenderId(ctx)
}

func TestSetLoggingEnabledPublic(t *testing.T) {
    helper := original.GetGcmHelperInstance()
    helper.SetLoggingEnabled(5)
    require.Equal(t, 5, helper.LogLevel())
}

func TestGetGcmListenerPublic(t *testing.T) {
    helper := original.GetGcmHelperInstance()
    ctx := new(original.MockContext)
    helper.GetGcmListener(ctx)
}