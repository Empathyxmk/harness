package original

import (
	"testing"

	"corbt-react-native-keep-awake"
)

func TestInitialState(t *testing.T) {
	ka := corbt.NewKeepAwake()
	if ka.IsAwake() {
		t.Errorf("Expected initial awake state to be false, got true")
	}
	if st := ka.GetStatus(); st != "Sleeping" {
		t.Errorf("Expected initial status to be 'Sleeping', got '%s'", st)
	}
}

func TestActivate(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Activate()
	if !ka.IsAwake() {
		t.Errorf("Expected awake after Activate, got false")
	}
	if st := ka.GetStatus(); st != "Awake" {
		t.Errorf("Expected status to be 'Awake' after Activate, got '%s'", st)
	}
}

func TestDeactivate(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Activate()
	ka.Deactivate()
	if ka.IsAwake() {
		t.Errorf("Expected not awake after Deactivate, got true")
	}
	if st := ka.GetStatus(); st != "Sleeping" {
		t.Errorf("Expected status to be 'Sleeping' after Deactivate, got '%s'", st)
	}
}

func TestActivateIdempotence(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Activate()
	ka.Activate() // Should remain true
	if !ka.IsAwake() {
		t.Errorf("Expected IsAwake to remain true after double Activate, got false")
	}
}

func TestDeactivateIdempotence(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Deactivate() // Still false
	if ka.IsAwake() {
		t.Errorf("Expected IsAwake to be false after Deactivate from initial, got true")
	}
}

func TestSetAwakeTrue(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.SetAwake(true)
	if !ka.IsAwake() {
		t.Errorf("Expected IsAwake to be true after SetAwake(true), got false")
	}
}

func TestSetAwakeFalse(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.SetAwake(true)
	ka.SetAwake(false)
	if ka.IsAwake() {
		t.Errorf("Expected IsAwake to be false after SetAwake(false), got true")
	}
}

func TestMultipleTransitions(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.SetAwake(true)
	if st := ka.GetStatus(); st != "Awake" {
		t.Errorf("After SetAwake(true), status should be 'Awake', got '%s'", st)
	}
	ka.SetAwake(false)
	if st := ka.GetStatus(); st != "Sleeping" {
		t.Errorf("After SetAwake(false), status should be 'Sleeping', got '%s'", st)
	}
	ka.SetAwake(true)
	if st := ka.GetStatus(); st != "Awake" {
		t.Errorf("After SetAwake(true) again, status should be 'Awake', got '%s'", st)
	}
}