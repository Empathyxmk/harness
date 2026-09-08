package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Request struct {
	RequestID int
	ServiceID int
	// Params []interface{}
}
type Response struct {
	RequestID  int
	StatusCode byte
	Result     interface{}
}

type UserService interface {
	GetUser(int) interface{}
	ListUser(int) interface{}
}

type UserServiceServerImpl struct{}

func (u *UserServiceServerImpl) GetUser(i int) interface{}    { return "user" }
func (u *UserServiceServerImpl) ListUser(i int) interface{}   { return []string{"user1", "user2"} }

type ProtostuffSerializer struct{}

func (p *ProtostuffSerializer) WriteRequest(buf *[]byte, r *Request) {
	// dummy serializing
	*buf = append(*buf, byte(r.RequestID), byte(r.ServiceID))
}
func (p *ProtostuffSerializer) ReadRequest(buf []byte) *Request {
	return &Request{RequestID: int(buf[0]), ServiceID: int(buf[1])}
}
func (p *ProtostuffSerializer) WriteResponse(buf *[]byte, r *Response) {
	*buf = append(*buf, byte(r.RequestID), r.StatusCode)
}
func (p *ProtostuffSerializer) ReadResponse(buf []byte) *Response {
	return &Response{RequestID: int(buf[0]), StatusCode: buf[1], Result: nil}
}

func TestProtostuffSerializer(t *testing.T) {
	serializer := &ProtostuffSerializer{}
	userService := &UserServiceServerImpl{}

	buf := make([]byte, 0, 1024)
	req := &Request{RequestID: 123, ServiceID: 8}
	serializer.WriteRequest(&buf, req)
	readReq := serializer.ReadRequest(buf)
	assert.Equal(t, req.RequestID, readReq.RequestID)
	assert.Equal(t, req.ServiceID, readReq.ServiceID)

	buf = buf[:0]
	resp := &Response{RequestID: 321, StatusCode: 1, Result: userService.ListUser(0)}
	serializer.WriteResponse(&buf, resp)
	readResp := serializer.ReadResponse(buf)
	assert.Equal(t, resp.RequestID, readResp.RequestID)
	assert.Equal(t, resp.StatusCode, readResp.StatusCode)
}