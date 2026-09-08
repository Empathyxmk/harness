package public_tests

import (
	"github.com/supersaiyanmode_PyWebOSTV/tests/original"
	"reflect"
	"testing"
)

func TestPublicApplicationStoresData(t *testing.T) {
	appData := map[string]interface{}{"id": "x.public", "active": true}
	app := original.NewApplication(appData)
	if !reflect.DeepEqual(app.Data, appData) {
		t.Errorf("Application Data mismatch. Got: %v, want: %v", app.Data, appData)
	}
}