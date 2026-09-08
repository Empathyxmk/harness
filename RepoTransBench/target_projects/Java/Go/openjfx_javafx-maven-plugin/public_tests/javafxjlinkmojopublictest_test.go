package public_tests

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx"
	"os"
	"testing"
)

func TestJavaFXJLinkMojoPublicTest_ExecuteWithException(t *testing.T) {
	mojo := &openjfx.JavaFXJLinkMojo{}
	mojo.SetMainClass("org.publicexample.Launcher")
	tmpdir := os.TempDir() + "/publictestsubdir"
	_ = os.MkdirAll(tmpdir, 0755)
	mojo.SetBasedir(tmpdir)
	mojo.SetBuilddir(tmpdir)
	if err := mojo.Execute(); err == nil {
		t.Errorf("Expected error (MojoExecutionException), got nil")
	}
}