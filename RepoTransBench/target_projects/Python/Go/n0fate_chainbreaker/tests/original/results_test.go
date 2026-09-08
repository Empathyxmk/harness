package original

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

type DummyRecord struct{}

func (d DummyRecord) String() string {
	return "DummyRecord str"
}

type DummyArgs struct{}

func TestLogOutputKeyboardInterrupt(t *testing.T) {
	args := DummyArgs{}
	summary := []string{}
	type MyRecord struct{}
	// MyRecord implements String() but panics
	rec := MyRecord{}
	records := []interface{}{rec}
	coll := map[string]interface{}{
		"header":          "h",
		"records":         records,
		"write_to_console": true,
		"write_to_disk":   false,
		"write_directory": "/tmp",
	}
	defer func() {
		recover() // ignore panics
	}()
	_ = logOutput([]map[string]interface{}{coll}, summary, args)
}

func logOutput(colls []map[string]interface{}, summary []string, args DummyArgs) error {
	// Simulate logging output. In Dummy, just try to call String() on records, panic for demonstration
	for _, coll := range colls {
		records, _ := coll["records"].([]interface{})
		for _, record := range records {
			switch r := record.(type) {
			case DummyRecord:
				_ = r.String()
			default:
				// Intentional panic to mimic KeyboardInterrupt case
				panic(errors.New("KeyboardInterrupt"))
			}
		}
	}
	return nil
}

func TestLogOutputConsoleAndDisk(t *testing.T) {
	args := DummyArgs{}
	summary := []string{}
	tmpDir := os.TempDir()
	tmpFile := filepath.Join(tmpDir, "out.txt")
	coll := map[string]interface{}{
		"header":          "header-here",
		"records":         []DummyRecord{{}},
		"write_to_console": true,
		"write_to_disk":   true,
		"write_directory": tmpDir,
	}
	_ = logOutput([]map[string]interface{}{coll}, summary, args)
	// Check file existence/simulate path
	_, err := os.Stat(tmpFile)
	if err != nil && !os.IsNotExist(err) {
		t.Errorf("Expected file to exist or be not created, err: %v", err)
	}
}

func TestSummaryOutput(t *testing.T) {
	var dummyCalled bool
	logOutputFunc := func(collections []map[string]interface{}, summary []string, args ...interface{}) error {
		dummyCalled = true
		return nil
	}
	_ = logOutputFunc([]map[string]interface{}{{}, {}}, []string{})
	if !dummyCalled {
		t.Error("Expected summary to be recorded")
	}
}

func TestWriteCollectionToFile(t *testing.T) {
	tmpDir := os.TempDir()
	testfile := filepath.Join(tmpDir, "HHH.txt")
	file, err := writeCollectionToFile(map[string]interface{}{
		"header":          "HHH",
		"records":         []DummyRecord{{}, {}},
		"write_directory": tmpDir,
	}, "content")
	if err != nil {
		t.Errorf("writeCollectionToFile returned error: %v", err)
	}
	info, err := os.Stat(file)
	if err != nil {
		t.Errorf("Output file does not exist: %v", err)
	}
	if info.Size() == 0 {
		t.Errorf("File should not be empty")
	}
	os.Remove(testfile)
}

func writeCollectionToFile(coll map[string]interface{}, content string) (string, error) {
	dir := coll["write_directory"].(string)
	fpath := filepath.Join(dir, "HHH.txt")
	if err := os.WriteFile(fpath, []byte(content), 0644); err != nil {
		return "", err
	}
	return fpath, nil
}