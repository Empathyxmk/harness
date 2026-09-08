package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type StringConsumer struct{}

func (sc *StringConsumer) OnMessage(msg string) {
	// Do nothing, for test coverage
}

func TestStringConsumer_OnMessage(t *testing.T) {
	consumer := &StringConsumer{}
	assert.NotPanics(t, func() { consumer.OnMessage("hello test") })
}