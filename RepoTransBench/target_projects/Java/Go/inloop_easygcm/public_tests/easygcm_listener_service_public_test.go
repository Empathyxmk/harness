package public_tests

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/inloop-easygcm/go-easygcm/tests/original"
)

// -- Public-specific stubber --
type easyGcmStubberPublic struct {
    calledOnMessage bool
}

var easyGcmStubPublic = &easyGcmStubberPublic{}

type spyListenerPublic struct{}

func (s *spyListenerPublic) OnMessage(from string, data original.Bundle) {
    if from == "public_sender" && data["another_key"] == "another_value" {
        easyGcmStubPublic.calledOnMessage = true
    }
}

type EasyGcmListenerServicePublic struct{}

func (s *EasyGcmListenerServicePublic) OnMessageReceived(from string, data original.Bundle) {
    if easyGcmStubPublic != nil {
        (&original.GcmListenerAdapter{PublicSpy: &spyListenerPublic{}}).OnMessage(from, data)
    }
}

type GcmListenerAdapter struct {
    PublicSpy *spyListenerPublic
}

func (g *GcmListenerAdapter) OnMessage(from string, data original.Bundle) {
    g.PublicSpy.OnMessage(from, data)
}

func (s *easyGcmStubberPublic) SetGcmListenerSpy() {
    s.calledOnMessage = false
}

func (s *easyGcmStubberPublic) Reset() {
    s.calledOnMessage = false
}

func TestOnMessageReceivedDelegatesToEasyGcmDifferent(t *testing.T) {
    from := "public_sender"
    data := original.Bundle{"another_key": "another_value"}
    easyGcmStubPublic.SetGcmListenerSpy()

    (&EasyGcmListenerServicePublic{}).OnMessageReceived(from, data)

    assert.True(t, easyGcmStubPublic.calledOnMessage)
    easyGcmStubPublic.Reset()
}