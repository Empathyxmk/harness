package public_tests

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx"
	"os"
	"testing"
)

func TestJavaFXRunMojoPublicTest_ExecuteThrowsWhenExecutableNil(t *testing.T) {
	mojo := &openjfx.JavaFXRunMojo{}
	mojo.SetMainClass("org.publicexample.Launcher")
	tmpdir := os.TempDir() + "/publictestsubdir_run"
	_ = os.MkdirAll(tmpdir, 0755)
	mojo.SetBasedir(tmpdir)
	mojo.SetBuilddir(tmpdir)
	mojo.SetExecutable(nil)
	if err := mojo.Execute(); err == nil {
		t.Errorf("Expected error (MojoExecutionException) when Executable is nil, got nil")
	}
}

func TestJavaFXRunMojoPublicTest_SkipExecution(t *testing.T) {
	mojo := &openjfx.JavaFXRunMojo{}
	mojo.Skip = true
	mojo.SetExecutable(nil) // Doesn't matter when skip is true
	if err := mojo.Execute(); err != nil {
		t.Errorf("Should not return error when skip is true, got: %v", err)
	}
}