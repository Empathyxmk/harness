package tests

import "testing"

// Translation of DropDownLayoutTest from Java
func TestDropDownLayout_OnLayoutWithSimpleChild(t *testing.T) {
	layout := NewDropDownLayout(&Context{})
	child := NewMockView(10, 5)
	layout.AddChild(child)

	if layout.GetChildCount() != 1 {
		t.Errorf("Expected 1 child, got %v", layout.GetChildCount())
	}
	layout.OnLayout(true, 0, 0, 10, 10)
	// No exception (panic) should occur
}

func TestDropDownLayout_OnLayoutWithToggleExpandLayoutChild(t *testing.T) {
	layout := NewDropDownLayout(&Context{})
	toggleChild := NewToggleExpandLayout(&Context{})
	grandChild := NewMockView(15, 3)
	toggleChild.AddChild(grandChild)
	layout.AddChild(toggleChild)

	if layout.GetChildCount() != 1 {
		t.Errorf("Expected 1 child, got %v", layout.GetChildCount())
	}
	if tc, ok := layout.GetChildAt(0).(*ToggleExpandLayout); !ok || tc == nil {
		t.Errorf("First child should be ToggleExpandLayout")
	}
	layout.OnLayout(false, 1, 2, 3, 4)
	// No exception (panic) should occur
}