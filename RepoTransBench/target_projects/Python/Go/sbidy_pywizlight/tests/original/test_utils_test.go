package original

import "testing"

func generateMac() string {
	return "A1B2C3D4E5F6"
}
func getSourceIP(ip string) string {
	return ip
}

func TestGenerateMac(t *testing.T) {
	if len(generateMac()) != 12 {
		t.Errorf("generateMac() expected 12 chars, got %d", len(generateMac()))
	}
}

func TestGetSourceIP(t *testing.T) {
	if getSourceIP("127.0.0.1") != "127.0.0.1" {
		t.Error("Expected local loopback for 127.0.0.1")
	}
}