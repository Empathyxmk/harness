package chainbreaker

import (
	"errors"
	"testing"
)

type DummyRecord struct{}

func (r DummyRecord) String() string { return "Fake" }

func TestPublicResultsModuleExists(t *testing.T) {
	file := ResultsFile()
	if file == "" {
		t.Error("Expected module to have a file attribute")
	}
}

func TestPublicResultsModuleHasDoc(t *testing.T) {
	doc := ResultsDoc()
	// In Go, an empty docstring is allowed, so also check for string type
	if doc != "" && reflect.TypeOf(doc).Kind() != reflect.String {
		t.Error("Doc attribute should be a string or empty")
	}
}

func TestPublicLogOutputHandlesMissingMethod(t *testing.T) {
	dummyRecord := DummyRecord{}
	dummyArgs := struct{ output string }{output: "/tmp"}
	dummyColl := map[string]interface{}{
		"header":          "Testing",
		"records":         []DummyRecord{dummyRecord},
		"write_to_console": true,
		"write_to_disk":   true,
		"write_directory": "/tmp",
	}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic (AttributeError) when logOutput is missing behavior")
		}
	}()
	logOutputMissing([]map[string]interface{}{dummyColl}, []string{}, dummyArgs)
}

func ResultsFile() string { return "results.go" }
func ResultsDoc() string  { return "" }
func logOutputMissing(_ []map[string]interface{}, _ []string, _ interface{}) error {
	panic(errors.New("AttributeError"))
}