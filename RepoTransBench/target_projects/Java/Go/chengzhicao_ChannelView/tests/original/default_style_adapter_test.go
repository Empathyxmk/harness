package original

import (
	"testing"
)

// These stubs emulate DefaultStyleAdapter/View for basic logic testing

type DefaultStyleAdapter struct {
	ChannelNormalTextColor   int
	ChannelNormalBackground  int
	ChannelFixedTextColor    int
	ChannelFixedBackground   int
	ChannelEditBackground    int
	ChannelFocusedBackground int
	ChannelFocusedTextColor  int
	ChannelTextSize          int
}

type DefaultViewHolder struct {
	itemView *TextView
}
type ViewGroup struct {
	name string
}
type TextView struct {
	text     string
	textSize float64
	color    int
	bg       int
}

func (a *DefaultStyleAdapter) createStyleView(parent *ViewGroup, channelName string) *DefaultViewHolder {
	return &DefaultViewHolder{itemView: &TextView{text: channelName}}
}
func (a *DefaultStyleAdapter) setTextColor(v *TextView, color int) {
	v.color = color
}
func (a *DefaultStyleAdapter) setTextSize(v *TextView, size float64) {
	v.textSize = size
}
func (a *DefaultStyleAdapter) setBackgroundResource(v *TextView, res int) {
	v.bg = res
}
func (a *DefaultStyleAdapter) setChannelNormalTextColor(v int) {
	a.ChannelNormalTextColor = v
}
func (a *DefaultStyleAdapter) setChannelNormalBackground(v int) {
	a.ChannelNormalBackground = v
}
func (a *DefaultStyleAdapter) setChannelFixedTextColor(v int) {
	a.ChannelFixedTextColor = v
}
func (a *DefaultStyleAdapter) setChannelFixedBackground(v int) {
	a.ChannelFixedBackground = v
}
func (a *DefaultStyleAdapter) setChannelEditBackground(v int) {
	a.ChannelEditBackground = v
}
func (a *DefaultStyleAdapter) setChannelFocusedBackground(v int) {
	a.ChannelFocusedBackground = v
}
func (a *DefaultStyleAdapter) setChannelFocusedTextColor(v int) {
	a.ChannelFocusedTextColor = v
}
func (a *DefaultStyleAdapter) setChannelTextSize(v int) {
	a.ChannelTextSize = v
}
func (a *DefaultStyleAdapter) setNormalStyle(holder *DefaultViewHolder)  {}
func (a *DefaultStyleAdapter) setFixedStyle(holder *DefaultViewHolder)   {}
func (a *DefaultStyleAdapter) setEditStyle(holder *DefaultViewHolder)    {}
func (a *DefaultStyleAdapter) setFocusedStyle(holder *DefaultViewHolder) {}

type TestAdapter struct {
	DefaultStyleAdapter
	parent *ViewGroup
}

func (ta *TestAdapter) createStyleView(parent *ViewGroup, channelName string) *DefaultViewHolder {
	ta.parent = parent
	return ta.DefaultStyleAdapter.createStyleView(parent, channelName)
}

type TestViewGroup struct {
	ViewGroup
}

func TestCreateStyleView(t *testing.T) {
	adapter := &TestAdapter{}
	parent := &ViewGroup{name: "MyParent"}
	holder := adapter.createStyleView(parent, "MyChannel")
	if holder.itemView == nil {
		t.Error("itemView should not be nil")
	}
	if holder.itemView.text != "MyChannel" {
		t.Errorf("expected text 'MyChannel', got '%s'", holder.itemView.text)
	}
}

func TestSetters(t *testing.T) {
	adapter := &TestAdapter{}
	view := &TextView{}
	adapter.setTextColor(view, 0xff112233)
	if view.color != 0xff112233 {
		t.Errorf("expected text color 0xff112233, got 0x%x", view.color)
	}
	adapter.setTextSize(view, 18)
	if view.textSize != 18.0 {
		t.Errorf("expected text size 18.0, got %f", view.textSize)
	}
	adapter.setBackgroundResource(view, 0)
	if view.bg != 0 {
		t.Errorf("expected background 0, got %d", view.bg)
	}
}

func TestSetStyleMethods(t *testing.T) {
	adapter := &TestAdapter{}
	view := &TextView{}
	holder := &DefaultViewHolder{itemView: view}
	adapter.setChannelNormalTextColor(0xf1)
	adapter.setChannelNormalBackground(0xa1)
	adapter.setChannelFixedTextColor(0xf2)
	adapter.setChannelFixedBackground(0xa2)
	adapter.setChannelEditBackground(0xa3)
	adapter.setChannelFocusedBackground(0xa4)
	adapter.setChannelFocusedTextColor(0xf3)
	// Should not panic or fail
	adapter.setNormalStyle(holder)
	adapter.setFixedStyle(holder)
	adapter.setEditStyle(holder)
	adapter.setFocusedStyle(holder)
}

func TestSetChannelTextSize(t *testing.T) {
	adapter := &TestAdapter{}
	adapter.setChannelTextSize(123)
	if adapter.ChannelTextSize != 123 {
		t.Errorf("expected ChannelTextSize 123, got %d", adapter.ChannelTextSize)
	}
}