package original

import (
    "testing"

    "github.com/stretchr/testify/assert"
)

// --- Interfaces ---

type Bundle map[string]interface{}
type GcmListener interface {
    OnMessage(from string, data Bundle)
}
type EasyGcmListenerService struct{}

var easyGcmStubber = &EasyGcmStubber{}

func (s *EasyGcmListenerService) OnMessageReceived(from string, data Bundle) {
    if easyGcmStubber.gcmListener != nil {
        easyGcmStubber.gcmListener.OnMessage(from, data)
    }
}

// --- Stubber for EasyGcm Static/Singleton ---

type EasyGcmStubber struct {
    calledOnMessage bool
    gcmListener     GcmListener
}

func (s *EasyGcmStubber) SetGcmListenerSpy() {
    s.calledOnMessage = false
    s.gcmListener = &spyListener{s}
}

func (s *EasyGcmStubber) Reset() {
    s.calledOnMessage = false
    s.gcmListener = nil
}

type spyListener struct {
    stubber *EasyGcmStubber
}

func (s *spyListener) OnMessage(from string, data Bundle) {
    s.stubber.calledOnMessage = true
}

// --- Test ---

func TestOnMessageReceivedDelegatesToEasyGcm(t *testing.T) {
    from := "sender"
    data := Bundle{"key": "value"}
    easyGcmStubber.SetGcmListenerSpy()

    svc := &EasyGcmListenerService{}
    svc.OnMessageReceived(from, data)

    assert.True(t, easyGcmStubber.calledOnMessage)
    easyGcmStubber.Reset()
}