package public_tests

import "testing"
import "fenjuly_toggleexpandlayout/tests"

// Public test for DropDownLayout with different input data
func TestDropDownLayoutPublic_OnLayoutWithDifferentSimpleChild(t *testing.T) {
	layout := tests.NewDropDownLayout(&tests.Context{})
	child1 := tests.NewMockView(13, 8)
	child2 := tests.NewMockView(17, 4)
	layout.AddChild(child1)
	layout.AddChild(child2)
	if layout.GetChildCount() != 2 {
		t.Errorf("Expected 2 children, got %v", layout.GetChildCount())
	}
	layout.OnLayout(true, 2, 3, 7, 12)
	// No panic expected
}

func TestDropDownLayoutPublic_OnLayoutWithDifferentToggleExpandLayoutChild(t *testing.T) {
	layout := tests.NewDropDownLayout(&tests.Context{})
	toggleChild := tests.NewToggleExpandLayout(&tests.Context{})
	grandChild1 := tests.NewMockView(20, 5)
	grandChild2 := tests.NewMockView(9, 2)
	toggleChild.AddChild(grandChild1)
	toggleChild.AddChild(grandChild2)
	child2 := tests.NewMockView(14, 7)
	layout.AddChild(toggleChild)
	layout.AddChild(child2)
	if layout.GetChildCount() != 2 {
		t.Errorf("Expected 2 children, got %v", layout.GetChildCount())
	}
	layout.OnLayout(false, 4, 5, 6, 10)
	// No panic expected
}