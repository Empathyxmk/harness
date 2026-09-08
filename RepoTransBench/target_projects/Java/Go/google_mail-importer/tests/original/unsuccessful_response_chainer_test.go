package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// MockHttpUnsuccessfulResponseHandler is a mock for a handler function.
type MockHttpUnsuccessfulResponseHandler struct {
	mock.Mock
	Name string
	CalledFlag *bool
	ReturnVal  bool
}

func (m *MockHttpUnsuccessfulResponseHandler) Handle(req, resp interface{}, supportsRetry bool) bool {
	m.Called()
	if m.CalledFlag != nil {
		*m.CalledFlag = true
	}
	return m.ReturnVal
}

type UnsuccessfulResponseHandlerChainer struct{}

func (u *UnsuccessfulResponseHandlerChainer) Chain(handlers ...*MockHttpUnsuccessfulResponseHandler) *ChainHandler {
	return &ChainHandler{Handlers: handlers}
}

type ChainHandler struct {
	Handlers []*MockHttpUnsuccessfulResponseHandler
}

func (c *ChainHandler) Handle(req, resp interface{}, supportsRetry bool) {
	for _, h := range c.Handlers {
		val := h.Handle(req, resp, supportsRetry)
		if val {
			break
		}
	}
}

func TestChainOfZero(t *testing.T) {
	chainer := &UnsuccessfulResponseHandlerChainer{}
	handler := chainer.Chain()
	handler.Handle(nil, nil, true)
}

func TestChainOfOne(t *testing.T) {
	var flag bool
	handler := &MockHttpUnsuccessfulResponseHandler{CalledFlag: &flag}
	chainer := &UnsuccessfulResponseHandlerChainer{}
	chain := chainer.Chain(handler)
	chain.Handle(nil, nil, true)
	assert.True(t, flag)
}

func TestChainOfTwo(t *testing.T) {
	flag1, flag2 := false, false
	h1 := &MockHttpUnsuccessfulResponseHandler{CalledFlag: &flag1}
	h2 := &MockHttpUnsuccessfulResponseHandler{CalledFlag: &flag2}
	chainer := &UnsuccessfulResponseHandlerChainer{}
	chain := chainer.Chain(h1, h2)
	chain.Handle(nil, nil, true)
	assert.True(t, flag1)
	assert.True(t, flag2)
}

func TestChainOnlyCallsUntilTrue(t *testing.T) {
	flag1, flag2 := false, false
	h1 := &MockHttpUnsuccessfulResponseHandler{CalledFlag: &flag1, ReturnVal: true}
	h2 := &MockHttpUnsuccessfulResponseHandler{CalledFlag: &flag2}
	chainer := &UnsuccessfulResponseHandlerChainer{}
	chain := chainer.Chain(h1, h2)
	chain.Handle(nil, nil, true)
	assert.True(t, flag1)
	assert.False(t, flag2)
}