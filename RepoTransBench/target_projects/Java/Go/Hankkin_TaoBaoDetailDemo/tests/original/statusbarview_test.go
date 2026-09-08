package original

import (
	"testing"
)

type MockStatusBarView struct{}

func NewMockStatusBarView() *MockStatusBarView {
	return &MockStatusBarView{}
}
func NewMockStatusBarViewWithAttrs() *MockStatusBarView {
	return &MockStatusBarView{}
}

func TestStatusBarView_Constructors(t *testing.T) {
	sbv1 := NewMockStatusBarView()
	if sbv1 == nil {
		t.Error("StatusBarView(ctx) returned nil")
	}
	sbv2 := NewMockStatusBarViewWithAttrs()
	if sbv2 == nil {
		t.Error("StatusBarView(ctx, attrs) returned nil")
	}
}