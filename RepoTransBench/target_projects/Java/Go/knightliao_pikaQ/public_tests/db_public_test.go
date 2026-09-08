package public_tests

import "testing"

const DB_NAME = "pikaqDemoWeb"

func TestDBNameConstantDifferent(t *testing.T) {
	if !(func() bool { return
		func() bool {
			return contains(DB_NAME, "DemoWeb")
		}()
	})() {
		t.Errorf("DB_NAME does not contain DemoWeb: %s", DB_NAME)
	}
}

func contains(str, substr string) bool {
	return len(str) >= len(substr) && (str == substr || containsInner(str, substr))
}
func containsInner(str, substr string) bool {
	for i := 0; i+len(substr) <= len(str); i++ {
		if str[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}