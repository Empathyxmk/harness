package original

import (
	"testing"
	"github.com/packt-oop3/goport/internal/chapter11"
)

func setupModule() {
	chapter11.RootFolder.Children = make(map[string]*chapter11.Folder)
}

func TestFolderAndFileBasicStructure(t *testing.T) {
	setupModule()
	f := chapter11.NewFolder("documents")
	chapter11.RootFolder.AddChild(f)
	fileTxt := chapter11.NewFile("notes.txt", "abc")
	f.AddChildFile(fileTxt)
	if f.Children["notes.txt"] != fileTxt {
		t.Error("File not added to folder children correctly")
	}
	if fileTxt.Parent != f {
		t.Error("Parent not set correctly on file")
	}
}

func TestMoveAndDeleteBehavior(t *testing.T) {
	setupModule()
	f1 := chapter11.NewFolder("docs1")
	f2 := chapter11.NewFolder("docs2")
	chapter11.RootFolder.AddChild(f1)
	chapter11.RootFolder.AddChild(f2)
	myfile := chapter11.NewFile("my.txt", "content")
	f1.AddChildFile(myfile)
	myfile.Move("/docs2")
	if myfile.Parent != f2 {
		t.Error("File parent not moved correctly")
	}
	if _, ok := f2.Children["my.txt"]; !ok {
		t.Error("Moved file not found in new folder children")
	}
	myfile.Delete()
	if _, ok := f2.Children["my.txt"]; ok {
		t.Error("File was not deleted from folder")
	}
}

func TestGetPathReturnsCorrectNode(t *testing.T) {
	setupModule()
	f := chapter11.NewFolder("foo")
	chapter11.RootFolder.AddChild(f)
	node := chapter11.GetPath("/foo")
	if node != f {
		t.Error("GetPath did not return correct folder")
	}
	sub := chapter11.NewFolder("bar")
	f.AddChild(sub)
	path := chapter11.GetPath("/foo/bar")
	if path != sub {
		t.Error("GetPath did not return subfolder")
	}
}

func TestFileAndFolderInit(t *testing.T) {
	file1 := chapter11.NewFile("dafile.txt", "cc")
	if file1.Name != "dafile.txt" {
		t.Error("File name incorrect at init")
	}
	if file1.Contents != "cc" {
		t.Error("File contents incorrect at init")
	}
	folder := chapter11.NewFolder("bktest")
	if folder.Name != "bktest" {
		t.Error("Folder name incorrect at init")
	}
}

func TestFolderAddChildSetsParent(t *testing.T) {
	p := chapter11.NewFolder("parentf")
	c := chapter11.NewFolder("childf")
	p.AddChild(c)
	if c.Parent != p {
		t.Error("Parent not set when adding child")
	}
	if _, ok := p.Children["childf"]; !ok {
		t.Error("Child not in parent's children map")
	}
}