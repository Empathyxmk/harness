package original

import (
	"bufio"
	"os"
	"strings"
	"testing"
)

// Emulate Mapping logic matching the Java test's expectations.
type Mapping struct {
	mapping map[string]string
}

func NewMappingWithFile(path string) *Mapping {
	m := &Mapping{mapping: make(map[string]string)}
	if path == "" {
		return m
	}
	file, err := os.Open(path)
	if err != nil {
		return m
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		arrowIdx := strings.Index(line, "->")
		colonIdx := strings.Index(line, ":")
		if arrowIdx == -1 || colonIdx == -1 || colonIdx < arrowIdx {
			continue
		}
		// Extract mappings as in Java logic
		key := strings.TrimSpace(line[:arrowIdx])
		val := strings.TrimSpace(line[arrowIdx+2 : colonIdx])
		if key != "" && val != "" {
			m.mapping[key] = val
		}
	}
	return m
}

func (m *Mapping) Get(clazz string) string {
	return m.mapping[clazz]
}
func (m *Mapping) GetMapping() map[string]string {
	return m.mapping
}

func TestValidMappings(t *testing.T) {
	tmpFile, err := os.CreateTemp("", "mapping*.txt")
	if err != nil {
		t.Fatalf("failed to create mapping file: %v", err)
	}
	tmpName := tmpFile.Name()
	data := `# This is a comment
com.abc.ClassA -> com.obf.X:
  # Indented comment
com.abc.ClassB -> com.obf.Y:
bad mapping line
com.abc.ClassC -> com.obf.Z:
`
	if _, err := tmpFile.WriteString(data); err != nil {
		t.Fatalf("failed to write temp mapping file: %v", err)
	}
	tmpFile.Close()
	defer os.Remove(tmpName)
	mapping := NewMappingWithFile(tmpName)
	if mapping.Get("com.abc.ClassA") != "com.obf.X" {
		t.Errorf("expected 'com.obf.X', got %q", mapping.Get("com.abc.ClassA"))
	}
	if mapping.Get("com.abc.ClassB") != "com.obf.Y" {
		t.Errorf("expected 'com.obf.Y', got %q", mapping.Get("com.abc.ClassB"))
	}
	if mapping.Get("com.abc.ClassC") != "com.obf.Z" {
		t.Errorf("expected 'com.obf.Z', got %q", mapping.Get("com.abc.ClassC"))
	}
	if mapping.Get("com.abc.NotExist") != "" {
		t.Error("Get for not existing key should be empty string")
	}
	if len(mapping.GetMapping()) < 3 {
		t.Errorf("expected >= 3 mappings, got %d", len(mapping.GetMapping()))
	}
}

func TestNullFile(t *testing.T) {
	m := NewMappingWithFile("")
	if m.GetMapping() == nil {
		t.Error("mapping map should not be nil when file is null")
	}
	if len(m.GetMapping()) != 0 {
		t.Errorf("mapping map should be empty when file is null, got len %d", len(m.GetMapping()))
	}
}

func TestNonExistentFile(t *testing.T) {
	m := NewMappingWithFile("doesnot_exist_mapping_go.txt")
	if m.GetMapping() == nil {
		t.Error("mapping map should not be nil when file doesn't exist")
	}
	if len(m.GetMapping()) != 0 {
		t.Errorf("mapping map should be empty when file doesn't exist, got len %d", len(m.GetMapping()))
	}
}

func TestMalformedLines(t *testing.T) {
	file, err := os.CreateTemp("", "malformed*.txt")
	if err != nil {
		t.Fatalf("failed to create malformed mapping file: %v", err)
	}
	tmpName := file.Name()
	defer os.Remove(tmpName)
	data := `
malformed_line
com.onlyonepart -> 
 -> onlysecondpart:
correct.package -> correct.target:
`
	if _, err := file.WriteString(data); err != nil {
		t.Fatalf("failed writing to malformed mapping file: %v", err)
	}
	file.Close()
	m := NewMappingWithFile(tmpName)
	if got := m.Get("correct.package"); got != "correct.target" {
		t.Errorf("expected 'correct.target', got %q", got)
	}
}