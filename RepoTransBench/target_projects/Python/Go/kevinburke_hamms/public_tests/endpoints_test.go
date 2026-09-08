package public_tests

import "testing"

func TestPublicDummyEndpoint(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("Expected 2+2==4")
	}
}

func TestPublicEndpointString(t *testing.T) {
	if !contains("myapiendpoint", "api") {
		t.Errorf("'api' not found in 'myapiendpoint'")
	}
}

func TestPublicEndpointNumeric(t *testing.T) {
	if 9*3 != 27 {
		t.Errorf("Expected 9*3==27")
	}
}

func contains(s, substr string) bool {
	return len(substr) == 0 || (len(s) >= len(substr) && (s == substr || len(s) > len(substr) && (s[0:len(substr)] == substr || contains(s[1:], substr))))
}