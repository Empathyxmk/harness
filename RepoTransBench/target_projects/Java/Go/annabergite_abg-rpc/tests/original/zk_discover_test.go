package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ZooKeeperDiscover struct {
	client   interface{}
	initd    bool
}

type Protocol interface {
	String() string
}

type HostPort struct {
	Host string
	Port int
}

type DiscoverListener interface {
	Changed()
}

func (z *ZooKeeperDiscover) Init(hps []HostPort) {
	z.initd = true
}

func (z *ZooKeeperDiscover) AddListener(group, app string, protocol Protocol, listener DiscoverListener) error {
	if listener == nil {
		return &NullPointerError{"listener is nil"}
	}
	if !z.initd {
		return &NullPointerError{"not initialized"}
	}
	return nil
}

// NullPointerError to simulate Java NPE behavior
type NullPointerError struct{ msg string }
func (e *NullPointerError) Error() string { return e.msg }

type mockProtocol struct{}

func (p *mockProtocol) String() string { return "proto" }

func TestInitAndAddListenerNullCheck(t *testing.T) {
	discover := &ZooKeeperDiscover{}
	discover.Init([]HostPort{{Host: "localhost", Port: 2181}})
	protocol := &mockProtocol{}

	assert.NotNil(t, discover)

	err := discover.AddListener("grp", "app", protocol, nil)
	assert.Error(t, err)
}

type fakeListener struct{}

func (fakeListener) Changed() {}

func TestAddListenerNoInit(t *testing.T) {
	discover := &ZooKeeperDiscover{}
	protocol := &mockProtocol{}
	listener := &fakeListener{}

	err := discover.AddListener("grp", "app", protocol, listener)
	assert.Error(t, err)
}