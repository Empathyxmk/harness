package tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type ZooKeeperRegister struct {
	client interface{}
	initd  bool
}

type Protocol interface {
	String() string
}

type HostPort struct {
	Host string
	Port int
}

func (z *ZooKeeperRegister) Init(hps []HostPort) {
	z.initd = true
	z.client = struct{}{}
}

func (z *ZooKeeperRegister) Register(group, app string, protocol Protocol, serverAddr HostPort, weight int) error {
	if !z.initd || z.client == nil {
		return errors.New("NullPointerException")
	}
	return nil
}

type mockProtocol struct{}
func (m *mockProtocol) String() string { return "proto" }

func TestInitAndRegisterNullCheck(t *testing.T) {
	register := &ZooKeeperRegister{}
	register.Init([]HostPort{{Host: "localhost", Port: 2181}})
	protocol := &mockProtocol{}
	serverAddr := HostPort{"127.0.0.1", 9876}
	tmp := &ZooKeeperRegister{}
	err := tmp.Register("g", "a", protocol, serverAddr, 1)
	assert.Error(t, err)
}