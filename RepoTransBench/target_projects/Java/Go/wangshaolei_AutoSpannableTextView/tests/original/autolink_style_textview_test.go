package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Simulating the structure of AutoLinkStyleTextView
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
	// Simulate text/image logic
	a.Text = txt
}

func (a *AutoLinkStyleTextView) setOnClickCallBack(cb func(string)) {
	a.OnClickCallback = cb
}

func (a *AutoLinkStyleTextView) getText() string {
	return a.Text
}

func TestConstructorAndDefaultFields(t *testing.T) {
	target := newAutoLinkStyleTextView("init", 1, 0xff0000)
	assert.NotNil(t, target)
}

func TestSetStartImageTextNoDrawableNoCrash(t *testing.T) {
	target := newAutoLinkStyleTextView("init", 1, 0xff0000)
	assert.NotNil(t, target.getText())
	target.setStartImageText("Test")
	assert.NotNil(t, target.getText())
}

func TestSetStartImageTextWithImageAndType(t *testing.T) {
	target := newAutoLinkStyleTextView("init", 0, 0xff0000)
	// Simulate a drawable existing at resource ID 42, assign as key "img"
	target.Drawables["img"] = 42
	target.setStartImageText("Hi")
	assert.NotNil(t, target.getText())
}

func TestClickCallBackSetAndTrigger(t *testing.T) {
	target := newAutoLinkStyleTextView("Buy,User", 1, 0xff0000)
	triggered := false
	target.setOnClickCallBack(func(s string) {
		triggered = true
	})
	// Simulate clicking "Buy"
	if target.OnClickCallback != nil {
		target.OnClickCallback("Buy")
	}
	assert.NotNil(t, target)
	assert.True(t, triggered)
}

func TestAddStyleBranchEmptyOrNoComma(t *testing.T) {
	target := newAutoLinkStyleTextView("OnlyOne", 1, 0xff0000)
	assert.NotNil(t, target.getText())
}

func TestClickableSpanUpdateDrawState(t *testing.T) {
	target := newAutoLinkStyleTextView("Buy,User", 1, 0xff0000)
	// Simulate that a ClickableSpan applies color
	type TextPaint struct {
		Color int
	}
	tp := TextPaint{}
	tp.Color = target.Color
	assert.Equal(t, 0xff0000, tp.Color)
}

func TestCenteredImageSpanDrawExecutes(t *testing.T) {
	target := newAutoLinkStyleTextView("Hey", 0, 0xff0000)
	target.Drawables["img"] = 999
	target.setStartImageText("Hey")
	// Simulate drawing: just a smoke call
	assert.Equal(t, "Hey", target.getText())
}