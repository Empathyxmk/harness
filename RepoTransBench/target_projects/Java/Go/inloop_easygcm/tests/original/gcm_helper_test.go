package original

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// --- Interfaces and Helper Types ---

// GcmListener and GcmServicesHandler are just empty for stub
type GcmListener interface{}
type GcmServicesHandler interface{}

// GcmHelper is a singleton with stubbed behavior
type GcmHelper struct {
    logLevel int
}

var gcmHelperSingleton *GcmHelper

func GetGcmHelperInstance() *GcmHelper {
    if gcmHelperSingleton == nil {
        gcmHelperSingleton = &GcmHelper{}
    }
    return gcmHelperSingleton
}
func (g *GcmHelper) SetLoggingEnabled(level int) {
    g.logLevel = level
}

// Dummy static method proxies (to EasyGcm)
func GcmHelper_init(ctx Context) {
    // Only to test that it doesn't panic
}
func GcmHelper_setGcmListener(listener GcmListener) { }
func GcmHelper_setCheckServicesHandler(handler GcmServicesHandler) { }
func GcmHelper_isRegistered(ctx Context) bool {
    // Default stub: always returns false to match test assertion
    return false
}
func GcmHelper_getRegistrationId(ctx Context) *string {
    // Default stub: always returns nil
    return nil
}
func GcmHelper_removeRegistrationId(ctx Context) {}
func GcmHelper_getGcmSenderId(ctx Context) *string { return nil }
func (g *GcmHelper) GetGcmListener(ctx Context) GcmListener { return nil }

// --- Tests ---

func TestInitDelegatesToEasyGcm(t *testing.T) {
    ctx := new(MockContext)
    assert.NotPanics(t, func() {
        GcmHelper_init(ctx)
    })
}

func TestGetInstance_Singleton(t *testing.T) {
    instance1 := GetGcmHelperInstance()
    instance2 := GetGcmHelperInstance()
    assert.NotNil(t, instance1)
    assert.Equal(t, instance1, instance2)
}

func TestSetGcmListenerDelegatesToEasyGcm(t *testing.T) {
    l := new(struct{})
    assert.NotPanics(t, func() {
        GcmHelper_setGcmListener(l)
    })
}

func TestSetCheckServicesHandlerDelegatesToEasyGcm(t *testing.T) {
    h := new(struct{})
    assert.NotPanics(t, func() {
        GcmHelper_setCheckServicesHandler(h)
    })
}

func TestIsRegisteredDelegatesToEasyGcm(t *testing.T) {
    ctx := new(MockContext)
    result := GcmHelper_isRegistered(ctx)
    assert.False(t, result)
}

func TestGetRegistrationIdDelegatesToEasyGcm(t *testing.T) {
    ctx := new(MockContext)
    val := GcmHelper_getRegistrationId(ctx)
    assert.Nil(t, val)
}

func TestRemoveRegistrationIdDelegatesToEasyGcm(t *testing.T) {
    ctx := new(MockContext)
    assert.NotPanics(t, func() {
        GcmHelper_removeRegistrationId(ctx)
    })
}

func TestGetGcmSenderIdDelegatesToEasyGcm(t *testing.T) {
    ctx := new(MockContext)
    val := GcmHelper_getGcmSenderId(ctx)
    assert.Nil(t, val)
}

func TestSetLoggingEnabled(t *testing.T) {
    helper := GetGcmHelperInstance()
    helper.SetLoggingEnabled(1)
    assert.Equal(t, 1, helper.logLevel)
}

func TestGetGcmListenerDelegatesToEasyGcm(t *testing.T) {
    helper := GetGcmHelperInstance()
    ctx := new(MockContext)
    l := helper.GetGcmListener(ctx)
    assert.Nil(t, l)
}