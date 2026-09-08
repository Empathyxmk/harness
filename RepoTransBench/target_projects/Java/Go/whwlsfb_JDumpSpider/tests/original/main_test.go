package original

import (
	"errors"
	"os"
	"strings"
	"testing"
)

// ---- Dummies to stub behaviors as in Java tests ----
type DummyHeapHolder struct{}

func (d *DummyHeapHolder) FindClass(var1 string) interface{}                        { return "dummyClass" }
func (d *DummyHeapHolder) GetClasses() []interface{}                                 { return []interface{}{} }
func (d *DummyHeapHolder) IsInstanceOf(javaClass interface{}, className string) bool { return false }
func (d *DummyHeapHolder) IsArray(javaClass interface{}) bool                        { return false }
func (d *DummyHeapHolder) GetSubClasses(javaClass interface{}) []interface{}         { return []interface{}{} }
func (d *DummyHeapHolder) GetInstances(javaClass interface{}) []interface{}          { return []interface{}{} }
func (d *DummyHeapHolder) GetFields(javaClass interface{}) []interface{}             { return []interface{}{} }
func (d *DummyHeapHolder) GetClassName(javaClass interface{}) string                 { return "dummyClass" }
func (d *DummyHeapHolder) GetSuperClass(javaClass interface{}) interface{}           { return nil }
func (d *DummyHeapHolder) GetFieldName(field interface{}) string                     { return "" }
func (d *DummyHeapHolder) GetFieldClass(field interface{}) interface{}               { return "" }
func (d *DummyHeapHolder) FindThing(objectId int64) interface{}                      { return nil }
func (d *DummyHeapHolder) GetValueOfField(instance interface{}, fieldName string) interface{} {
	return nil
}
func (d *DummyHeapHolder) GetFieldsByNameList(instance interface{}, fieldList map[string]string) map[string]string {
	return map[string]string{
		"username": "u",
		"password": "p",
		"jdbcUrl":  "j",
	}
}
func (d *DummyHeapHolder) ArrayDump(instance interface{}) map[string]string {
	return map[string]string{}
}
func (d *DummyHeapHolder) GetArrayItems(instance interface{}) []interface{} { return []interface{}{} }
func (d *DummyHeapHolder) GetFieldStringValue(instance interface{}, fieldName string) string {
	return ""
}
func (d *DummyHeapHolder) GetFieldValue(instance interface{}, fieldName string) interface{} { return nil }
func (d *DummyHeapHolder) IsMap(instance interface{}) bool                                 { return false }
func (d *DummyHeapHolder) GetMap(instance interface{}) interface{}                         { return map[string]string{} }
func (d *DummyHeapHolder) ToString(instance interface{}) string                            { return "" }
func (d *DummyHeapHolder) ToByteArray(_instance interface{}) []byte                        { return []byte{} }

type DummySpider struct{}

func (d *DummySpider) GetName() string                                    { return "dummy" }
func (d *DummySpider) Sniff(heapHolder *DummyHeapHolder) string           { return "sniffed" }

// ---- Implementation stubs for Main ----
type MainStruct struct {
	Flag     []string
	Heapfile string
}

func (m *MainStruct) GetArgValue(arg string) (string, error) {
	for i, v := range m.Flag {
		if v == arg {
			if i+1 >= len(m.Flag) {
				return "", errors.New("Get '" + arg + "' value failed")
			}
			return m.Flag[i+1], nil
		}
	}
	return "", errors.New("not found")
}

// Simulate Main.run and Main.runAsync logic based on test expectation
type MainMock struct {
	heapfile string
	flag     []string
}

func Main_run(args []string) string {
	if len(args) == 0 {
		return "please give a heap filepath"
	}
	if len(args) > 0 && !fileExists(args[0]) {
		return "file not exist"
	}
	if len(args) > 0 && args[0] == "-help" {
		return "usage"
	}
	return "ok"
}

func Main_runAsync(args []string) string {
	if len(args) < 2 {
		return "must give a result file path"
	}
	return "async ok"
}

func (m *MainMock) GetArgValue(flag string) (string, error) {
	for i, v := range m.flag {
		if v == flag {
			if i+1 >= len(m.flag) {
				return "", errors.New("Get '" + flag + "' value failed")
			}
			return m.flag[i+1], nil
		}
	}
	return "", errors.New("not found")
}

func (m *MainMock) GetFileVersion() string {
	// Simulate file not found error
	if !fileExists(m.heapfile) {
		panic("file not exist: " + m.heapfile)
	}
	return "1.0"
}

func fileExists(filename string) bool {
	_, err := os.Stat(filename)
	return err == nil
}

// ----------- TESTS ---------------

func TestRunWithNoArgsShowsMessage(t *testing.T) {
	out := Main_run([]string{})
	if !strings.Contains(out, "please give a heap filepath") {
		t.Errorf("Expected help message for no args, got: %v", out)
	}
}

func TestRunWithNonexistentFileShowsMessage(t *testing.T) {
	args := []string{"nonexistent_file.hprof"}
	out := Main_run(args)
	if !strings.Contains(out, "file not exist") {
		t.Errorf("Expected 'file not exist' message, got: %v", out)
	}
}

func TestRunAsyncRequiresResultPath(t *testing.T) {
	result := Main_runAsync([]string{"heap.hprof"})
	if !strings.Contains(result, "must give a result file path") {
		t.Errorf("Expected 'must give a result file path', got: %v", result)
	}
}

func TestGetArgValueThrowsOnError(t *testing.T) {
	m := MainMock{}
	m.flag = []string{"-out"}
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Did not expect panic, got: %v", r)
		}
	}()
	_, err := m.GetArgValue("-out")
	if err == nil || !strings.Contains(err.Error(), "Get '-out' value failed") {
		t.Errorf("Expected error 'Get -out value failed', got: %v", err)
	}
}

func TestGetFileVersionBadFile(t *testing.T) {
	m := MainMock{}
	m.heapfile = "nope.file.that.is.never.there"
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for file not exist")
		}
	}()
	_ = m.GetFileVersion()
}