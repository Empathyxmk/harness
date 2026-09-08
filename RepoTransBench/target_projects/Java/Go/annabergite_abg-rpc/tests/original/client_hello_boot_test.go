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

func TestHelloBoot(t *testing.T) {
	helloService := &mockHelloService{}
	res := helloService.Hello("Go")
	assert.True(t, len(res) > 0)
}