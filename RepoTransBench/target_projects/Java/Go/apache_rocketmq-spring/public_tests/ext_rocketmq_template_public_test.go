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

type ExtRocketMQTemplate struct {
	rocketMQTemplate interface{ Receive(string) []string }
}

func (e *ExtRocketMQTemplate) receiveMessage() []string {
	return e.rocketMQTemplate.Receive("String")
}

func TestExtRocketMQTemplatePublic_ReceiveMessage(t *testing.T) {
	mockTemplate := new(MockRocketMQTemplate)
	extTemplate := &ExtRocketMQTemplate{
		rocketMQTemplate: mockTemplate,
	}
	expected := []string{"alpha", "beta", "gamma"}
	mockTemplate.On("Receive", "String").Return(expected).Once()
	received := extTemplate.receiveMessage()
	assert.Equal(t, 3, len(received))
	assert.Equal(t, "alpha", received[0])
	assert.Contains(t, received, "beta")
	mockTemplate.AssertCalled(t, "Receive", "String")
}