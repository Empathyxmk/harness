package public_tests

import (
	"strings"
	"testing"

	"corbt-react-native-keep-awake"
)

// Public tests correspond to KeepAwakePublicTest.java

func TestNotAwakeAfterConstruction(t *testing.T) {
	ka := corbt.NewKeepAwake()
	if ka.IsAwake() {
		t.Errorf("Expected not awake after construction, got true")
	}
	if st := ka.GetStatus(); st == "Awake" {
		t.Errorf("Expected GetStatus not to be 'Awake' after construction, got 'Awake'")
	}
	if st := ka.GetStatus(); st != "Sleeping" {
		t.Errorf("Expected GetStatus to be 'Sleeping' after construction, got '%s'", st)
	}
}

func TestActivateFromFalse(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Activate()
	if !ka.IsAwake() {
		t.Errorf("Expected awake after Activate, got false")
	}
	if !strings.Contains(ka.GetStatus(), "Awake") {
		t.Errorf("Expected GetStatus to contain 'Awake' after Activate, got '%s'", ka.GetStatus())
	}
}

func TestDeactivateAfterActivation(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.SetAwake(true)
	ka.Deactivate()
	if ka.IsAwake() {
		t.Errorf("Expected sleeping after Deactivate, got IsAwake()=true")
	}
	if ka.GetStatus() == "Awake" {
		t.Errorf("Expected GetStatus not to be 'Awake' after deactivation, got 'Awake'")
	}
}

func TestMultipleActivatesRemainAwake(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Activate()
	ka.Activate()
	ka.Activate()
	if !ka.IsAwake() {
		t.Errorf("Expected awake after multiple Activates, got false")
	}
	if ka.GetStatus() != "Awake" {
		t.Errorf("Expected status to be 'Awake' after multiple Activates, got '%s'", ka.GetStatus())
	}
}

func TestMultipleDeactivatesRemainSleeping(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Deactivate()
	ka.Deactivate()
	if ka.IsAwake() {
		t.Errorf("Expected sleeping after multiple Deactivates, got IsAwake()=true")
	}
	if ka.GetStatus() != "Sleeping" {
		t.Errorf("Expected status to be 'Sleeping' after multiple Deactivates, got '%s'", ka.GetStatus())
	}
}

func TestSetAwakeToTrueSetsAwakeStatus(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.SetAwake(true)
	if !ka.IsAwake() {
		t.Errorf("Expected IsAwake() to be true after SetAwake(true), got false")
	}
	if ka.GetStatus() != "Awake" {
		t.Errorf("Expected status to be 'Awake' after SetAwake(true), got '%s'", ka.GetStatus())
	}
}

func TestSetAwakeToFalseFromAwake(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Activate()
	ka.SetAwake(false)
	if ka.IsAwake() {
		t.Errorf("Expected IsAwake() to be false after SetAwake(false), got true")
	}
	if ka.GetStatus() != "Sleeping" {
		t.Errorf("Expected status to be 'Sleeping' after SetAwake(false), got '%s'", ka.GetStatus())
	}
}

func TestToggleMultipleTimes(t *testing.T) {
	ka := corbt.NewKeepAwake()
	ka.Activate()
	if ka.GetStatus() != "Awake" {
		t.Errorf("Expected status to be 'Awake' after Activate, got '%s'", ka.GetStatus())
	}
	ka.Deactivate()
	if ka.GetStatus() != "Sleeping" {
		t.Errorf("Expected status to be 'Sleeping' after Deactivate, got '%s'", ka.GetStatus())
	}
	ka.Activate()
	if ka.GetStatus() != "Awake" {
		t.Errorf("Expected status to be 'Awake' after Activate (again), got '%s'", ka.GetStatus())
	}
	ka.Deactivate()
	if ka.GetStatus() != "Sleeping" {
		t.Errorf("Expected status to be 'Sleeping' after final Deactivate, got '%s'", ka.GetStatus())
	}
}