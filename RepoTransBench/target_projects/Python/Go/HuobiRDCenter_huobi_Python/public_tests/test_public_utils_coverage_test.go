package public_tests

import (
	"testing"
	"huobirdcenter_huobi_go/huobi/utils"
)

// TestInputCheckerPublic mirrors TestInputCheckerPublic in Python
func TestCheckShouldNotNonePublic(t *testing.T) {
	err := utils.CheckShouldNotNone(nil, "different_param")
	if err == nil {
		t.Error("Expected error when param is nil")
	}
}
func TestCheckShouldNotNoneValidPublic(t *testing.T) {
	err := utils.CheckShouldNotNone(123, "another_param")
	if err != nil {
		t.Errorf("Expected nil error but got: %v", err)
	}
}
func TestCheckShouldNonePublic(t *testing.T) {
	err := utils.CheckShouldNone(nil, "wonka_param")
	if err != nil {
		t.Errorf("Expected nil error but got: %v", err)
	}
	err = utils.CheckShouldNone(0, "wonka_param")
	if err == nil {
		t.Error("Expected error when param is NOT nil")
	}
}

// TestUrlParamsBuilderPublic mirrors TestUrlParamsBuilderPublic in Python
func TestAddAndBuildUrlPublic(t *testing.T) {
	builder := utils.NewUrlParamsBuilder()
	builder.PutUrl("x", "alpha")
	builder.PutUrl("y", "beta")
	url := builder.BuildUrl()
	if !(url == "?x=alpha&y=beta" || url == "?y=beta&x=alpha") {
		t.Errorf("Expected ?x=alpha&y=beta or ?y=beta&x=alpha, got: %s", url)
	}
	builder = utils.NewUrlParamsBuilder()
	if builder.BuildUrl() != "" {
		t.Error("Expected empty string for no params")
	}
}

// TestLogInfoPublic mirrors TestLogInfoPublic in Python
func TestLogMethodsExistPublic(t *testing.T) {
	utils.PrintWarn("public warn message")
	utils.PrintBasicInfo("public info message")
	utils.PrintReplace("public_from", "public_to")
}

// TestTimeServicePublic mirrors TestTimeServicePublic in Python
func TestGetCurrentTimePublic(t *testing.T) {
	now := utils.GetCurrentTimestamp()
	if now < 0 {
		t.Error("Expected current timestamp to be non-negative integer")
	}
}

// TestPrintMixObjectPublic mirrors TestPrintMixObjectPublic in Python
type dummyOtherStruct struct{}
func (d dummyOtherStruct) String() string { return "OtherDummy" }

func TestPrintObjectBasicPublic(t *testing.T) {
	obj := dummyOtherStruct{}
	utils.PrintBasicObject(obj)
}

func TestPrintListAndDictPublic(t *testing.T) {
	obj := dummyOtherStruct{}
	utils.PrintList([]interface{}{obj, obj})
	utils.PrintList([]interface{}{obj})
	utils.PrintDict(map[string]interface{}{"b": 2})
	utils.PrintDict(map[string]interface{}{"a": 42})
	utils.PrintBasicDict(map[string]interface{}{"z": 789})
	utils.PrintBasicList([]interface{}{9,8,7})
	utils.PrintBasicList([]interface{}{0})
}

// TestJsonParserPublic mirrors TestJsonParserPublic in Python
func TestParseJsonPublic(t *testing.T) {
	obj := map[string]interface{}{"spam": "eggs"}
	jsonStr, err := utils.JsonDumps(obj)
	if err != nil {
		t.Fatalf("Failed to dump json: %v", err)
	}
	result, err := utils.JsonLoads(jsonStr)
	if err != nil {
		t.Fatalf("Failed to load json: %v", err)
	}
	if result["spam"] != "eggs" {
		t.Errorf("Expected spam to be eggs, got: %v", result["spam"])
	}
}