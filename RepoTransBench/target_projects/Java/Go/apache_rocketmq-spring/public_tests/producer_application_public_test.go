package public_tests

import (
	"testing"

	"github.com/stretchr/testify/mock"
)

// Mocks/stubs as in original package, but with public dataset

type MockRocketMQTemplate struct {
	mock.Mock
}

func (m *MockRocketMQTemplate) SyncSend(topic string, msg interface{}) interface{} {
	args := m.Called(topic, msg)
	return args.Get(0)
}

type ProducerApplication struct {
	rocketMQTemplate interface {
		SyncSend(string, interface{}) interface{}
	}
	topic string
}

func (p *ProducerApplication) run() {
	p.rocketMQTemplate.SyncSend(p.topic, "Hello, World!")
}

func (p *ProducerApplication) main(args []string) {}

func TestProducerApplicationPublic_Run(t *testing.T) {
	mockTemplate := new(MockRocketMQTemplate)
	app := &ProducerApplication{
		rocketMQTemplate: mockTemplate,
		topic:            "publicTopic",
	}
	mockTemplate.On("SyncSend", "publicTopic", "Hello, World!").Return(struct{}{}).Once()
	app.run()
	mockTemplate.AssertExpectations(t)
}

func TestProducerApplicationPublic_Main(t *testing.T) {
	app := &ProducerApplication{}
	app.main([]string{"public"})
}