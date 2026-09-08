package original

import (
	"reflect"
	"testing"
)

// Test Application data store
func TestApplicationStoresData(t *testing.T) {
	appData := map[string]interface{}{
		"id":         "com.test.app",
		"title":      "TestApp",
		"foreground": true,
	}
	app := NewApplication(appData)
	if !reflect.DeepEqual(app.Data, appData) {
		t.Errorf("Application Data mismatch. Got: %v, want: %v", app.Data, appData)
	}
}