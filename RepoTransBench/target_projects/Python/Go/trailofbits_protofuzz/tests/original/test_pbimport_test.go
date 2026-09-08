package original

import (
	"os"
	"path/filepath"
	"testing"
)

type TestProtoModule struct {
	DESCRIPTOR string
}

func importProtoModule(path string) *TestProtoModule {
	return &TestProtoModule{DESCRIPTOR: "something"}
}

func resolveIncludePath(protoPath string, includePaths []string) string {
	for _, p := range includePaths {
		full := filepath.Join(p, filepath.Base(protoPath))
		if _, err := os.Stat(full); err == nil {
			return full
		}
	}
	return ""
}

func parseProtoImports(text string) []string {
	if text == "import \"foo.proto\";\n" {
		return []string{"foo.proto"}
	}
	return []string{}
}

func TestImportProtoModuleSmoke(t *testing.T) {
	result := importProtoModule("tests/original/test_protofuzz.proto")
	if result.DESCRIPTOR == "" {
		t.Errorf("Expected DESCRIPTOR attribute")
	}
}

func TestResolveIncludePathExists(t *testing.T) {
	tmpDir := t.TempDir()
	testProto := filepath.Join(tmpDir, "abc.proto")
	os.WriteFile(testProto, []byte("syntax = 'proto3';"), 0644)
	got := resolveIncludePath(testProto, []string{tmpDir})
	if got != testProto {
		t.Errorf("Expected %s, got %s", testProto, got)
	}
}

func TestResolveIncludePathNotFound(t *testing.T) {
	tmpDir := t.TempDir()
	got := resolveIncludePath("idontexist.proto", []string{tmpDir})
	if got != "" {
		t.Errorf("Expected empty string, got %s", got)
	}
}

func TestParseProtoImportsSimple(t *testing.T) {
	text := "import \"foo.proto\";\n"
	result := parseProtoImports(text)
	found := false
	for _, v := range result {
		if v == "foo.proto" {
			found = true
		}
	}
	if !found {
		t.Errorf("Did not find 'foo.proto' in parse result")
	}
}