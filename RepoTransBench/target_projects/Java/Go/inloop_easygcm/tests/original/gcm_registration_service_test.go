package original

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// --- Constants and minimal stub types ---

const (
    ACTION_REGISTER_GCM     = 101
    EXTRA_ACTION_CODE       = "AC"
    EXTRA_HAS_WAKELOCK      = "WL"
)

// GcmRegistrationService provides just the basics for test logic
type GcmRegistrationService struct {
    mock.Mock
}

func (g *GcmRegistrationService) isAlreadyRegistered(ctx Context) bool {
    args := g.Called(ctx)
    return args.Bool(0)
}
func (g *GcmRegistrationService) releaseWakeLock() {
    g.Called()
}
func (g *GcmRegistrationService) registerGcm() {
    g.Called()
}
func (g *GcmRegistrationService) onHandleIntent(intent *Intent) {
    if intent == nil {
        g.releaseWakeLock()
        return
    }
    actionCode, ok := intent.extras[EXTRA_ACTION_CODE]
    if !ok || actionCode != ACTION_REGISTER_GCM {
        g.releaseWakeLock()
        return
    }

    fakeCtx := new(MockContext)
    if g.isAlreadyRegistered(fakeCtx) {
        g.releaseWakeLock()
        return
    }
    g.registerGcm()
    g.releaseWakeLock()
}

func CreateGcmRegistrationIntent(ctx Context) *Intent {
    intent := NewIntent()
    intent.extras[EXTRA_ACTION_CODE] = ACTION_REGISTER_GCM
    return intent
}
func CreateGcmRegistrationIntentWithWakeLock(ctx Context, hasWakeLock bool) *Intent {
    intent := NewIntent()
    intent.extras[EXTRA_ACTION_CODE] = ACTION_REGISTER_GCM
    intent.extras[EXTRA_HAS_WAKELOCK] = hasWakeLock
    return intent
}

// --- Tests ---

func TestCreateGcmRegistrationIntentDefaults(t *testing.T) {
    ctx := new(MockContext)
    result := CreateGcmRegistrationIntent(ctx)
    assert.NotNil(t, result)
    v, ok := result.extras[EXTRA_ACTION_CODE]
    assert.True(t, ok)
    assert.Equal(t, ACTION_REGISTER_GCM, v)
}

func TestCreateGcmRegistrationIntentWithWakeLock(t *testing.T) {
    ctx := new(MockContext)
    result := CreateGcmRegistrationIntentWithWakeLock(ctx, true)
    wl := result.extras[EXTRA_HAS_WAKELOCK]
    assert.Equal(t, true, wl)
}

func TestOnHandleIntentAlreadyRegistered(t *testing.T) {
    intent := NewIntent()
    intent.extras[EXTRA_ACTION_CODE] = ACTION_REGISTER_GCM

    service := new(GcmRegistrationService)
    service.On("isAlreadyRegistered", mock.Anything).Return(true)
    service.On("releaseWakeLock").Return()

    service.onHandleIntent(intent)

    service.AssertNotCalled(t, "registerGcm")
    service.AssertCalled(t, "releaseWakeLock")
}

func TestOnHandleIntentRegistersAndHandlesError(t *testing.T) {
    intent := NewIntent()
    intent.extras[EXTRA_ACTION_CODE] = ACTION_REGISTER_GCM

    service := new(GcmRegistrationService)
    service.On("isAlreadyRegistered", mock.Anything).Return(false)
    service.On("releaseWakeLock").Return()
    service.On("registerGcm").Return()

    service.onHandleIntent(intent)

    service.AssertCalled(t, "registerGcm")
    service.AssertCalled(t, "releaseWakeLock")
}