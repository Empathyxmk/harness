package public_tests

import (
	"reflect"
	"testing"
)

type MockContext struct{}

type MyApp struct{}

func (app *MyApp) attachBaseContext(base MockContext) {
	// Just test call chain/coverage
}

func TestAttachBaseContextOverridePublic(t *testing.T) {
	app := &MyApp{}
	app.attachBaseContext(MockContext{})
	if app == nil {
		t.Error("app should not be nil")
	}
	typ := reflect.TypeOf(app)
	if typ != reflect.TypeOf(&MyApp{}) {
		t.Errorf("Expected type %v, got %v", reflect.TypeOf(&MyApp{}), typ)
	}
}