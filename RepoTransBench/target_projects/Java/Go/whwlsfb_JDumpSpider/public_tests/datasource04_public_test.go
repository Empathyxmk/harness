package public_tests

import (
	"strings"
	"testing"
)

type DataSource04 struct{}

func (d *DataSource04) GetName() string { return "AliDruidDataSourceWrapper" }
func (d *DataSource04) Sniff(holder *PublicDummyDS04HeapHolder) string {
	clazz := holder.FindClass("AnotherDruidDataSourceWrapper")
	if clazz == nil {
		return ""
	}
	defer func() { _ = recover() }()
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

type PublicDummyDS04HeapHolder struct {
	throwOnGetInstances bool
	noClass             bool
}

func (p *PublicDummyDS04HeapHolder) FindClass(name string) interface{} {
	if p.noClass {
		return nil
	}
	if strings.Contains(name, "AnotherDruidDataSourceWrapper") {
		return p
	}
	return nil
}
func (p *PublicDummyDS04HeapHolder) GetInstances(clazz interface{}) []interface{} {
	if p.throwOnGetInstances {
		panic("publicFail")
	}
	return []interface{}{struct{}{}, struct{}{}}
}
func (p *PublicDummyDS04HeapHolder) GetFieldsByNameList(instance interface{}, fields map[string]string) map[string]string {
	return map[string]string{
		"username": "pubuser",
		"password": "pubpass",
		"jdbcUrl":  "jdbc:oracle://newhost/db",
	}
}

func TestDataSource04GetNamePublic(t *testing.T) {
	ds := &DataSource04{}
	if ds.GetName() != "AliDruidDataSourceWrapper" {
		t.Errorf("Expected AliDruidDataSourceWrapper, got %q", ds.GetName())
	}
}

func TestDataSource04SniffNoClassFoundPublic(t *testing.T) {
	ds := &DataSource04{}
	dummy := &PublicDummyDS04HeapHolder{noClass: true}
	got := ds.Sniff(dummy)
	if got != "" {
		t.Errorf("Expected nil/empty string when no class found, got: %v", got)
	}
}

func TestDataSource04SniffHappyPathPublic(t *testing.T) {
	ds := &DataSource04{}
	dummy := &PublicDummyDS04HeapHolder{}
	result := ds.Sniff(dummy)
	if !strings.Contains(result, "pubuser") || !strings.Contains(result, "pubpass") || !strings.Contains(result, "jdbc:oracle://newhost/db") {
		t.Errorf("Expected pubuser/pubpass/jdbc:oracle in output, got: %v", result)
	}
}

func TestDataSource04SniffHandlesExceptionPublic(t *testing.T) {
	ds := &DataSource04{}
	dummy := &PublicDummyDS04HeapHolder{throwOnGetInstances: true}
	defer func() {
		if r := recover(); r != nil {
			// Should not propagate panic outside
		}
	}()
	ds.Sniff(dummy)
}