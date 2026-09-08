package original

import (
	"testing"
)

type Engine struct {
	sayFunc       func(string)
	runAndWaitFunc func()
	stopFunc      func()
}

func (e *Engine) Say(text string)                           { e.sayFunc(text) }
func (e *Engine) RunAndWait()                               { e.runAndWaitFunc() }
func (e *Engine) Stop()                                     { e.stopFunc() }

var engineInstanceCache = make(map[string]*Engine)

func Pyttsx3InitAPI(driverName string, debug bool) *Engine {
	key := driverName
	if e, ok := engineInstanceCache[key]; ok {
		return e
	}
	e := &Engine{
		sayFunc:       func(_ string) {},
		runAndWaitFunc: func() {},
		stopFunc:      func() {},
	}
	engineInstanceCache[key] = e
	return e
}

func TestInitReturnsEngine(t *testing.T) {
	engine := Pyttsx3InitAPI("dummy", false)
	// Just check that methods exist
	engine.Say("something")
	engine.RunAndWait()
	engine.Stop()
}

func TestInitReturnsCachedInstance(t *testing.T) {
	eng1 := Pyttsx3InitAPI("dummy", false)
	eng2 := Pyttsx3InitAPI("dummy", false)
	if eng1 != eng2 {
		t.Errorf("Expected same cached engine for same driverName")
	}
}

func TestInitWithDebugFlag(t *testing.T) {
	eng := Pyttsx3InitAPI("dummy", true)
	eng.Say("test")
}

func TestSpeakCallsInitAndEngineMethods(t *testing.T) {
	calls := make(map[string]interface{})
	type DummyEngine struct{}
	engine := &DummyEngine{}
	initCalled := false
	var lastSay string
	runCalled := false

	// Simulate init and speak helpers
	initFn := func(driverName string, debug bool) *DummyEngine {
		initCalled = true
		return engine
	}
	sayFn := func(text string) { lastSay = text }
	runFn := func()            { runCalled = true }
	engineImpl := &Engine{
		sayFunc:       sayFn,
		runAndWaitFunc: runFn,
		stopFunc:      func() {},
	}
	Pyttsx3InitAPI := func(driverName string, debug bool) *Engine {
		initCalled = true
		return engineImpl
	}
	// Simulate "pyttsx3.speak" logic
	Pyttsx3Speak := func(text string) {
		engine := Pyttsx3InitAPI("dummy", false)
		engine.Say(text)
		engine.RunAndWait()
	}
	Pyttsx3Speak("text")
	if !initCalled || lastSay != "text" || !runCalled {
		t.Errorf("Expected speak to call init, say, and run, got %v %v %v", initCalled, lastSay, runCalled)
	}
}