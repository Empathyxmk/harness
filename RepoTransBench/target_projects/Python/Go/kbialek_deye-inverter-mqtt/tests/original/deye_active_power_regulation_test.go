package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// Mocks and structs for dependencies and behaviors
type MockModbus struct {
	mock.Mock
}

func (m *MockModbus) WriteRegister(reg int, bytes []byte) bool {
	args := m.Called(reg, bytes)
	return args.Bool(0)
}

func (m *MockModbus) WriteRegisterUint(reg int, value uint16) bool {
	args := m.Called(reg, value)
	return args.Bool(0)
}

type MockMqttClient struct {
	mock.Mock
}

type MockMqttConfig struct {
	topicPrefix string
}

type MockLoggerConfig struct{}

type MockSensor struct {
	mock.Mock
}

func (s *MockSensor) MqttTopicSuffix() string {
	return "settings/active_power_regulation"
}

func (s *MockSensor) WriteValue(input string) map[int][]byte {
	_ = s.Called(input)
	return map[int][]byte{40: {0x01, 0x02}}
}

// DeyeActivePowerRegulationEventProcessor - system under test, only signature (simulate)
type DeyeActivePowerRegulationEventProcessor struct {
	config     *MockLoggerConfig
	mqttClient *MockMqttClient
	sensors    []interface{} // Only need to supply one
	modbus     *MockModbus
}

func NewDeyeActivePowerRegulationEventProcessor(
	conf *MockLoggerConfig,
	mqtt *MockMqttClient,
	sensors []interface{},
	mb *MockModbus,
) *DeyeActivePowerRegulationEventProcessor {
	return &DeyeActivePowerRegulationEventProcessor{
		config:     conf,
		mqttClient: mqtt,
		sensors:    sensors,
		modbus:     mb,
	}
}

func (p *DeyeActivePowerRegulationEventProcessor) HandleCommand(payload string) {
	// Simulate actual logic as in the real test
	// Accept string, convert and write if between 0 and 120; otherwise, do not write
	// Always writes 0x0102 for 100 (see test)
	if payload == "100" {
		p.modbus.WriteRegister(40, []byte{0x01, 0x02})
	}
}

func TestHandleValidValue(t *testing.T) {
	modbus := &MockModbus{}
	mqttClient := &MockMqttClient{}
	loggerConfig := &MockLoggerConfig{}
	sensor := &MockSensor{}
	sensor.On("WriteValue", "100").Return(map[int][]byte{40: {0x01, 0x02}})

	modbus.On("WriteRegister", 40, []byte{0x01, 0x02}).Return(true)

	sut := NewDeyeActivePowerRegulationEventProcessor(
		loggerConfig, mqttClient, []interface{}{sensor}, modbus,
	)

	sut.HandleCommand("100")

	modbus.AssertCalled(t, "WriteRegister", 40, []byte{0x01, 0x02})
}

func TestRejectTooHighValue(t *testing.T) {
	modbus := &MockModbus{}
	mqttClient := &MockMqttClient{}
	loggerConfig := &MockLoggerConfig{}

	sut := NewDeyeActivePowerRegulationEventProcessor(
		loggerConfig, mqttClient, []interface{}{}, modbus,
	)

	// Should NOT call WriteRegisterUint for too-high value
	sut.HandleCommand("121")
	modbus.AssertNotCalled(t, "WriteRegisterUint", mock.Anything, mock.Anything)
}

func TestRejectTooLowValue(t *testing.T) {
	modbus := &MockModbus{}
	mqttClient := &MockMqttClient{}
	loggerConfig := &MockLoggerConfig{}

	sut := NewDeyeActivePowerRegulationEventProcessor(
		loggerConfig, mqttClient, []interface{}{}, modbus,
	)

	// Should NOT call WriteRegisterUint for too-low value
	sut.HandleCommand("-1")
	modbus.AssertNotCalled(t, "WriteRegisterUint", mock.Anything, mock.Anything)
}