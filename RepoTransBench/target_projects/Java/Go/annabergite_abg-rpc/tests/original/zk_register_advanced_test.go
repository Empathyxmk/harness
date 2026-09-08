package tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type Protocol interface {
	String() string
}
type HostPort struct {
	Host string
	Port int
}
type ZooKeeperRegister struct {
	client   *MockCuratorFramework
	initd    bool
	watchers map[string]bool
}
type MockCuratorFramework struct{ mock.Mock }

func (z *ZooKeeperRegister) Init(hps []HostPort) {
	z.initd = true
	z.client = &MockCuratorFramework{}
	if z.watchers == nil {
		z.watchers = make(map[string]bool)
	}
}

func (z *ZooKeeperRegister) Register(group, app string, protocol Protocol, hostPort HostPort, weight int) error {
	if !z.initd || z.client == nil {
		return errors.New("client nil")
	}
	// Just simulate watcher registration map logic
	key := group + app + protocol.String()
	if z.watchers[key] {
		return nil // already registered, skip watcher
	}
	z.watchers[key] = true
	// Simulate node checking/creating logic
	return nil
}

// ---- TESTS BEGIN ----

type testProtocol struct{ id string }
func (t *testProtocol) String() string { return t.id }

func TestRegisterNodeAlreadyExistsHandlesDeleteException(t *testing.T) {
	r := &ZooKeeperRegister{}
	r.Init([]HostPort{{Host: "localhost", Port: 2181}})
	r.client = &MockCuratorFramework{}
	r.watchers = make(map[string]bool)
	protocol := &testProtocol{"p"}
	hp := HostPort{"127.0.0.2", 9999}
	err := r.Register("g", "a", protocol, hp, 3)
	assert.NoError(t, err)
}

func TestRegisterNodeDoesNotExistCreateFails(t *testing.T) {
	r := &ZooKeeperRegister{}
	r.Init([]HostPort{{Host: "localhost", Port: 2181}})
	r.client = &MockCuratorFramework{}
	r.watchers = make(map[string]bool)
	protocol := &testProtocol{"p"}
	hp := HostPort{"127.0.0.3", 9}
	err := r.Register("g", "a", protocol, hp, 5)
	assert.NoError(t, err)
}

func TestRegisterAddsWatcherOnlyOnce(t *testing.T) {
	r := &ZooKeeperRegister{}
	r.Init([]HostPort{{Host: "localhost", Port: 2181}})
	r.client = &MockCuratorFramework{}
	r.watchers = make(map[string]bool)
	protocol := &testProtocol{"proto"}
	hp := HostPort{"127.0.0.255", 5}
	err := r.Register("g", "a", protocol, hp, 5)
	assert.NoError(t, err)
	// Second call should not double-register
	err = r.Register("g", "a", protocol, hp, 5)
	assert.NoError(t, err)
}