package original

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// --- Interfaces and Stubs for BroadcastReceiver behavior ---

type Intent struct {
    extras map[string]interface{}
}

func NewIntent() *Intent {
    return &Intent{extras: map[string]interface{}{}}
}

type WakefulBroadcastReceiver interface {
    OnReceive(ctx Context, intent *Intent)
    StartWakefulService(ctx Context, intent *Intent)
}

type NetworkStateReceiver struct {
    mock.Mock
}

func (n *NetworkStateReceiver) OnReceive(ctx Context, intent *Intent) {
    if GcmUtils_checkCanAndShouldRegister(ctx) {
        regIntent := GcmRegistrationService_createGcmRegistrationIntent(ctx, true)
        n.StartWakefulService(ctx, regIntent)
    }
    // else do nothing
}

func (n *NetworkStateReceiver) StartWakefulService(ctx Context, intent *Intent) {
    n.Called(ctx, intent)
}

// --- Static stubbers for test injection ---

var gcmUtilsStub = &GcmUtilsStubber{}
var gcmRegServiceStub = &GcmRegistrationServiceStubber{}

func GcmUtils_checkCanAndShouldRegister(ctx Context) bool {
    if gcmUtilsStub.override {
        return gcmUtilsStub.forcedResult
    }
    return false
}
type GcmUtilsStubber struct {
    forcedResult bool
    override     bool
}
func (g *GcmUtilsStubber) SetCheckCanAndShouldRegisterResult(res bool) {
    g.forcedResult = res
    g.override = true
}
func (g *GcmUtilsStubber) Reset() {
    g.forcedResult = false
    g.override = false
}

func GcmRegistrationService_createGcmRegistrationIntent(ctx Context, hasWakeLock bool) *Intent {
    if gcmRegServiceStub.forcedIntent != nil {
        return gcmRegServiceStub.forcedIntent
    }
    return NewIntent()
}
type GcmRegistrationServiceStubber struct {
    forcedIntent *Intent
}
func (g *GcmRegistrationServiceStubber) SetCreateGcmRegistrationIntentResult(intent *Intent) {
    g.forcedIntent = intent
}
func (g *GcmRegistrationServiceStubber) Reset() {
    g.forcedIntent = nil
}

// --- Context interface already imported from connection_utils_test.go ---

func setupNetworkStateReceiverMocks() (*MockContext, *Intent) {
    ctx := new(MockContext)
    intent := NewIntent()
    return ctx, intent
}

// --- Tests ---

func TestReceiveRegistersWhenAllowed(t *testing.T) {
    gcmUtilsStub.SetCheckCanAndShouldRegisterResult(true)
    regIntent := NewIntent()
    gcmRegServiceStub.SetCreateGcmRegistrationIntentResult(regIntent)
    defer func() {
        gcmUtilsStub.Reset()
        gcmRegServiceStub.Reset()
    }()

    receiver := &NetworkStateReceiver{}
    receiver.On("StartWakefulService", mock.Anything, regIntent).Return()
    ctx, intent := setupNetworkStateReceiverMocks()

    receiver.OnReceive(ctx, intent)

    receiver.AssertCalled(t, "StartWakefulService", ctx, regIntent)
}

func TestReceiveDoesNothingIfNotAllowed(t *testing.T) {
    gcmUtilsStub.SetCheckCanAndShouldRegisterResult(false)
    defer func() {
        gcmUtilsStub.Reset()
        gcmRegServiceStub.Reset()
    }()

    receiver := &NetworkStateReceiver{}
    ctx, intent := setupNetworkStateReceiverMocks()

    receiver.OnReceive(ctx, intent)

    receiver.AssertNotCalled(t, "StartWakefulService", mock.Anything, mock.Anything)
}