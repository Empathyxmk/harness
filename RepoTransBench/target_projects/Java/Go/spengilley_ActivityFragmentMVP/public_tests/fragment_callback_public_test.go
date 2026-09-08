package public_tests

import (
	"testing"
)

type FragmentCallbackPublic interface {
	onAction(s string)
}

// test instance with string comparison
type fakeFragmentCallbackPublic struct {
	onActionFunc func(s string)
}

func (f *fakeFragmentCallbackPublic) onAction(s string) {
	f.onActionFunc(s)
}

func TestFragmentCallbackPublic_DummyTestForCallback(t *testing.T) {
	callback := &fakeFragmentCallbackPublic{
		onActionFunc: func(s string) {
			if s != "PublicAction" {
				t.Errorf("Expected s to be 'PublicAction', got %v", s)
			}
		},
	}
	callback.onAction("PublicAction")
}