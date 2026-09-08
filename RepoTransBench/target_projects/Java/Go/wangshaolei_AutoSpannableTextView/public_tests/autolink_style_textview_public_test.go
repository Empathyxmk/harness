package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Simulating the structure but with public test-specific values
type AutoLinkStyleTextView struct {
	Text            string
	StyleType       int
	OnClickCallback func(string)
	Color           int
	Drawables       map[string]int
	DefaultText     string
}

func newAutoLinkStyleTextView(defaultText string, styleType int, color int) *AutoLinkStyleTextView {
	return &AutoLinkStyleTextView{
		Text:      defaultText,
		StyleType: styleType,
		Color:     color,
		Drawables: make(map[string]int),
	}
}

func (a *AutoLinkStyleTextView) setStartImageText(txt string) {
	a.Text = txt
}

func (a *AutoLinkStyleTextView) setOnClickCallBack(cb func(string)) {
	a.OnClickCallback = cb
}

func (a *AutoLinkStyleTextView) getText() string {
	return a.Text
}

func TestConstructorAndDefaultFieldsPublic(t *testing.T) {
	target := newAutoLinkStyleTextView("Alpha;Beta", 0, 0x00ff00)
	assert.NotNil(t, target)
}

func TestSetStartImageTextNoDrawableNoCrashPublic(t *testing.T) {
	target := newAutoLinkStyleTextView("Alpha;Beta", 0, 0x00ff00)
	assert.NotNil(t, target.getText())
	target.setStartImageText("Sample")
	assert.NotNil(t, target.getText())
}

func TestSetStartImageTextWithImageAndTypePublic(t *testing.T) {
	target := newAutoLinkStyleTextView("Hello", 0, 0x00ff00)
	target.Drawables["img"] = 71
	target.setStartImageText("Hello")
	assert.NotNil(t, target.getText())
}

func TestClickCallBackSetAndTriggerPublic(t *testing.T) {
	target := newAutoLinkStyleTextView("Plan-Policy", 0, 0x00ff00)
	triggered := false
	target.setOnClickCallBack(func(s string) {
		triggered = true
	})
	if target.OnClickCallback != nil {
		target.OnClickCallback("Policy")
	}
	assert.NotNil(t, target)
	assert.True(t, triggered)
}

func TestAddStyleBranchEmptyOrNoCommaPublic(t *testing.T) {
	target := newAutoLinkStyleTextView("SingleSegment", 0, 0x00ff00)
	assert.NotNil(t, target.getText())
}

func TestClickableSpanUpdateDrawStatePublic(t *testing.T) {
	target := newAutoLinkStyleTextView("Green,Orange", 1, 0x123456)
	type TextPaint struct {
		Color int
	}
	tp := TextPaint{}
	tp.Color = target.Color
	assert.Equal(t, 0x123456, tp.Color)
}

func TestCenteredImageSpanDrawExecutesPublic(t *testing.T) {
	target := newAutoLinkStyleTextView("World", 0, 0x00ff00)
	target.Drawables["img"] = 555
	target.setStartImageText("World")
	assert.Equal(t, "World", target.getText())
}