package original

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx"
	"openjfx_javafx_maven_plugin/src/org/openjfx/model"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestJavaFXBaseMojo_ParentTest(t *testing.T) {
	tmpdir := os.TempDir()
	testPath := filepath.Join(tmpdir, "test", "test")
	_ = os.MkdirAll(testPath, 0755)
	mojo := &openjfx.JavaFXBaseMojo{}
	parent := mojo.GetParent(testPath, 2)
	if parent == nil || *parent != tmpdir {
		t.Errorf("Expected parent dir: %v, got: %v", tmpdir, parent)
	}
}

func TestJavaFXBaseMojo_MainClassStringWithModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	moduleDesc := openjfx.NewJavaModuleDescriptor("hellofx")
	got := mojo.CreateMainClassString("org.openjfx.Main", moduleDesc, nil)
	expected := "hellofx/org.openjfx.Main"
	if got != expected {
		t.Errorf("Expected: %s, got: %s", expected, got)
	}
}

func TestJavaFXBaseMojo_MainClassStringWithoutModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	got := mojo.CreateMainClassString("org.openjfx.Main", nil, nil)
	if got != "org.openjfx.Main" {
		t.Errorf("Expected org.openjfx.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("hellofx/org.openjfx.Main", nil, nil)
	if got != "hellofx/org.openjfx.Main" {
		t.Errorf("Expected hellofx/org.openjfx.Main, got %s", got)
	}
}

func TestJavaFXBaseMojo_MainClassStringWithClasspathWithModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	moduleDesc := openjfx.NewJavaModuleDescriptor("hellofx")
	opt := model.CLASSPATH.String()
	optPtr := &opt
	got := mojo.CreateMainClassString("org.openjfx.Main", moduleDesc, optPtr)
	if got != "org.openjfx.Main" {
		t.Errorf("Expected org.openjfx.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("hellofx/org.openjfx.Main", moduleDesc, optPtr)
	if got != "org.openjfx.Main" {
		t.Errorf("Expected org.openjfx.Main, got %s", got)
	}
}

func TestJavaFXBaseMojo_MainClassStringWithClasspathWithoutModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	opt := model.CLASSPATH.String()
	optPtr := &opt
	got := mojo.CreateMainClassString("org.openjfx.Main", nil, optPtr)
	if got != "org.openjfx.Main" {
		t.Errorf("Expected org.openjfx.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("hellofx/org.openjfx.Main", nil, optPtr)
	if got != "org.openjfx.Main" {
		t.Errorf("Expected org.openjfx.Main, got %s", got)
	}
}

func TestJavaFXBaseMojo_MainClassStringWithModulepathWithModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	moduleDesc := openjfx.NewJavaModuleDescriptor("hellofx")
	opt := model.MODULEPATH.String()
	optPtr := &opt
	got := mojo.CreateMainClassString("org.openjfx.Main", moduleDesc, optPtr)
	if got != "hellofx/org.openjfx.Main" {
		t.Errorf("Expected hellofx/org.openjfx.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("hellofx/org.openjfx.Main", moduleDesc, optPtr)
	if got != "hellofx/org.openjfx.Main" {
		t.Errorf("Expected hellofx/org.openjfx.Main, got %s", got)
	}
}

func TestJavaFXBaseMojo_MainClassStringWithModulepathWithoutModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	opt := model.MODULEPATH.String()
	optPtr := &opt
	got := mojo.CreateMainClassString("org.openjfx.Main", nil, optPtr)
	if got != "org.openjfx.Main" {
		t.Errorf("Expected org.openjfx.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("hellofx/org.openjfx.Main", nil, optPtr)
	if got != "hellofx/org.openjfx.Main" {
		t.Errorf("Expected hellofx/org.openjfx.Main, got %s", got)
	}
}

func TestJavaFXBaseMojo_InvalidParentTest(t *testing.T) {
	tmpdir := os.TempDir()
	testPath := filepath.Join(tmpdir, "test", "test")
	_ = os.MkdirAll(testPath, 0755)
	mojo := &openjfx.JavaFXBaseMojo{}
	parent := mojo.GetParent(testPath, 10)
	if parent != nil {
		t.Errorf("Expected nil (overshot traversal), got: %v", parent)
	}
}

func TestJavaFXBaseMojo_InvalidPathTest(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	parent := mojo.GetParent("/some-invalid-path", 0)
	if parent != nil {
		t.Errorf("Expected nil for invalid path, got: %v", parent)
	}
}

func TestJavaFXBaseMojo_InvalidPathWithDepthTest(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	parent := mojo.GetParent("/some-invalid-path", 2)
	if parent != nil {
		t.Errorf("Expected nil for invalid path with depth, got: %v", parent)
	}
}