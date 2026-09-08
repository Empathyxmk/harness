package original

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx"
	"os"
	"testing"
)

// Test Execute() throws error when Executable is nil
func TestJavaFXRunMojo_ExecuteThrowsWhenExecutableNil(t *testing.T) {
	mojo := &openjfx.JavaFXRunMojo{}
	mojo.SetMainClass("com.example.Main")
	tmpdir := os.TempDir()
	mojo.SetBasedir(tmpdir)
	mojo.SetBuilddir(tmpdir)
	mojo.SetExecutable(nil)
	if err := mojo.Execute(); err == nil {
		t.Errorf("Expected error (MojoExecutionException) when Executable is nil, got nil")
	}
}

// Test skip execution does not return error
func TestJavaFXRunMojo_SkipExecution(t *testing.T) {
	mojo := &openjfx.JavaFXRunMojo{}
	mojo.Skip = true
	mojo.SetExecutable(nil) // Doesn't matter when skip is true
	if err := mojo.Execute(); err != nil {
		t.Errorf("Should not return error when skip is true, got: %v", err)
	}
}