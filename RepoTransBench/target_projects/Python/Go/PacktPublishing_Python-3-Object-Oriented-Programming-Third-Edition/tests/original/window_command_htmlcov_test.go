package original

import (
	"os"
	"testing"
	"bytes"
	"github.com/packt-oop3/goport/internal/chapter11"
)

func TestDocumentSaveHTMLCov(t *testing.T) {
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

func TestSaveCommandExecutesDocumentSaveHTMLCov(t *testing.T) {
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

type dummyHTMLCovCommand struct{ x bool }
func (d *dummyHTMLCovCommand) Execute() { d.x = true }

func TestToolbarButtonClickCallsCommandHTMLCov(t *testing.T) {
	button := chapter11.NewToolbarButton("n", "icon")
	dummy := &dummyHTMLCovCommand{x: false}
	button.Command = dummy
	dummy.x = false
	button.Click()
	if !dummy.x {
		t.Error("Dummy command x was not set true via Click")
	}
}

type dummyHTMLCovCommand2 struct{ called bool }
func (d *dummyHTMLCovCommand2) Execute() { d.called = true }

func TestKeyboardShortcutKeypressExecutesCommandHTMLCov(t *testing.T) {
	ks := chapter11.NewKeyboardShortcut("k", "ctrl")
	dummy := &dummyHTMLCovCommand2{called: false}
	ks.Command = dummy
	dummy.called = false
	ks.Keypress()
	if !dummy.called {
		t.Error("Command was not called")
	}
}

type dummyHTMLCovCommand3 struct{ did bool }
func (d *dummyHTMLCovCommand3) Execute() { d.did = true }

func TestMenuItemClickCallsCommandHTMLCov(t *testing.T) {
	m := chapter11.NewMenuItem("F", "X")
	dummy := &dummyHTMLCovCommand3{did: false}
	m.Command = dummy
	dummy.did = false
	m.Click()
	if !dummy.did {
		t.Error("Did not set dummy.did true")
	}
}

type dummyHTMLCovWindow struct{}
type dummyHTMLCovExitCommand struct{ w *dummyHTMLCovWindow }
func (c *dummyHTMLCovExitCommand) Execute() { panic(0) }

func TestExitCommandExitsHTMLCov(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("SystemExit was not raised")
		} else if code, ok := r.(int); !ok || code != 0 {
			t.Errorf("Expected exit code 0, got %v", r)
		}
	}()
	cmd := &dummyHTMLCovExitCommand{w: &dummyHTMLCovWindow{}}
	cmd.Execute()
}