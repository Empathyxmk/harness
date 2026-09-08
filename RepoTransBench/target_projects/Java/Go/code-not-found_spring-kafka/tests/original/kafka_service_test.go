package original

import (
	"kafkaservice/kafkaservice"
	"testing"
)

func TestProcessMessage_valid(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	result := service.ProcessMessage("hello world")
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Processed: HELLO WORLD" {
		t.Errorf("Expected 'Processed: HELLO WORLD', got '%s'", result)
	}
}

func TestProcessMessage_null(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	result := service.ProcessMessage("")
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Error: Message cannot be empty." {
		t.Errorf("Expected 'Error: Message cannot be empty.', got '%s'", result)
	}
}

func TestProcessMessage_empty(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	result := service.ProcessMessage("")
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Error: Message cannot be empty." {
		t.Errorf("Expected 'Error: Message cannot be empty.', got '%s'", result)
	}
}

func TestProcessMessage_whitespace(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	result := service.ProcessMessage("   ")
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Error: Message cannot be empty." {
		t.Errorf("Expected 'Error: Message cannot be empty.', got '%s'", result)
	}
}

func TestProcessMessage_tooLong(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	longMessage := "This is a very long message that definitely exceeds fifty characters in length and will trigger the warning message condition."
	result := service.ProcessMessage(longMessage)
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Warning: Message too long." {
		t.Errorf("Expected 'Warning: Message too long.', got '%s'", result)
	}
}

func TestProcessMessage_boundaryLengthFifty(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	fiftyCharMsg := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX" // 50 chars
	result := service.ProcessMessage(fiftyCharMsg)
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Processed: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWX" {
		t.Errorf("Expected 'Processed: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWX', got '%s'", result)
	}
}

func TestProcessMessage_boundaryLengthFiftyOne(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	fiftyOneCharMsg := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY" // 51 chars
	result := service.ProcessMessage(fiftyOneCharMsg)
	if result == "" {
		t.Error("Expected non-empty result")
	}
	if result != "Warning: Message too long." {
		t.Errorf("Expected 'Warning: Message too long.', got '%s'", result)
	}
}

func TestGetMessageLength_valid(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	length := service.GetMessageLength("test")
	if length != 4 {
		t.Errorf("Expected 4, got %d", length)
	}
}

func TestGetMessageLength_null(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	length := service.GetMessageLength("")
	if length != 0 {
		t.Errorf("Expected 0, got %d", length)
	}
}

func TestGetMessageLength_empty(t *testing.T) {
	service := &kafkaservice.KafkaService{}
	length := service.GetMessageLength("")
	if length != 0 {
		t.Errorf("Expected 0, got %d", length)
	}
}