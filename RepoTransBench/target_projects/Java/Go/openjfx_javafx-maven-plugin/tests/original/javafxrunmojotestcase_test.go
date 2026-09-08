package original

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx"
	"strings"
	"testing"
)

func TestJavaFXRunMojoTestCase_SplitComplexArgumentString(t *testing.T) {
	mojo := &openjfx.JavaFXRunMojo{}
	option := "param1 " +
		"param2   \n   " +
		"param3\n" +
		"param4=\"/path/to/my file.log\"   " +
		"'var\"foo   var\"foo' " +
		"'var\"foo'   " +
		"'var\"foo' " +
		"\"foo'var foo'var\" " +
		"\"foo'var\" " +
		"\"foo'var\""

	expected := []string{
		"param1",
		"param2",
		"param3",
		"param4=\"/path/to/my file.log\"",
		"'var\"foo   var\"foo'",
		"'var\"foo'",
		"'var\"foo'",
		"\"foo'var foo'var\"",
		"\"foo'var\"",
		"\"foo'var\"",
	}

	got := mojo.SplitComplexArgumentStringAdapter(option)
	if len(got) != len(expected) {
		t.Errorf("Expected %d args, got %d (%v)", len(expected), len(got), got)
	}
	for i := range expected {
		if got[i] != expected[i] {
			t.Errorf("Expected argument %d to be %q, got %q", i, expected[i], got[i])
		}
	}
}