package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type PublicMockContext struct {
	obtainStyledAttributesCalled int
}
type PublicMockAttrs struct{}
type PublicMockTypedArray struct {
	getIntCalled              int
	getDimensionPixelSizeCall int
	getFloatCalled            int
	getResourceIdCalled       int
	getBooleanCalled          int
	recycleCalled             int
}

func (c *PublicMockContext) ObtainStyledAttributes(attrs *PublicMockAttrs, ids []int) *PublicMockTypedArray {
	c.obtainStyledAttributesCalled++
	return &PublicMockTypedArray{}
}
func (t *PublicMockTypedArray) GetInt(index, def int) int {
	t.getIntCalled++
	return 888
}
func (t *PublicMockTypedArray) GetDimensionPixelSize(index, def int) int {
	t.getDimensionPixelSizeCall++
	return 50
}
func (t *PublicMockTypedArray) GetFloat(index int, def float32) float32 {
	t.getFloatCalled++
	return 0.88
}
func (t *PublicMockTypedArray) GetResourceId(index, def int) int {
	t.getResourceIdCalled++
	return 42
}
func (t *PublicMockTypedArray) GetBoolean(index int, def bool) bool {
	t.getBooleanCalled++
	return false
}
func (t *PublicMockTypedArray) Recycle() {
	t.recycleCalled++
}

type PublicFABToolbarLayout struct {
	context *PublicMockContext
	attrs   *PublicMockAttrs
	typed   *PublicMockTypedArray
	def     int
}

func NewPublicFABToolbarLayout1(c *PublicMockContext) *PublicFABToolbarLayout {
	return &PublicFABToolbarLayout{context: c}
}
func NewPublicFABToolbarLayout2(c *PublicMockContext, attrs *PublicMockAttrs) *PublicFABToolbarLayout {
	ta := c.ObtainStyledAttributes(attrs, []int{1})
	ta.Recycle()
	return &PublicFABToolbarLayout{context: c, attrs: attrs, typed: ta}
}
func NewPublicFABToolbarLayout3(c *PublicMockContext, attrs *PublicMockAttrs, defStyle int) *PublicFABToolbarLayout {
	ta := c.ObtainStyledAttributes(attrs, []int{1})
	ta.Recycle()
	return &PublicFABToolbarLayout{context: c, attrs: attrs, typed: ta, def: defStyle}
}

func TestFABToolbarLayout_ConstructorsWithOtherValues(t *testing.T) {
	mockContext := &PublicMockContext{}
	mockAttrs := &PublicMockAttrs{}

	layout1 := NewPublicFABToolbarLayout1(mockContext)
	assert.NotNil(t, layout1, "Layout1 should not be nil (public)")

	layout2 := NewPublicFABToolbarLayout2(mockContext, mockAttrs)
	assert.NotNil(t, layout2, "Layout2 should not be nil (public)")

	layout3 := NewPublicFABToolbarLayout3(mockContext, mockAttrs, 1)
	assert.NotNil(t, layout3, "Layout3 should not be nil (public)")
}

func TestFABToolbarLayout_ParseAttrsPublic(t *testing.T) {
	mockContext := &PublicMockContext{}
	mockAttrs := &PublicMockAttrs{}

	NewPublicFABToolbarLayout2(mockContext, mockAttrs)

	assert.True(t, mockContext.obtainStyledAttributesCalled > 0, "obtainStyledAttributes should have been called (public)")
}