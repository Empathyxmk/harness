package public_tests

import (
	"testing"
)

type VirtualMachine struct {
	userVars map[string]interface{}
}

func NewPublicVirtualMachine() *VirtualMachine {
	return &VirtualMachine{userVars: make(map[string]interface{})}
}

func (vm *VirtualMachine) setUserVariable(key string, v interface{}) {
	vm.userVars[key] = v
}
func (vm *VirtualMachine) getUserVariable(key string) interface{} {
	return vm.userVars[key]
}

func TestSetAndGetUserVariableWithDifferentKey(t *testing.T) {
	vm := NewPublicVirtualMachine()
	testKey := "public_key_2"
	testVal := 7890
	vm.setUserVariable(testKey, testVal)
	val := vm.getUserVariable(testKey)
	if val != testVal {
		t.Errorf("Expected value %v, got %v", testVal, val)
	}
}

func TestSetAndGetMultipleUserVariables(t *testing.T) {
	vm := NewPublicVirtualMachine()
	vm.setUserVariable("user_var_one", 111)
	vm.setUserVariable("user_var_two", "hello")
	if vm.getUserVariable("user_var_one") != 111 {
		t.Errorf("Expected 111 for user_var_one, got %v", vm.getUserVariable("user_var_one"))
	}
	if vm.getUserVariable("user_var_two") != "hello" {
		t.Errorf("Expected 'hello' for user_var_two, got %v", vm.getUserVariable("user_var_two"))
	}
}