package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"yinjihuan_netty_im_go/tests"
)

func setup() { tests.ConnectionPoolClear() }

func TestPutAndGetChannel(t *testing.T) {
	setup()
	assert.Nil(t, tests.ConnectionPoolGetChannel("non_existent"))
	ch := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("client1", ch))
	assert.Equal(t, ch, tests.ConnectionPoolGetChannel("client1"))
}

func TestPutChannelReturnsOldValue(t *testing.T) {
	setup()
	ch1 := &tests.MockChannel{}
	ch2 := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("client2", ch1))
	assert.Equal(t, ch1, tests.ConnectionPoolPutChannel("client2", ch2))
	assert.Equal(t, ch2, tests.ConnectionPoolGetChannel("client2"))
}

func TestGetChannelNullClientId(t *testing.T) {
	setup()
	assert.Nil(t, tests.ConnectionPoolGetChannel(""))
}

func TestGetClients(t *testing.T) {
	setup()
	ch := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("cc", ch))
	clients := tests.ConnectionPoolGetClients()
	found := false
	for _, c := range clients {
		if c == "cc" {
			found = true
			break
		}
	}
	assert.True(t, found)
	assert.NotNil(t, clients)
}

func TestGetChannels(t *testing.T) {
	setup()
	ch := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("client3", ch))
	channels := tests.ConnectionPoolGetChannels()
	found := false
	for _, c := range channels {
		if c == ch {
			found = true
			break
		}
	}
	assert.True(t, found)
}

func TestPutChannelNullClientId(t *testing.T) {
	setup()
	ch := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("", ch))
}

// For mocking: expose mockChannel with correct method
type MockChannel tests.MockChannel