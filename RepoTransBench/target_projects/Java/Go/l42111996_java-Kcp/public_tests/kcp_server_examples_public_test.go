package public_tests

import (
	"testing"
)

func TestSimplePublicServer(t *testing.T) {
	serverID := 42
	port := 16667
	expectedGreeting := "KCP Public Test Server Started (ServerID: 42, Port: 16667)"
	greeting := simulateServerStart(serverID, port)
	if greeting != expectedGreeting {
		t.Errorf("Expected '%s', got '%s'", expectedGreeting, greeting)
	}
}

func simulateServerStart(serverId int, port int) string {
	return "KCP Public Test Server Started (ServerID: " + itoa(serverId) + ", Port: " + itoa(port) + ")"
}

func itoa(i int) string {
	// Fast path for small ints
	var digits = "0123456789"
	if i == 0 {
		return "0"
	}
	neg := i < 0
	if neg {
		i = -i
	}
	result := [20]byte{}
	pos := len(result)
	for i > 0 {
		pos--
		result[pos] = digits[i%10]
		i /= 10
	}
	if neg {
		pos--
		result[pos] = '-'
	}
	return string(result[pos:])
}