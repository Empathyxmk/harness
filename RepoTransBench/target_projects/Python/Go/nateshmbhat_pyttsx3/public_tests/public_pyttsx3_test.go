package public_tests

import (
	"testing"
)

type AnotherDummyEngine struct {
	driverName string
}

func (d *AnotherDummyEngine) Say(text string) string {
	// Reverse string
	runes := []rune(text)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}
func (d *AnotherDummyEngine) RunAndWait() string {
	return "executed"
}
func (d *AnotherDummyEngine) Stop() string {
	return "halted"
}

var activePublicEngines = make(map[string]*AnotherDummyEngine)

func Pyttsx3InitPublic(driverName string) *AnotherDummyEngine {
	if e, ok := activePublicEngines[driverName]; ok {
		return e
	}
	e := &AnotherDummyEngine{driverName: driverName}
	activePublicEngines[driverName] = e
	return e
}

func TestPublicInitAndEngine(t *testing.T) {
	engine := Pyttsx3InitPublic("diffdummy")
	if engine.driverName != "diffdummy" {
		t.Errorf("driverName should be 'diffdummy', got '%s'", engine.driverName)
	}
}

func TestPublicEngineCache(t *testing.T) {
	e1 := Pyttsx3InitPublic("cachetestA")
	e2 := Pyttsx3InitPublic("cachetestA")
	if e1 != e2 {
		t.Errorf("Should be same engine instance for same driverName")
	}
}

func TestPublicEngineUnique(t *testing.T) {
	e1 := Pyttsx3InitPublic("uniqueA")
	e2 := Pyttsx3InitPublic("uniqueB")
	if e1 == e2 {
		t.Errorf("Unique engines should be different for different names")
	}
}

func TestPublicEngineMethods(t *testing.T) {
	e1 := Pyttsx3InitPublic("diffdummy")
	if e1.Say("bar") != "rab" {
		t.Errorf("Say() reverse did not work")
	}
	if e1.RunAndWait() != "executed" {
		t.Errorf("runAndWait should be 'executed'")
	}
	if e1.Stop() != "halted" {
		t.Errorf("stop should be 'halted'")
	}
}