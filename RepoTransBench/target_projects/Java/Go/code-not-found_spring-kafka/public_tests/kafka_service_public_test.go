package public_tests

import (
	"kafkaservice/kafkaservice"
	"strings"
	"testing"
)

func TestProcessMessage_valid_diff(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	result := service.ProcessMessage("Kafka Rocks")
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Processed: KAFKA ROCKS" {
		t.Errorf("Expected 'Processed: KAFKA ROCKS', got '%s'", result)
	}
}

func TestProcessMessage_null_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	result := service.ProcessMessage("")
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Error: Message cannot be empty." {
		t.Errorf("Expected 'Error: Message cannot be empty.', got '%s'", result)
	}
}

func TestProcessMessage_empty_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	result := service.ProcessMessage("")
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Error: Message cannot be empty." {
		t.Errorf("Expected 'Error: Message cannot be empty.', got '%s'", result)
	}
}

func TestProcessMessage_whitespace_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	result := service.ProcessMessage("\t\n")
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Error: Message cannot be empty." {
		t.Errorf("Expected 'Error: Message cannot be empty.', got '%s'", result)
	}
}

func TestProcessMessage_tooLong_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	longMsg := "Short messages are nice, but this one is way too long!!!"
	result := service.ProcessMessage(longMsg)
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Warning: Message too long." {
		t.Errorf("Expected 'Warning: Message too long.', got '%s'", result)
	}
}

func TestProcessMessage_boundaryLengthFifty_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	msg := "12345678901234567890123456789012345678901234567890" // 50 chars
	result := service.ProcessMessage(msg)
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Processed: 12345678901234567890123456789012345678901234567890" {
		t.Errorf("Expected 'Processed: 12345678901234567890123456789012345678901234567890', got '%s'", result)
	}
}

func TestProcessMessage_boundaryLengthFiftyOne_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	msg := "123456789012345678901234567890123456789012345678901" // 51 chars
	result := service.ProcessMessage(msg)
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Warning: Message too long." {
		t.Errorf("Expected 'Warning: Message too long.', got '%s'", result)
	}
}

func TestGetMessageLength_valid_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	length := service.GetMessageLength("Kafka")
	if length != 5 {
		t.Errorf("Expected 5, got %d", length)
	}
}

func TestGetMessageLength_null_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	length := service.GetMessageLength("")
	if length != 0 {
		t.Errorf("Expected 0, got %d", length)
	}
}

func TestGetMessageLength_empty_public(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	trimmed := strings.TrimSpace("   ")
	length := service.GetMessageLength(trimmed)
	if length != 0 {
		t.Errorf("Expected 0, got %d", length)
	}
}