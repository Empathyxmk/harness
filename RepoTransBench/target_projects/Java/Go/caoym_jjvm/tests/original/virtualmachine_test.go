package original

import (
	"reflect"
	"testing"
)

type DummyMethod struct {
	Called bool
}

func (d *DummyMethod) Call(env Env, thiz interface{}, args ...interface{}) {
	d.Called = true
}
func (d *DummyMethod) GetParameterCount() int { return 1 }
func (d *DummyMethod) GetName() string        { return "main" }

type DummyClass struct {
	Method *DummyMethod
}

func NewDummyClass() *DummyClass {
	return &DummyClass{Method: &DummyMethod{}}
}

func (d *DummyClass) GetMethod(name string, descriptor string) JvmMethod {
	if name == "main" && descriptor == "([Ljava/lang/String;)V" {
		return d.Method
	}
	return nil
}

type DummyClassLoader struct {
	Loaded bool
}

func (d *DummyClassLoader) LoadClass(className string) JvmClass {
	d.Loaded = true
	return NewDummyClass()
}

type VirtualMachine struct {
	classLoader JvmClassLoader
	classCache  map[string]JvmClass
}

func NewVirtualMachine(classLoader JvmClassLoader) *VirtualMachine {
	return &VirtualMachine{
		classLoader: classLoader,
		classCache:  make(map[string]JvmClass),
	}
}

func (vm *VirtualMachine) GetClass(className string) JvmClass {
	cls, ok := vm.classCache[className]
	if !ok {
		cls = vm.classLoader.LoadClass(className)
		vm.classCache[className] = cls
	}
	return cls
}

// Tests
func TestGetClassCachesAndReturns(t *testing.T) {
	loader := &DummyClassLoader{}
	vm := NewVirtualMachine(loader)

	cls1 := vm.GetClass("hello.FakeClass")
	if !loader.Loaded {
		t.Errorf("Expected loader.Loaded to be true after first load")
	}
	loader.Loaded = false

	cls2 := vm.GetClass("hello.FakeClass")
	if loader.Loaded {
		t.Errorf("Expected loader.Loaded to be false for cached load")
	}
	if !reflect.DeepEqual(cls1, cls2) {
		t.Errorf("Expected cached class to be same instance")
	}
}