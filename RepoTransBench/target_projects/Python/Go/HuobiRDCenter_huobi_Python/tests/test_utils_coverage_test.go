package tests

import (
	"testing"

	"huobirdcenter_huobi_go/huobi/utils"
)

// TestInputChecker mirrors TestInputChecker in original Python
func TestCheckShouldNotNone(t *testing.T) {
	err := utils.CheckShouldNotNone(nil, "param")
	if err == nil {
		t.Error("Expected error when param is nil")
	}
}
func TestCheckShouldNotNoneValid(t *testing.T) {
	err := utils.CheckShouldNotNone("abc", "param")
	if err != nil {
		t.Errorf("Expected nil error but got: %v", err)
	}
}
func TestCheckShouldNone(t *testing.T) {
	err := utils.CheckShouldNone(nil, "param")
	if err != nil {
		t.Errorf("Expected nil error but got: %v", err)
	}
	err = utils.CheckShouldNone("abc", "param")
	if err == nil {
		t.Error("Expected error when param is NOT nil")
	}
}

// TestUrlParamsBuilder mirrors TestUrlParamsBuilder in original Python
func TestAddAndBuildUrl(t *testing.T) {
	builder := utils.NewUrlParamsBuilder()
	builder.PutUrl("a", "1")
	builder.PutUrl("b", "2")
	url := builder.BuildUrl()
	if !(url == "?a=1&b=2" || url == "?b=2&a=1") {
		t.Errorf("Expected ?a=1&b=2 or ?b=2&a=1, got: %s", url)
	}
	builder = utils.NewUrlParamsBuilder()
	if builder.BuildUrl() != "" {
		t.Error("Expected empty string for no params")
	}
}

// TestLogInfo mirrors TestLogInfo in original Python
func TestLogMethodsExist(t *testing.T) {
	utils.PrintWarn("warn message")
	utils.PrintBasicInfo("info message")
	utils.PrintReplace("from_message", "to_message")
}

// TestTimeService mirrors TestTimeService in original Python
func TestGetCurrentTime(t *testing.T) {
	now := utils.GetCurrentTimestamp()
	if now <= 0 {
		t.Error("Expected current timestamp to be positive integer")
	}
}

// TestPrintMixObject mirrors TestPrintMixObject in original Python
type dummyStruct struct{}
func (d dummyStruct) String() string { return "Dummy" }

func TestPrintObjectBasic(t *testing.T) {
	obj := dummyStruct{}
	utils.PrintBasicObject(obj)
}

func TestPrintListAndDict(t *testing.T) {
	obj := dummyStruct{}
	l := []interface{}{obj}
	utils.PrintList(l)
	utils.PrintList([]interface{}{})
	utils.PrintDict(map[string]interface{}{"a": 1})
	utils.PrintDict(map[string]interface{}{})
	utils.PrintBasicDict(map[string]interface{}{"k": 1})
	utils.PrintBasicList([]interface{}{1,2,3})
	utils.PrintBasicList([]interface{}{})
}

// TestJsonParser mirrors TestJsonParser in original Python
func TestParseJson(t *testing.T) {
	obj := map[string]interface{}{"foo": "bar"}
	jsonStr, err := utils.JsonDumps(obj)
	if err != nil {
		t.Fatalf("Failed to dump json: %v", err)
	}
	result, err := utils.JsonLoads(jsonStr)
	if err != nil {
		t.Fatalf("Failed to load json: %v", err)
	}
	if result["foo"] != "bar" {
		t.Errorf("Expected foo to be bar, got: %v", result["foo"])
	}
}