package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type FlinkRestClient struct {
	address string
	port    int
}

func NewFlinkRestClient(host string, port int) *FlinkRestClient {
	return &FlinkRestClient{address: host, port: port}
}

func (c *FlinkRestClient) GetRestAddress() string { return c.address }
func (c *FlinkRestClient) GetRestPort() int       { return c.port }

func TestAddressWithPort(t *testing.T) {
	client := NewFlinkRestClient("192.168.0.100", 9000)
	assert.Equal(t, "192.168.0.100", client.GetRestAddress())
	assert.Equal(t, 9000, client.GetRestPort())
}

func TestRestAddressNotDefault(t *testing.T) {
	client := NewFlinkRestClient("example.com", 12345)
	assert.NotEqual(t, "localhost", client.GetRestAddress())
	assert.Equal(t, 12345, client.GetRestPort())
}