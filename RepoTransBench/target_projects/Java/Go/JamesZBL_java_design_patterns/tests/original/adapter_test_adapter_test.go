package original

import (
	"testing"

	"jameszbl_java_design_patterns/adapter"
)

func TestAdapter(t *testing.T) {
	busAdapter := adapter.NewBusAdapter()
	driver := adapter.NewDriver(busAdapter)

	// When calling drive, the call should hit busAdapter's Run
	called := false
	busAdapter.SetRunFunc(func() {
		called = true
	})
	driver.Drive()
	if !called {
		t.Error("expected driver.Drive() to invoke busAdapter.Run()")
	}

	// Adapter should also support drive directly
	called2 := false
	busAdapter.SetDriveFunc(func() {
		called2 = true
	})
	busAdapter.Drive()
	if !called2 {
		t.Error("expected busAdapter.Drive() to use provided drive func")
	}
}