package original

import (
	"strings"
	"testing"
)

type EnvProperty01 struct{}

func (e *EnvProperty01) GetName() string { return "ProcessEnvironment" }
func (e *EnvProperty01) Sniff(h *DummyEnvHeapHolder) string {
	clazz := h.FindClass("java.lang.ProcessEnvironment")
	if clazz == nil {
		return ""
	}
	defer func() { _ = recover() }()
	instances := h.GetInstances(clazz)
	if len(instances) == 0 {
		return ""
	}
	m := h.ArrayDump(instances[0])
	if len(m) == 0 {
		return ""
	}
	firstKey := ""
	firstVal := ""
	for k, v := range m {
		firstKey = k
		firstVal = v
		break
	}
	return firstKey + "=" + firstVal
}

type DummyEnvHeapHolder struct {
	noClass            bool
	panicOnGetMap      bool
	provideArrayDump   bool
}

func (d *DummyEnvHeapHolder) FindClass(name string) interface{} {
	if d.noClass {
		return nil
	}
	if name == "java.lang.ProcessEnvironment" {
		return d
	}
	return nil
}
func (d *DummyEnvHeapHolder) GetInstances(clazz interface{}) []interface{} {
	return []interface{}{struct{}{}}
}
func (d *DummyEnvHeapHolder) ArrayDump(instance interface{}) map[string]string {
	if d.provideArrayDump {
		return map[string]string{"ENVVAR": "VAL"}
	}
	return map[string]string{}
}
func (d *DummyEnvHeapHolder) GetMap(instance interface{}) interface{} {
	if d.panicOnGetMap {
		panic("bad")
	}
	return map[string]string{}
}

func TestEnvProperty01GetName(t *testing.T) {
	e := &EnvProperty01{}
	if e.GetName() != "ProcessEnvironment" {
		t.Errorf("Expected Name ProcessEnvironment, got %v", e.GetName())
	}
}

func TestEnvProperty01SniffHappyPath(t *testing.T) {
	e := &EnvProperty01{}
	h := &DummyEnvHeapHolder{provideArrayDump: true}
	s := e.Sniff(h)
	if !strings.Contains(s, "ENVVAR") || !strings.Contains(s, "VAL") {
		t.Errorf("Expected ENVVAR=VAL, got %v", s)
	}
}

func TestEnvProperty01SniffHandlesException(t *testing.T) {
	e := &EnvProperty01{}
	h := &DummyEnvHeapHolder{panicOnGetMap: true}
	defer func() { _ = recover() }()
	e.Sniff(h)
}

func TestEnvProperty01SniffNoClassFound(t *testing.T) {
	e := &EnvProperty01{}
	h := &DummyEnvHeapHolder{noClass: true}
	s := e.Sniff(h)
	if s != "" {
		t.Errorf("Expected nil/empty when class not found, got %v", s)
	}
}