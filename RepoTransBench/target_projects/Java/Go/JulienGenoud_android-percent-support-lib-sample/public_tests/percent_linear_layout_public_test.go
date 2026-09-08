package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Re-define stubs if needed (needed for public_tests in Go module separation)
type Context struct{}
type AttributeSet struct{}

type LinearLayout struct{}
type LayoutParams struct {
	Width  int
	Height int
}
func NewLinearLayoutLayoutParams(w, h int) *LayoutParams {
	return &LayoutParams{Width: w, Height: h}
}
type MarginLayoutParams struct {
	LayoutParams
}
func NewMarginLayoutParams(w, h int) *MarginLayoutParams {
	return &MarginLayoutParams{
		LayoutParams: LayoutParams{Width: w, Height: h},
	}
}

type PercentLinearLayout struct{}
func NewPercentLinearLayout(ctx *Context, attrs *AttributeSet) *PercentLinearLayout {
	return &PercentLinearLayout{}
}
type PercentLinearLayoutLayoutParams struct {
	MarginLayoutParams
}
func NewPercentLinearLayoutLayoutParamsFromBaseParams(base *LayoutParams) *PercentLinearLayoutLayoutParams {
	if base == nil {
		return nil
	}
	return &PercentLinearLayoutLayoutParams{
		MarginLayoutParams: MarginLayoutParams{LayoutParams: LayoutParams{Width: base.Width, Height: base.Height}},
	}
}
func NewPercentLinearLayoutLayoutParams(w, h int) *PercentLinearLayoutLayoutParams {
	return &PercentLinearLayoutLayoutParams{
		MarginLayoutParams: MarginLayoutParams{LayoutParams: LayoutParams{Width: w, Height: h}},
	}
}
func NewPercentLinearLayoutLayoutParamsFromMarginParams(margin *MarginLayoutParams) *PercentLinearLayoutLayoutParams {
	if margin == nil {
		return nil
	}
	return &PercentLinearLayoutLayoutParams{
		MarginLayoutParams: *margin,
	}
}
func (pll *PercentLinearLayout) GenerateLayoutParams(attrs *AttributeSet) *PercentLinearLayoutLayoutParams {
	return NewPercentLinearLayoutLayoutParams(42, 24)
}

// ===== testGenerateLayoutParamsPublic =====
func setupPercentLinearLayoutPublic() *PercentLinearLayout {
	return NewPercentLinearLayout(&Context{}, &AttributeSet{})
}

func TestGenerateLayoutParamsPublic(t *testing.T) {
	pll := setupPercentLinearLayoutPublic()
	params := pll.GenerateLayoutParams(&AttributeSet{})
	assert.NotNil(t, params, "Expected GenerateLayoutParams to return non-nil")
	if _, ok := interface{}(params).(*PercentLinearLayoutLayoutParams); !ok {
		t.Errorf("Expected params to be of type *PercentLinearLayoutLayoutParams")
	}
}

// ===== testLayoutParamsConstructorsPublic =====
func TestLayoutParamsConstructorsPublic(t *testing.T) {
	// Use values: 50, 75; 200, 125; 8, 14
	baseParams := NewLinearLayoutLayoutParams(50, 75)
	copy1 := NewPercentLinearLayoutLayoutParamsFromBaseParams(baseParams)
	assert.Equal(t, 50, copy1.Width, "Width should match base param (public)")
	assert.Equal(t, 75, copy1.Height, "Height should match base param (public)")

	copy2 := NewPercentLinearLayoutLayoutParams(200, 125)
	assert.Equal(t, 200, copy2.Width, "Width should match direct constructor (public)")
	assert.Equal(t, 125, copy2.Height, "Height should match direct constructor (public)")

	marginParams := NewMarginLayoutParams(8, 14)
	copy3 := NewPercentLinearLayoutLayoutParamsFromMarginParams(marginParams)
	assert.Equal(t, 8, copy3.Width, "Width should match margin params (public)")
	assert.Equal(t, 14, copy3.Height, "Height should match margin params (public)")
}