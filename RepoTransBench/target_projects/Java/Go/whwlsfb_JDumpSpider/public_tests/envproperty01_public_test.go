package public_tests

import (
	"strings"
	"testing"
)

type EnvProperty01 struct{}

func (e *EnvProperty01) GetName() string { return "ProcessEnvironment" }
func (e *EnvProperty01) Sniff(h *PublicDummyEnvHeapHolder) string {
	clazz := h.FindClass("java.lang.PublicProcessEnvironment")
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

type PublicDummyEnvHeapHolder struct {
	noClass            bool
	panicOnGetMap      bool
	provideArrayDump   bool
}

func (d *PublicDummyEnvHeapHolder) FindClass(name string) interface{} {
	if d.noClass {
		return nil
	}
	if name == "java.lang.PublicProcessEnvironment" {
		return d
	}
	return nil
}
func (d *PublicDummyEnvHeapHolder) GetInstances(clazz interface{}) []interface{} {
	return []interface{}{struct{}{}, struct{}{}}
}
func (d *PublicDummyEnvHeapHolder) ArrayDump(instance interface{}) map[string]string {
	return map[string]string{"PUBLIC_ENV": "VALUE42"}
}
func (d *PublicDummyEnvHeapHolder) GetMap(instance interface{}) interface{} {
	if d.panicOnGetMap {
		panic("bad_public")
	}
	return map[string]string{}
}

func TestEnvProperty01GetNamePublic(t *testing.T) {
	e := &EnvProperty01{}
	if e.GetName() != "ProcessEnvironment" {
		t.Errorf("Expected Name ProcessEnvironment, got %v", e.GetName())
	}
}

func TestEnvProperty01SniffHappyPathPublic(t *testing.T) {
	e := &EnvProperty01{}
	h := &PublicDummyEnvHeapHolder{}
	s := e.Sniff(h)
	if !strings.Contains(s, "PUBLIC_ENV") || !strings.Contains(s, "VALUE42") {
		t.Errorf("Expected ENVVAR=VAL, got %v", s)
	}
}

func TestEnvProperty01SniffHandlesExceptionPublic(t *testing.T) {
	e := &EnvProperty01{}
	h := &PublicDummyEnvHeapHolder{panicOnGetMap: true}
	defer func() { _ = recover() }()
	e.Sniff(h)
}

func TestEnvProperty01SniffNoClassFoundPublic(t *testing.T) {
	e := &EnvProperty01{}
	h := &PublicDummyEnvHeapHolder{noClass: true}
	s := e.Sniff(h)
	if s != "" {
		t.Errorf("Expected nil/empty when class not found, got %v", s)
	}
}