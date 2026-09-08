package public_tests

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummySession struct {
	Connected   bool
	Disconnected bool
	DomainValue string
	BeanValue   string
	Closed      bool
}

func (s *DummySession) SetDomain(domain string) { s.DomainValue = domain }
func (s *DummySession) GetDomain() string       { return s.DomainValue }
func (s *DummySession) SetBean(bean string)     { s.BeanValue = bean }
func (s *DummySession) GetBean() string         { return s.BeanValue }
func (s *DummySession) Close()                  { s.Closed = true }
func (s *DummySession) IsClosed() bool          { return s.Closed }
func (s *DummySession) Connect(env map[string]interface{}) {
	if env != nil {
		if _, ok := env["secret"]; ok {
			s.Connected = true
		}
	}
}
func (s *DummySession) Disconnect() { s.Disconnected = true }
func (s *DummySession) IsConnected() bool {
	return s.Connected
}

func TestGetDomain_public(t *testing.T) {
	s := &DummySession{}
	s.SetDomain("anotherDomain")
	assert.Equal(t, "anotherDomain", s.GetDomain())
}

func TestBean_public(t *testing.T) {
	s := &DummySession{}
	s.SetBean("myBeanXX")
	assert.Equal(t, "myBeanXX", s.GetBean())
}

func TestClose_public(t *testing.T) {
	s := &DummySession{}
	s.Close()
	assert.True(t, s.IsClosed())
}

func TestIOandConnection_public(t *testing.T) {
	s := &DummySession{}
	env := map[string]interface{}{"secret": "value"}
	s.Connect(env)
	assert.True(t, s.IsConnected())
	s.Disconnect()
	assert.True(t, s.Disconnected)
}