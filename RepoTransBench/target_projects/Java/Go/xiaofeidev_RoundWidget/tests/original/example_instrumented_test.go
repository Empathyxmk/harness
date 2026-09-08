package original

import (
	"testing"
)

type MockAppContext struct{}

func (c *MockAppContext) PackageName() string {
	return "com.github.xiaofeidev.round.test"
}

func TestUseAppContext(t *testing.T) {
	appContext := &MockAppContext{}
	if got, want := appContext.PackageName(), "com.github.xiaofeidev.round.test"; got != want {
		t.Errorf("got package name %v, want %v", got, want)
	}
}