package original

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx"
	"os"
	"path/filepath"
	"testing"
)

// Test that Execute() always returns MojoExecutionException as in Java.
func TestJavaFXJLinkMojo_ExecuteWithException(t *testing.T) {
	mojo := &openjfx.JavaFXJLinkMojo{}
	mojo.SetMainClass("com.example.Main")
	tmpdir := os.TempDir()
	mojo.SetBasedir(tmpdir)
	mojo.SetBuilddir(tmpdir)
	if err := mojo.Execute(); err == nil {
		t.Errorf("Expected error (MojoExecutionException), got nil")
	}
}