package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"fenjuly_toggleexpandlayout/tests"
)

type publicListener struct{}
func (p *publicListener) OnStartOpen(h, oh int) {}
func (p *publicListener) OnOpen() {}
func (p *publicListener) OnStartClose(h, oh int) {}
func (p *publicListener) OnClosed() {}

// Public test for ToggleExpandLayout constructor variation and behavior
func TestToggleExpandLayout_ConstructorWithDifferentDataPublic(t *testing.T) {
	context := &tests.Context{}
	attrs := &tests.AttributeSet{}
	layout1 := tests.NewToggleExpandLayoutWith(context, attrs, 123)
	assert.NotNil(t, layout1)

	layout2 := tests.NewToggleExpandLayoutWith(context, attrs, 789)
	assert.NotNil(t, layout2)
}

func TestToggleExpandLayout_Public_OpenCloseNoCrash(t *testing.T) {
	context := &tests.Context{}
	attrs := &tests.AttributeSet{}
	layout := tests.NewToggleExpandLayoutWith(context, attrs, 123)
	layout.Open()
	layout.Close()
	// No panic means pass
}

func TestToggleExpandLayout_Public_SetOnToggleTouchListenerNoCrash(t *testing.T) {
	context := &tests.Context{}
	attrs := &tests.AttributeSet{}
	layout := tests.NewToggleExpandLayoutWith(context, attrs, 123)
	layout.SetOnToggleTouchListener(&publicListener{})
	layout.Open()
	layout.Close()
}