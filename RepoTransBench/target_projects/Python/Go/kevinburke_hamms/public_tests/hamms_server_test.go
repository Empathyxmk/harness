package public_tests

import "testing"

func TestPublicServerTrue(t *testing.T) {
	if 100/5 != 20 {
		t.Errorf("Expected 100/5==20")
	}
}

func TestPublicServerOther(t *testing.T) {
	config := map[string]int{"foo": 5, "bar": 9}
	if _, ok := config["bar"]; !ok {
		t.Errorf("Expected 'bar' key in config map")
	}
}