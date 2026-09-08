package original

import (
	"os"
	"testing"
	"github.com/packt-oop3/goport/internal/chapter11"
)

func TestDocumentSavePythonic(t *testing.T) {
	filename := "doc.txt"
	defer os.Remove(filename)
	doc := chapter11.NewPythonicDocument(filename)
	doc.Save()
	content, err := os.ReadFile(filename)
	if err != nil {
		t.Fatalf("Reading saved file failed: %v", err)
	}
	if string(content) != "This file cannot be modified" {
		t.Errorf("Expected file content to be unchanged")
	}
}

func TestSaveCommandCallsDocumentSave(t *testing.T) {
	filename := "doc.txt"
	defer os.Remove(filename)
	doc := chapter11.NewPythonicDocument(filename)
	called := false
	origSave := doc.Save
	doc.Save = func() {
		called = true
		origSave()
	}
	cmd := chapter11.NewPythonicSaveCommand(doc)
	cmd()
	if !called {
		t.Errorf("Save command didn't call document.Save()")
	}
}

type pythonicDummyCommand struct{ called bool }
func (d *pythonicDummyCommand) Call() { d.called = true }

func TestKeyboardShortcutCallsCommand(t *testing.T) {
	cmd := &pythonicDummyCommand{called: false}
	ks := chapter11.NewPythonicKeyboardShortcut()
	ks.Command = cmd
	ks.Keypress()
	if !cmd.called {
		t.Error("KeyboardShortcut didn't call command")
	}
}

func TestMenuItemClickCallsCommand(t *testing.T) {
	dummy := &pythonicDummyCommand{called: false}
	item := chapter11.NewPythonicMenuItem()
	item.Command = dummy
	item.Click()
	if !dummy.called {
		t.Error("MenuItem did not call command")
	}
}

// Golang doesn't use monkeypatch, so mimic with recover.
type pythonicDummyWindow struct{}

func (w *pythonicDummyWindow) Exit() { panic(0) }

func TestWindowExitExits(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("SystemExit (panic) not triggered in TestWindowExitExits")
		} else if code, ok := r.(int); !ok || code != 0 {
			t.Errorf("Expected code 0, got %v", r)
		}
	}()
	w := &pythonicDummyWindow{}
	w.Exit()
}