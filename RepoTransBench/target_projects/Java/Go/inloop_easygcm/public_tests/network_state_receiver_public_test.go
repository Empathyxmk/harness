package public_tests

import (
    "testing"

    "github.com/stretchr/testify/mock"
    "github.com/inloop-easygcm/go-easygcm/tests/original"
)

// --- Public stubbers with public-specific data ---

var gcmUtilsPublicStub = &gcmUtilsStubberPublic{}
var gcmRegServicePublicStub = &gcmRegistrationServiceStubberPublic{}

func GcmUtilsCheckCanAndShouldRegisterPublic(ctx original.Context) bool {
    if gcmUtilsPublicStub.override {
        return gcmUtilsPublicStub.forcedResult
    }
    return false
}
type gcmUtilsStubberPublic struct {
    forcedResult bool
    override     bool
}
func (g *gcmUtilsStubberPublic) SetCheckCanAndShouldRegisterResult(res bool) {
    g.forcedResult = res
    g.override = true
}
func (g *gcmUtilsStubberPublic) Reset() {
    g.forcedResult = false
    g.override = false
}

func GcmRegistrationServiceCreateGcmRegistrationIntentPublic(ctx original.Context, hasWakeLock bool) *original.Intent {
    if gcmRegServicePublicStub.forcedIntent != nil {
        return gcmRegServicePublicStub.forcedIntent
    }
    return &original.Intent{}
}
type gcmRegistrationServiceStubberPublic struct {
    forcedIntent *original.Intent
}
func (g *gcmRegistrationServiceStubberPublic) SetCreateGcmRegistrationIntentResult(intent *original.Intent) {
    g.forcedIntent = intent
}
func (g *gcmRegistrationServiceStubberPublic) Reset() {
    g.forcedIntent = nil
}

type NetworkStateReceiverPublic struct {
    mock.Mock
}

func (n *NetworkStateReceiverPublic) OnReceive(ctx original.Context, intent *original.Intent) {
    if GcmUtilsCheckCanAndShouldRegisterPublic(ctx) {
        regIntent := GcmRegistrationServiceCreateGcmRegistrationIntentPublic(ctx, true)
        n.StartWakefulService(ctx, regIntent)
    }
}

func (n *NetworkStateReceiverPublic) StartWakefulService(ctx original.Context, intent *original.Intent) {
    n.Called(ctx, intent)
}

func setupNetworkStateReceiverMocksPublic() (*original.MockContext, *original.Intent) {
    ctx := new(original.MockContext)
    intent := &original.Intent{}
    return ctx, intent
}

// --- Tests ---

func TestReceiveRegistersWhenAllowedPublic(t *testing.T) {
    gcmUtilsPublicStub.SetCheckCanAndShouldRegisterResult(true)

    regIntent := &original.Intent{}
    gcmRegServicePublicStub.SetCreateGcmRegistrationIntentResult(regIntent)
    defer func() {
        gcmUtilsPublicStub.Reset()
        gcmRegServicePublicStub.Reset()
    }()

    receiver := &NetworkStateReceiverPublic{}
    receiver.On("StartWakefulService", mock.Anything, regIntent).Return()
    ctx, intent := setupNetworkStateReceiverMocksPublic()

    receiver.OnReceive(ctx, intent)

    receiver.AssertCalled(t, "StartWakefulService", ctx, regIntent)
}

func TestReceiveDoesNothingIfNotAllowedPublic(t *testing.T) {
    gcmUtilsPublicStub.SetCheckCanAndShouldRegisterResult(false)
    defer func() {
        gcmUtilsPublicStub.Reset()
        gcmRegServicePublicStub.Reset()
    }()

    receiver := &NetworkStateReceiverPublic{}
    ctx, intent := setupNetworkStateReceiverMocksPublic()

    receiver.OnReceive(ctx, intent)

    receiver.AssertNotCalled(t, "StartWakefulService", mock.Anything, mock.Anything)
}