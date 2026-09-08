package original

import (
	"testing"
)

type DummyEngine struct {
	driverName string
}

func (d *DummyEngine) Say(text string) string {
	return text
}
func (d *DummyEngine) RunAndWait() string {
	return "ran"
}
func (d *DummyEngine) Stop() string {
	return "stopped"
}

// Simulate active engines cache (simple map)
var activeEngines = make(map[string]*DummyEngine)

func Pyttsx3Init(driverName string) *DummyEngine {
	if e, ok := activeEngines[driverName]; ok {
		return e
	}
	e := &DummyEngine{driverName: driverName}
	activeEngines[driverName] = e
	return e
}

func TestInitAndEngine(t *testing.T) {
	engine := Pyttsx3Init("dummy")
	if engine.driverName != "dummy" {
		t.Errorf("Expected driverName 'dummy', got '%s'", engine.driverName)
	}
}

func TestEngineCache(t *testing.T) {
	e1 := Pyttsx3Init("dummy")
	e2 := Pyttsx3Init("dummy")
	if e1 != e2 {
		t.Errorf("Expected cache to return same instance")
	}
}

func TestEngineUnique(t *testing.T) {
	e1 := Pyttsx3Init("dummy1")
	e2 := Pyttsx3Init("dummy2")
	if e1 == e2 {
		t.Errorf("Expected unique engines for different driver names")
	}
}

func TestEngineMethods(t *testing.T) {
	e := Pyttsx3Init("dummy")
	if e.Say("foo") != "foo" {
		t.Errorf("Say() did not return expected result")
	}
	if e.RunAndWait() != "ran" {
		t.Errorf("RunAndWait() not expected result")
	}
	if e.Stop() != "stopped" {
		t.Errorf("Stop() not expected result")
	}
}