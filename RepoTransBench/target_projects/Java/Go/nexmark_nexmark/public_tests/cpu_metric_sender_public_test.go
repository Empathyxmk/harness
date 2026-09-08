package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type CpuMetricSender struct {
	host string
	port int
}

func NewCpuMetricSender(host string, port int) *CpuMetricSender {
	return &CpuMetricSender{host: host, port: port}
}

func (s *CpuMetricSender) GetHost() string { return s.host }
func (s *CpuMetricSender) GetPort() int    { return s.port }

func TestMetricSenderHostAndPort(t *testing.T) {
	sender := NewCpuMetricSender("testhost", 10000)
	assert.Equal(t, "testhost", sender.GetHost())
	assert.Equal(t, 10000, sender.GetPort())
}

func TestMetricSenderNegativePort(t *testing.T) {
	sender := NewCpuMetricSender("anotherhost", -1)
	assert.Equal(t, -1, sender.GetPort())
}