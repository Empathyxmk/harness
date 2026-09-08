package model

import (
	"openjfx_javafx_maven_plugin/src/org/openjfx/model"
	"testing"
)

func TestRuntimePathOption_EnumValues(t *testing.T) {
	if model.ValueOf("CLASSPATH") != model.CLASSPATH {
		t.Errorf("Expected CLASSPATH value")
	}
	if model.ValueOf("MODULEPATH") != model.MODULEPATH {
		t.Errorf("Expected MODULEPATH value")
	}
	values := model.Values()
	if len(values) != 2 {
		t.Errorf("Expected 2 enum values, got %d", len(values))
	}
}