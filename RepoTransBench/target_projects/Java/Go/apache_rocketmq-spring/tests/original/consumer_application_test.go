package original

import (
	"testing"

	"github.com/stretchr/testify/mock"
)

// --- Mock ---

type MockRocketMQTemplate struct {
	mock.Mock
}

func (m *MockRocketMQTemplate) Receive(className string) []string {
	args := m.Called(className)
	return args.Get(0).([]string)
}

type ConsumerApplication struct {
	rocketMQTemplate    interface{ Receive(string) []string }
	extRocketMQTemplate interface{ Receive(string) []string }
}

func (c *ConsumerApplication) run() {
	c.rocketMQTemplate.Receive("String")
	c.extRocketMQTemplate.Receive("String")
}

func (c *ConsumerApplication) main(args []string) {}

func TestConsumerApplication_Run(t *testing.T) {
	mockTemplate := new(MockRocketMQTemplate)
	mockExtTemplate := new(MockRocketMQTemplate)
	app := &ConsumerApplication{
		rocketMQTemplate:    mockTemplate,
		extRocketMQTemplate: mockExtTemplate,
	}
	mockList := []string{"msg1", "msg2"}
	mockTemplate.On("Receive", "String").Return(mockList).Once()
	mockExtTemplate.On("Receive", "String").Return(mockList).Once()

	app.run()
	mockTemplate.AssertCalled(t, "Receive", "String")
	mockExtTemplate.AssertCalled(t, "Receive", "String")
}

func TestConsumerApplication_Main(t *testing.T) {
	app := &ConsumerApplication{}
	app.main([]string{})
}