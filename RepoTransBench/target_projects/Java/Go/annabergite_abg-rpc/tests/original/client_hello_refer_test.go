package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type HelloService interface {
	Hello(msg string) string
}
type mockHelloService struct{}
func (mockHelloService) Hello(msg string) string { return "hello: " + msg }

func TestHelloRefer(t *testing.T) {
	helloService := &mockHelloService{}
	res := helloService.Hello("test")
	assert.Equal(t, "hello: test", res)
}