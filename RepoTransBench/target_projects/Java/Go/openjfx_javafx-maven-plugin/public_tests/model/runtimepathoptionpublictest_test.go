package model

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx/model"
	"testing"
)

func TestRuntimePathOptionPublicTest_ValueOfDifferentData(t *testing.T) {
	if model.ValueOf("MODULEPATH") != model.MODULEPATH {
		t.Errorf("Expected MODULEPATH value")
	}
	if model.ValueOf("CLASSPATH") != model.CLASSPATH {
		t.Errorf("Expected CLASSPATH value")
	}
}

func TestRuntimePathOptionPublicTest_ValuesArrayLengthAndContentDifferentOrder(t *testing.T) {
	values := model.Values()
	if len(values) < 2 {
		t.Errorf("Expected at least 2 values in enum, got %d", len(values))
	}
	if values[0] == values[1] {
		t.Errorf("Expected different values at positions 0 and 1")
	}
}