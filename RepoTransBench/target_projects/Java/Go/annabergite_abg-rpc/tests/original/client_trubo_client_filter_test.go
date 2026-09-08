package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Request struct {
	ID int
}
type Response struct {
	ID int
}
type RpcClientFilter interface {
	OnSend(req *Request) bool
	OnReceive(req *Request, resp *Response)
	OnError(req *Request, resp *Response, err error)
}
type mockRpcClientFilter struct {
	sendCalled   bool
	receiveCalled bool
	errorCalled   bool
}
func (f *mockRpcClientFilter) OnSend(req *Request) bool {
	f.sendCalled = true
	return true
}
func (f *mockRpcClientFilter) OnReceive(req *Request, resp *Response) {
	f.receiveCalled = true
}
func (f *mockRpcClientFilter) OnError(req *Request, resp *Response, err error) {
	f.errorCalled = true
}

func TestTruboClientFilter(t *testing.T) {
	req := &Request{ID: 1}
	resp := &Response{ID: 2}
	filter := &mockRpcClientFilter{}

	ok := filter.OnSend(req)
	assert.True(t, ok)
	filter.OnReceive(req, resp)
	assert.True(t, filter.receiveCalled)
	filter.OnError(req, resp, nil)
	assert.True(t, filter.errorCalled)
}