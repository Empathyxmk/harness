package original

import (
	"testing"
	"twigmodule/tests"
)

type DummyFileLoader struct {
	*tests.MultiFileLoader
}
func NewDummyFileLoader() *DummyFileLoader {
	return &DummyFileLoader{tests.NewMultiFileLoader("twigdataobject")}
}

// Simulate creating a memory file object as in Java
func createMemoryFileObject() *tests.FileObject {
	return tests.NewFileObject("test", "twig")
}

func TestTwigDataObjectConstruction(t *testing.T) {
	fo := createMemoryFileObject()
	loader := NewDummyFileLoader()
	obj := tests.NewTwigDataObjectFo(fo, loader.MultiFileLoader)
	if obj == nil {
		t.Fatal("TwigDataObject should not be nil")
	}
	if obj.GetLookup() == nil {
		t.Errorf("GetLookup should not return nil")
	}
}

func TestCreateNodeDelegateReturnsDataNode(t *testing.T) {
	fo := createMemoryFileObject()
	loader := NewDummyFileLoader()
	obj := tests.NewTwigDataObjectFo(fo, loader.MultiFileLoader)
	node := obj.CreateNodeDelegate()
	if node == nil {
		t.Fatal("Node should not be nil")
	}
	if node.Name != "DataNode" {
		t.Errorf("Expected node name 'DataNode', got '%s'", node.Name)
	}
}