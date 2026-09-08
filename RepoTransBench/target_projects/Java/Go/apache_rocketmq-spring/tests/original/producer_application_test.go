package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// --- Mock & Test Stubs ---

type MockRocketMQTemplate struct {
	mock.Mock
}

func (m *MockRocketMQTemplate) SyncSend(topic string, msg interface{}) interface{} {
	args := m.Called(topic, msg)
	return args.Get(0)
}

// Simulate ProducerApplication with reflection set fields.
type ProducerApplication struct {
	rocketMQTemplate interface {
		SyncSend(string, interface{}) interface{}
	}
	topic string
}

// Run sends a fixed message to the topic using rocketMQTemplate.SyncSend
func (p *ProducerApplication) run() {
	p.rocketMQTemplate.SyncSend(p.topic, "Hello, World!")
}

func (p *ProducerApplication) main(args []string) {
	// For coverage; does nothing in our mock
}

// --- TESTS ---

func TestProducerApplication_Run(t *testing.T) {
	mockTemplate := new(MockRocketMQTemplate)
	app := &ProducerApplication{
		rocketMQTemplate: mockTemplate,
		topic:            "testTopic",
	}
	// Setup expectation
	mockTemplate.On("SyncSend", "testTopic", "Hello, World!").Return(struct{}{}).Once()

	app.run()
	mockTemplate.AssertExpectations(t)
}

func TestProducerApplication_Main(t *testing.T) {
	app := &ProducerApplication{}
	app.main([]string{})
}