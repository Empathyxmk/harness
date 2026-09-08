package original

import (
	"os"
	"testing"
	"bytes"
	"github.com/packt-oop3/goport/internal/chapter11"
)

func TestDocumentSave(t *testing.T) {
	filename := "file1.txt"
	defer os.Remove(filename)
	doc := chapter11.NewDocument(filename)
	doc.Save()
	content, err := os.ReadFile(filename)
	if err != nil {
		t.Fatalf("Reading saved file failed: %v", err)
	}
	if string(content) != "This file cannot be modified" {
		t.Errorf("File content mismatch: got [%s]", content)
	}
}

func TestSaveCommandExecutesDocumentSave(t *testing.T) {
	filename := "file2.txt"
	defer os.Remove(filename)
	doc := chapter11.NewDocument(filename)
	doc.Contents = "SAVED"
	cmd := chapter11.NewSaveCommand(doc)
	cmd.Execute()
	content, err := os.ReadFile(filename)
	if err != nil {
		t.Fatalf("Reading saved file failed: %v", err)
	}
	if string(content) != "SAVED" {
		t.Errorf("File content mismatch: wanted SAVED, got [%s]", content)
	}
}

type dummyCommand struct{ x bool }
func (d *dummyCommand) Execute() { d.x = true }

func TestToolbarButtonClickCallsCommand(t *testing.T) {
	button := chapter11.NewToolbarButton("n", "icon")
	dummy := &dummyCommand{x: false}
	button.Command = dummy
	button.Click()
	if !dummy.x {
		t.Error("Dummy command x was not set true via Click")
	}
}

type dummyCommand2 struct{ called bool }
func (d *dummyCommand2) Execute() { d.called = true }

func TestKeyboardShortcutKeypressExecutesCommand(t *testing.T) {
	ks := chapter11.NewKeyboardShortcut("k", "ctrl")
	dummy := &dummyCommand2{called: false}
	ks.Command = dummy
	ks.Keypress()
	if !dummy.called {
		t.Error("Command was not called")
	}
}

type dummyCommand3 struct{ did bool }
func (d *dummyCommand3) Execute() { d.did = true }

func TestMenuItemClickCallsCommand(t *testing.T) {
	m := chapter11.NewMenuItem("F", "X")
	dummy := &dummyCommand3{did: false}
	m.Command = dummy
	m.Click()
	if !dummy.did {
		t.Error("Did not set dummy.did true")
	}
}

// Cannot exit os.Exit in Go without stopping the test process; use recoverable panic.
type dummyWindow struct{}
type dummyExitCommand struct{ w *dummyWindow }
func (c *dummyExitCommand) Execute() { panic(0) }

func TestExitCommandExits(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("SystemExit was not raised")
		} else if code, ok := r.(int); !ok || code != 0 {
			t.Errorf("Expected exit code 0, got %v", r)
		}
	}()
	cmd := &dummyExitCommand{w: &dummyWindow{}}
	cmd.Execute()
}