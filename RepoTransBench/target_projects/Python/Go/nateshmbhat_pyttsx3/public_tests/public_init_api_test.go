package public_tests

import "testing"

type YetAnotherDummyEngine struct {
	name string
}

func (e *YetAnotherDummyEngine) Start() string  { return "hello" }
func (e *YetAnotherDummyEngine) Finish() string { return "goodbye" }

var activePublicAPIEngines = make(map[string]*YetAnotherDummyEngine)

func Pyttsx3InitPublicAPI(driverName string) *YetAnotherDummyEngine {
	if e, ok := activePublicAPIEngines[driverName]; ok {
		return e
	}
	e := &YetAnotherDummyEngine{name: driverName}
	activePublicAPIEngines[driverName] = e
	return e
}

func TestPublicEngineCreation(t *testing.T) {
	engine := Pyttsx3InitPublicAPI("publicengine")
	if engine.name != "publicengine" {
		t.Errorf("Expected engine.name='publicengine', got '%s'", engine.name)
	}
}

func TestPublicEngineSingleton(t *testing.T) {
	e1 := Pyttsx3InitPublicAPI("publicdummyA")
	e2 := Pyttsx3InitPublicAPI("publicdummyA")
	if e1 != e2 {
		t.Errorf("Expected singleton on engine, but got new instance")
	}
}

func TestPublicEngineDifferent(t *testing.T) {
	e1 := Pyttsx3InitPublicAPI("public1")
	e2 := Pyttsx3InitPublicAPI("public2")
	if e1 == e2 {
		t.Errorf("Different engine names should lead to distinct struct pointers")
	}
}