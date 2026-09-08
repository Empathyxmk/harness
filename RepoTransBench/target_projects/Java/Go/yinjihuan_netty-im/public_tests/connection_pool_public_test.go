package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"yinjihuan_netty_im_go/tests"
)

func setup() { tests.ConnectionPoolClear() }

func TestPutAndGetChannelWithDifferentId(t *testing.T) {
	setup()
	assert.Nil(t, tests.ConnectionPoolGetChannel("public_id"))
	ch := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("publicUserA", ch))
	assert.Equal(t, ch, tests.ConnectionPoolGetChannel("publicUserA"))
}

func TestPutChannelReturnsOldValuePublic(t *testing.T) {
	setup()
	ch1 := &tests.MockChannel{}
	ch2 := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("publicClient", ch1))
	assert.Equal(t, ch1, tests.ConnectionPoolPutChannel("publicClient", ch2))
	assert.Equal(t, ch2, tests.ConnectionPoolGetChannel("publicClient"))
}

func TestGetChannelNullClientIdPublic(t *testing.T) {
	setup()
	assert.Nil(t, tests.ConnectionPoolGetChannel(""))
}

func TestGetClientsPublic(t *testing.T) {
	setup()
	ch := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("alice", ch))
	clients := tests.ConnectionPoolGetClients()
	foundAlice, foundBob := false, false
	for _, c := range clients {
		if c == "alice" {
			foundAlice = true
		}
		if c == "bob" {
			foundBob = true
		}
	}
	assert.True(t, foundAlice)
	assert.False(t, foundBob)
	assert.NotNil(t, clients)
}

func TestGetChannelsPublic(t *testing.T) {
	setup()
	ch := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("publicFour", ch))
	channels := tests.ConnectionPoolGetChannels()
	found := false
	for _, c := range channels {
		if c == ch {
			found = true
		}
	}
	assert.True(t, found)
	assert.Equal(t, len(tests.ConnectionPoolGetClients()), len(channels))
}

func TestPutChannelNullClientIdPublic(t *testing.T) {
	setup()
	ch := &tests.MockChannel{}
	assert.Nil(t, tests.ConnectionPoolPutChannel("", ch))
}