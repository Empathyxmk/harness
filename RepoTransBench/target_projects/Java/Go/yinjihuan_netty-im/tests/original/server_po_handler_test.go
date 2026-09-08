package original

import (
	"testing"

	"yinjihuan_netty_im_go/tests"
	"github.com/stretchr/testify/assert"
)

func TestChannelReadBasic(t *testing.T) {
	handler := tests.NewServerPoHandler()
	ch := &tests.MockChannel{}
	err := handler.ChannelRead(ch, "hello")
	assert.NoError(t, err)
	writes := ch.GetWrittenMessages()
	found := false
	for _, msg := range writes {
		if msg == "hello" {
			found = true
			break
		}
	}
	assert.True(t, found)
}

func TestChannelReadNullMsg(t *testing.T) {
	handler := tests.NewServerPoHandler()
	ch := &tests.MockChannel{}
	err := handler.ChannelRead(ch, nil)
	assert.NoError(t, err)
	// Should not panic, simply no write.
}

type MockChannel tests.MockChannel