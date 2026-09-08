package public_tests

import (
	"strings"
	"testing"
)

type FallBackMethodController struct{}

func (c *FallBackMethodController) DepartmentServiceFallBack(param *string) string {
	var user string
	if param == nil {
		user = ""
	} else {
		user = *param
	}
	return "Department Service is taking longer than Expected. Please try again later, User: " + user
}

func TestDepartmentServiceFallBackWithAnotherParam(t *testing.T) {
	controller := &FallBackMethodController{}
	input := "publicExample"
	result := controller.DepartmentServiceFallBack(&input)
	if !strings.Contains(result, "Department Service is taking longer") {
		t.Errorf("Expected result to contain fallback message, got: %s", result)
	}
	if !strings.Contains(result, input) {
		t.Errorf("Expected result to contain input param '%s', got: %s", input, result)
	}
}

func TestDepartmentServiceFallBack_EmptyStringParam(t *testing.T) {
	controller := &FallBackMethodController{}
	empty := ""
	result := controller.DepartmentServiceFallBack(&empty)
	if !strings.Contains(result, "Department Service is taking longer") {
		t.Errorf("Expected result to contain fallback message, got: %s", result)
	}
	// Accept any output as long as fallback message present with empty input
}