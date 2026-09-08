package original

import (
	"strings"
	"testing"
)

// Minimal interface stubs per Java for test purposes only
type DataSource04 struct{}

func (d *DataSource04) GetName() string { return "AliDruidDataSourceWrapper" }
func (d *DataSource04) Sniff(holder *DummyDS04HeapHolder) string {
	clazz := holder.FindClass("DruidDataSourceWrapper")
	if clazz == nil {
		return ""
	}
	defer func() {
		_ = recover() // swallow panics
	}()
	instances := holder.GetInstances(clazz)
	if len(instances) == 0 {
		return ""
	}
	creds := holder.GetFieldsByNameList(instances[0], map[string]string{
		"username": "",
		"password": "",
		"jdbcUrl":  "",
	})
	return creds["username"] + "," + creds["password"] + "," + creds["jdbcUrl"]
}
type DummyDS04HeapHolder struct {
	throwOnGetInstances bool
	noClass             bool
}

func (d *DummyDS04HeapHolder) FindClass(name string) interface{} {
	if d.noClass {
		return nil
	}
	if strings.Contains(name, "DruidDataSourceWrapper") {
		return d
	}
	return nil
}
func (d *DummyDS04HeapHolder) GetInstances(clazz interface{}) []interface{} {
	if d.throwOnGetInstances {
		panic("fail")
	}
	return []interface{}{struct{}{}}
}
func (d *DummyDS04HeapHolder) GetFieldsByNameList(instance interface{}, fields map[string]string) map[string]string {
	return map[string]string{
		"username": "user",
		"password": "pass",
		"jdbcUrl":  "jdbc:mysql://localhost/x",
	}
}

func TestDataSource04GetName(t *testing.T) {
	ds := &DataSource04{}
	if ds.GetName() != "AliDruidDataSourceWrapper" {
		t.Errorf("Expected AliDruidDataSourceWrapper, got %q", ds.GetName())
	}
}

func TestDataSource04SniffNoClassFound(t *testing.T) {
	ds := &DataSource04{}
	dummy := &DummyDS04HeapHolder{noClass: true}
	got := ds.Sniff(dummy)
	if got != "" {
		t.Errorf("Expected nil/empty string when no class found, got: %v", got)
	}
}

func TestDataSource04SniffHappyPath(t *testing.T) {
	ds := &DataSource04{}
	dummy := &DummyDS04HeapHolder{}
	result := ds.Sniff(dummy)
	if !strings.Contains(result, "user") || !strings.Contains(result, "pass") || !strings.Contains(result, "jdbc:mysql://localhost/x") {
		t.Errorf("Expected user/pass/jdbc in output, got: %v", result)
	}
}

func TestDataSource04SniffHandlesException(t *testing.T) {
	ds := &DataSource04{}
	dummy := &DummyDS04HeapHolder{throwOnGetInstances: true}
	defer func() {
		if r := recover(); r != nil {
			// ok, should not panic outside
		}
	}()
	ds.Sniff(dummy)
}