package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type MockContext struct {
	obtainStyledAttributesCalled int
}
type MockAttrs struct{}
type MockTypedArray struct {
	getIntCalled              int
	getDimensionPixelSizeCall int
	getFloatCalled            int
	getResourceIdCalled       int
	getBooleanCalled          int
	recycleCalled             int
}

func (c *MockContext) ObtainStyledAttributes(attrs *MockAttrs, ids []int) *MockTypedArray {
	c.obtainStyledAttributesCalled++
	return &MockTypedArray{}
}
func (t *MockTypedArray) GetInt(index, def int) int {
	t.getIntCalled++
	return 500
}
func (t *MockTypedArray) GetDimensionPixelSize(index, def int) int {
	t.getDimensionPixelSizeCall++
	return 20
}
func (t *MockTypedArray) GetFloat(index int, def float32) float32 {
	t.getFloatCalled++
	return 0.42
}
func (t *MockTypedArray) GetResourceId(index, def int) int {
	t.getResourceIdCalled++
	return -1
}
func (t *MockTypedArray) GetBoolean(index int, def bool) bool {
	t.getBooleanCalled++
	return true
}
func (t *MockTypedArray) Recycle() {
	t.recycleCalled++
}

// Simulate the constructor logic for FABToolbarLayout in Java
type FABToolbarLayout struct {
	context *MockContext
	attrs   *MockAttrs
	typed   *MockTypedArray
	def     int
}

func NewFABToolbarLayout1(c *MockContext) *FABToolbarLayout {
	return &FABToolbarLayout{context: c}
}
func NewFABToolbarLayout2(c *MockContext, attrs *MockAttrs) *FABToolbarLayout {
	ta := c.ObtainStyledAttributes(attrs, []int{1})
	ta.Recycle()
	return &FABToolbarLayout{context: c, attrs: attrs, typed: ta}
}
func NewFABToolbarLayout3(c *MockContext, attrs *MockAttrs, defStyle int) *FABToolbarLayout {
	ta := c.ObtainStyledAttributes(attrs, []int{1})
	ta.Recycle()
	return &FABToolbarLayout{context: c, attrs: attrs, typed: ta, def: defStyle}
}

func TestFABToolbarLayout_ConstructorsAndParseAttrs(t *testing.T) {
	mockContext := &MockContext{}
	mockAttrs := &MockAttrs{}

	layout1 := NewFABToolbarLayout1(mockContext)
	assert.NotNil(t, layout1, "Layout1 should not be nil")

	layout2 := NewFABToolbarLayout2(mockContext, mockAttrs)
	assert.NotNil(t, layout2, "Layout2 should not be nil")

	layout3 := NewFABToolbarLayout3(mockContext, mockAttrs, 0)
	assert.NotNil(t, layout3, "Layout3 should not be nil")
}

func TestFABToolbarLayout_ParseAttrsFallback(t *testing.T) {
	mockContext := &MockContext{}
	mockAttrs := &MockAttrs{}

	// Call constructor that triggers attribute parsing
	NewFABToolbarLayout2(mockContext, mockAttrs)

	assert.True(t, mockContext.obtainStyledAttributesCalled > 0, "obtainStyledAttributes should have been called")
	// Since NewFABToolbarLayout2/3 always calls Recycle() once
}