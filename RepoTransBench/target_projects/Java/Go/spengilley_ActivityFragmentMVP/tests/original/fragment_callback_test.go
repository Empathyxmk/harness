package original

import "testing"

type FragmentCallback interface {
	loadDetailFragment()
	finishProcess()
}

// Coverage of the interface via implementation.
func TestFragmentCallback_Interface(t *testing.T) {
	// Anonymous struct implementing FragmentCallback.
	cb := &struct {
	}{}
	var calledLoad, calledFinish bool

	impl := struct {
		FragmentCallback
	}{
		FragmentCallback: struct {
			loadDetailFragmentFunc func()
			finishProcessFunc     func()
		}{
			loadDetailFragmentFunc: func() { calledLoad = true },
			finishProcessFunc:     func() { calledFinish = true },
		},
	}
	// Use a simple wrapper
	type callbackImpl struct{}

	// Implement interface directly
	var cb2 FragmentCallback = &callbackImpl{}
	cb2 = &struct{ FragmentCallback }{
		FragmentCallback: &struct {
			FragmentCallback
		}{},
	}
	// But for test, just call direct closures:
	calledLoad = false
	calledFinish = false
	fakeCallback := &fakeFragmentCallback{
		loadDetailFragmentFunc: func() { calledLoad = true },
		finishProcessFunc:      func() { calledFinish = true },
	}
	fakeCallback.loadDetailFragment()
	fakeCallback.finishProcess()
	if !calledLoad {
		t.Error("Expected loadDetailFragment to be called")
	}
	if !calledFinish {
		t.Error("Expected finishProcess to be called")
	}
}

// Provide a test implementation
type fakeFragmentCallback struct {
	loadDetailFragmentFunc func()
	finishProcessFunc      func()
}

func (f *fakeFragmentCallback) loadDetailFragment() {
	f.loadDetailFragmentFunc()
}
func (f *fakeFragmentCallback) finishProcess() {
	f.finishProcessFunc()
}