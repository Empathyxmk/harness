package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type MockRocketMQTemplate struct {
	mock.Mock
}

func (m *MockRocketMQTemplate) Receive(className string) []string {
	args := m.Called(className)
	return args.Get(0).([]string)
}

type StringConsumer struct {
	rocketMQTemplate interface{ Receive(string) []string }
}

// consume returns the messages received from MQ
func (sc *StringConsumer) consume() []string {
	return sc.rocketMQTemplate.Receive("String")
}

func TestStringConsumerPublic_Consume(t *testing.T) {
	mockTemplate := new(MockRocketMQTemplate)
	sc := &StringConsumer{
		rocketMQTemplate: mockTemplate,
	}
	messages := []string{"foo", "bar", "baz"}
	mockTemplate.On("Receive", "String").Return(messages).Once()
	got := sc.consume()
	assert.Equal(t, 3, len(got))
	assert.Contains(t, got, "foo")
	assert.Equal(t, "bar", got[1])
	mockTemplate.AssertCalled(t, "Receive", "String")
}