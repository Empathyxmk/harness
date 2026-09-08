package public_tests

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx"
	"openjfx_javafx_maven_plugin/src/org/openjfx/model"
	"os"
	"path/filepath"
	"testing"
)

func TestJavaFXBaseMojoPublicTest_ParentTest(t *testing.T) {
	tmpdir := os.TempDir()
	publicPath := filepath.Join(tmpdir, "publictest", "pubdir")
	_ = os.MkdirAll(publicPath, 0755)
	mojo := &openjfx.JavaFXBaseMojo{}
	parent := mojo.GetParent(publicPath, 2)
	if parent == nil || *parent != tmpdir {
		t.Errorf("Expected parent dir: %v, got: %v", tmpdir, parent)
	}
}

func TestJavaFXBaseMojoPublicTest_MainClassStringWithModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	moduleDesc := openjfx.NewJavaModuleDescriptor("publicmodule")
	got := mojo.CreateMainClassString("com.publicexample.Main", moduleDesc, nil)
	expected := "publicmodule/com.publicexample.Main"
	if got != expected {
		t.Errorf("Expected: %s, got: %s", expected, got)
	}
}

func TestJavaFXBaseMojoPublicTest_MainClassStringWithoutModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	got := mojo.CreateMainClassString("com.publicexample.Main", nil, nil)
	if got != "com.publicexample.Main" {
		t.Errorf("Expected com.publicexample.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("publicmodule/com.publicexample.Main", nil, nil)
	if got != "publicmodule/com.publicexample.Main" {
		t.Errorf("Expected publicmodule/com.publicexample.Main, got %s", got)
	}
}

func TestJavaFXBaseMojoPublicTest_MainClassStringWithClasspathWithModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	moduleDesc := openjfx.NewJavaModuleDescriptor("publicmodule")
	opt := model.CLASSPATH.String()
	optPtr := &opt
	got := mojo.CreateMainClassString("com.publicexample.Main", moduleDesc, optPtr)
	if got != "com.publicexample.Main" {
		t.Errorf("Expected com.publicexample.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("publicmodule/com.publicexample.Main", moduleDesc, optPtr)
	if got != "com.publicexample.Main" {
		t.Errorf("Expected com.publicexample.Main, got %s", got)
	}
}

func TestJavaFXBaseMojoPublicTest_MainClassStringWithClasspathWithoutModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	opt := model.CLASSPATH.String()
	optPtr := &opt
	got := mojo.CreateMainClassString("com.publicexample.Main", nil, optPtr)
	if got != "com.publicexample.Main" {
		t.Errorf("Expected com.publicexample.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("publicmodule/com.publicexample.Main", nil, optPtr)
	if got != "com.publicexample.Main" {
		t.Errorf("Expected com.publicexample.Main, got %s", got)
	}
}

func TestJavaFXBaseMojoPublicTest_MainClassStringWithModulepathWithModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	moduleDesc := openjfx.NewJavaModuleDescriptor("publicmodule")
	opt := model.MODULEPATH.String()
	optPtr := &opt
	got := mojo.CreateMainClassString("com.publicexample.Main", moduleDesc, optPtr)
	if got != "publicmodule/com.publicexample.Main" {
		t.Errorf("Expected publicmodule/com.publicexample.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("publicmodule/com.publicexample.Main", moduleDesc, optPtr)
	if got != "publicmodule/com.publicexample.Main" {
		t.Errorf("Expected publicmodule/com.publicexample.Main, got %s", got)
	}
}

func TestJavaFXBaseMojoPublicTest_MainClassStringWithModulepathWithoutModuleDescriptor(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	opt := model.MODULEPATH.String()
	optPtr := &opt
	got := mojo.CreateMainClassString("com.publicexample.Main", nil, optPtr)
	if got != "com.publicexample.Main" {
		t.Errorf("Expected com.publicexample.Main, got %s", got)
	}
	got = mojo.CreateMainClassString("publicmodule/com.publicexample.Main", nil, optPtr)
	if got != "publicmodule/com.publicexample.Main" {
		t.Errorf("Expected publicmodule/com.publicexample.Main, got %s", got)
	}
}

func TestJavaFXBaseMojoPublicTest_InvalidParentTest(t *testing.T) {
	tmpdir := os.TempDir()
	publicPath := filepath.Join(tmpdir, "publictest", "pubdir")
	_ = os.MkdirAll(publicPath, 0755)
	mojo := &openjfx.JavaFXBaseMojo{}
	parent := mojo.GetParent(publicPath, 10)
	if parent != nil {
		t.Errorf("Expected nil (overshot traversal), got: %v", parent)
	}
}

func TestJavaFXBaseMojoPublicTest_InvalidPathTest(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	parent := mojo.GetParent("/some-other-invalid-path", 0)
	if parent != nil {
		t.Errorf("Expected nil for invalid path, got: %v", parent)
	}
}

func TestJavaFXBaseMojoPublicTest_InvalidPathWithDepthTest(t *testing.T) {
	mojo := &openjfx.JavaFXBaseMojo{}
	parent := mojo.GetParent("/some-other-invalid-path", 2)
	if parent != nil {
		t.Errorf("Expected nil for invalid path with depth, got: %v", parent)
	}
}