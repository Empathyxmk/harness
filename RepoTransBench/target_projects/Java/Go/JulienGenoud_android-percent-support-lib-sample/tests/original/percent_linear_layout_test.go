package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// ===== Translation of PercentLinearLayoutTest.java (unit test) =====
func setupPercentLinearLayout() *PercentLinearLayout {
	return NewPercentLinearLayout(&Context{}, &AttributeSet{})
}

func TestGenerateLayoutParams(t *testing.T) {
	pll := setupPercentLinearLayout()
	params := pll.GenerateLayoutParams(&AttributeSet{})
	assert.NotNil(t, params, "Expected GenerateLayoutParams to return non-nil")
	if _, ok := interface{}(params).(*PercentLinearLayoutLayoutParams); !ok {
		t.Errorf("Expected params to be of type *PercentLinearLayoutLayoutParams")
	}
}

// This test inspects all the LayoutParams constructors.
func TestLayoutParamsConstructors(t *testing.T) {
	// LinearLayout.LayoutParams baseParams = new LinearLayout.LayoutParams(123, 456);
	baseParams := NewLinearLayoutLayoutParams(123, 456)
	copy1 := NewPercentLinearLayoutLayoutParamsFromBaseParams(baseParams)
	assert.Equal(t, 123, copy1.Width, "Width should match base param")
	assert.Equal(t, 456, copy1.Height, "Height should match base param")

	// PercentLinearLayout.LayoutParams copy2 = new PercentLinearLayout.LayoutParams(321, 654);
	copy2 := NewPercentLinearLayoutLayoutParams(321, 654)
	assert.Equal(t, 321, copy2.Width, "Width should match direct constructor")
	assert.Equal(t, 654, copy2.Height, "Height should match direct constructor")

	// LinearLayout.MarginLayoutParams marginParams = new LinearLayout.MarginLayoutParams(7, 8);
	marginParams := NewMarginLayoutParams(7, 8)
	copy3 := NewPercentLinearLayoutLayoutParamsFromMarginParams(marginParams)
	assert.Equal(t, 7, copy3.Width, "Width should match margin params")
	assert.Equal(t, 8, copy3.Height, "Height should match margin params")
}