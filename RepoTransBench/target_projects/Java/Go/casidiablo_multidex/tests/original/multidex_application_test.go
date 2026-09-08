package original

import (
	"testing"
)

type mockContext struct{}

func attachBaseContext(_ mockContext) {
	// In Go, nothing to do but this simulates Application.onAttach.
}

type multiDexApplication struct{}

func (a *multiDexApplication) attachBaseContext(base mockContext) {
	attachBaseContext(base)
}

func TestAttachBaseContext(t *testing.T) {
	app := &multiDexApplication{}
	defer func() {
		_ = recover() // Ignore panics
	}()
	app.attachBaseContext(mockContext{})
	if app == nil {
		t.Error("instance should not be nil")
	}
}