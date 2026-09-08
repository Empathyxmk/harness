package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type HttpResponseInterceptor func(response interface{}) error

type UnsuccessfulResponseHandlerChainer struct {
	Interceptors []HttpResponseInterceptor
}

func NewUnsuccessfulResponseHandlerChainer(interceptors ...HttpResponseInterceptor) *UnsuccessfulResponseHandlerChainer {
	return &UnsuccessfulResponseHandlerChainer{Interceptors: interceptors}
}

func (u *UnsuccessfulResponseHandlerChainer) InterceptResponse(resp interface{}) {
	for _, i := range u.Interceptors {
		_ = i(resp)
	}
}

func TestDifferentInterceptorChainDelegates(t *testing.T) {
	var called1, called2 bool
	interceptor1 := func(resp interface{}) error {
		called1 = true
		return nil
	}
	interceptor2 := func(resp interface{}) error {
		called2 = true
		return nil
	}
	resp := struct{}{}
	chain := NewUnsuccessfulResponseHandlerChainer(interceptor1, interceptor2)
	chain.InterceptResponse(resp)
	assert.True(t, called1)
	assert.True(t, called2)
}