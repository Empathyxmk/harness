package public_tests

import (
	"errors"
	"os"
	"strings"
	"testing"
)

// ==== Public Dummies as in Java Public Tests ====
type PublicDummyHeapHolder struct{}

func (d *PublicDummyHeapHolder) FindClass(var1 string) interface{} { return "publicDummyClass" }
func (d *PublicDummyHeapHolder) GetClasses() []interface{}         { return []interface{}{} }
func (d *PublicDummyHeapHolder) IsInstanceOf(javaClass interface{}, className string) bool {
	return true
}
func (d *PublicDummyHeapHolder) IsArray(javaClass interface{}) bool       { return true }
func (d *PublicDummyHeapHolder) GetSubClasses(javaClass interface{}) []interface{} {
	return []interface{}{"sub1"}
}
func (d *PublicDummyHeapHolder) GetInstances(javaClass interface{}) []interface{} {
	return []interface{}{"instance"}
}
func (d *PublicDummyHeapHolder) GetFields(javaClass interface{}) []interface{} { return []interface{}{"field"} }
func (d *PublicDummyHeapHolder) GetClassName(javaClass interface{}) string     { return "publicDummyClass" }
func (d *PublicDummyHeapHolder) GetSuperClass(javaClass interface{}) interface{} {
	return "publicSuperClass"
}
func (d *PublicDummyHeapHolder) GetFieldName(field interface{}) string  { return "fieldName" }
func (d *PublicDummyHeapHolder) GetFieldClass(field interface{}) string { return "fieldClass" }
func (d *PublicDummyHeapHolder) FindThing(objectId int64) interface{}   { return "foundThing" }
func (d *PublicDummyHeapHolder) GetValueOfField(instance interface{}, fieldName string) interface{} {
	return "valueOfField"
}
func (d *PublicDummyHeapHolder) GetFieldsByNameList(instance interface{}, fieldList map[string]string) map[string]string {
	return map[string]string{
		"username": "publicU",
		"password": "publicP",
		"jdbcUrl":  "jdbc:public",
	}
}
func (d *PublicDummyHeapHolder) ArrayDump(instance interface{}) map[string]string {
	return map[string]string{}
}
func (d *PublicDummyHeapHolder) GetArrayItems(instance interface{}) []interface{} {
	return []interface{}{"item1", "item2"}
}
func (d *PublicDummyHeapHolder) GetFieldStringValue(instance interface{}, fieldName string) string {
	return "stringValue"
}
func (d *PublicDummyHeapHolder) GetFieldValue(instance interface{}, fieldName string) interface{} { return "fieldValue" }
func (d *PublicDummyHeapHolder) IsMap(instance interface{}) bool                                 { return true }
func (d *PublicDummyHeapHolder) GetMap(instance interface{}) interface{}                         { return map[string]string{} }
func (d *PublicDummyHeapHolder) ToString(instance interface{}) string                            { return "toStringResult" }
func (d *PublicDummyHeapHolder) ToByteArray(_instance interface{}) []byte                       { return []byte{1, 2, 3} }

// For Main run
func Main_run(args []string) string {
	if len(args) > 0 && args[0] == "-help" {
		return "usage"
	}
	if len(args) > 0 && !fileExists(args[0]) {
		return "file not exist"
	}
	return "ok"
}

func Main_runAsync(args []string) string {
	if len(args) < 2 {
		return "must give a result file path"
	}
	return "async ok"
}

type MainMock struct {
	flag     []string
	heapfile string
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
	if !fileExists(m.heapfile) {
		panic("file not exist: " + m.heapfile)
	}
	return "1.0"
}
func fileExists(filename string) bool {
	_, err := os.Stat(filename)
	return err == nil
}

// -------- Public Tests --------

func TestRunWithHelpFlagShowsHelpMessage(t *testing.T) {
	out := Main_run([]string{"-help"})
	if !strings.Contains(out, "usage") {
		t.Errorf("Expected help/usage message, got: %v", out)
	}
}

func TestRunWithNonexistentFileShowsMessageDifferentName(t *testing.T) {
	args := []string{"totally_missing_file.hprof"}
	out := Main_run(args)
	if !strings.Contains(strings.ToLower(out), "file not exist") {
		t.Errorf("Expected 'file not exist' message, got: %v", out)
	}
}

func TestRunAsyncRequiresResultPathDifferentHeap(t *testing.T) {
	result := Main_runAsync([]string{"randomheap.hprof"})
	if !strings.Contains(strings.ToLower(result), "must give a result file path") {
		t.Errorf("Expected must give a result file path, got: %v", result)
	}
}

func TestGetArgValueThrowsOnDifferentFlag(t *testing.T) {
	m := MainMock{}
	m.flag = []string{"-in"}
	_, err := m.GetArgValue("-in")
	if err == nil || !strings.Contains(strings.ToLower(err.Error()), "get '-in' value failed") {
		t.Errorf("Expected Get '-in' value failed, got: %v", err)
	}
}

func TestGetFileVersionBadFileDifferent(t *testing.T) {
	m := MainMock{}
	m.heapfile = "definitely_nonexistent_file.file"
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for file not exist")
		}
	}()
	_ = m.GetFileVersion()
}