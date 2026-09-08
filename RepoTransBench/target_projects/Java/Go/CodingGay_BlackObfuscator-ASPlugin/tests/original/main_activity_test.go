package original

import (
	"testing"
)

// Dummy MainActivity structure for coverage
type MainActivity struct{}

// In real Java, this would accept a Bundle object, here just dummy.
func (m *MainActivity) OnCreate(bundle interface{}) {
	_ = abxGo() // for coverage, mimic Java's branch
	// Do nothing else. No crash == pass.
}

func TestOnCreateNoCrash(t *testing.T) {
	activity := &MainActivity{}
	var bundle interface{} = nil
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("MainActivity.OnCreate panicked: %v", r)
		}
	}()
	activity.OnCreate(bundle)
}