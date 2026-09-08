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
type RpcServerFilter interface {
	OnSend(req *Request, resp *Response)
	OnReceive(req *Request) bool
	OnError(req *Request, resp *Response, err error)
}
type mockRpcServerFilter struct {
	sendCalled    bool
	receiveCalled bool
	errorCalled   bool
}
func (f *mockRpcServerFilter) OnSend(req *Request, resp *Response) {
	f.sendCalled = true
}
func (f *mockRpcServerFilter) OnReceive(req *Request) bool {
	f.receiveCalled = true
	return true
}
func (f *mockRpcServerFilter) OnError(req *Request, resp *Response, err error) {
	f.errorCalled = true
}

func TestTruboServerFilter(t *testing.T) {
	req := &Request{ID: 1}
	resp := &Response{ID: 2}
	filter := &mockRpcServerFilter{}

	filter.OnSend(req, resp)
	assert.True(t, filter.sendCalled)
	ok := filter.OnReceive(req)
	assert.True(t, ok)
	assert.True(t, filter.receiveCalled)
	filter.OnError(req, resp, nil)
	assert.True(t, filter.errorCalled)
}