package original

import (
	"testing"
	"github.com/xiaofeidev/roundwidget/roundwidget"
)

func TestRoundImageViewConstructorAndInitMinimal(t *testing.T) {
	view := roundwidget.NewRoundImageView(nil)
	if view == nil {
		t.Fatal("view is nil")
	}
	if view == nil {
		t.Error("view is not instance of RoundImageView")
	}
	if view.GetRadiusList() == ([8]float32{}) {
		t.Error("radius list should not be zero array")
	}
	if roundwidget.StrokeModePadding != 0 {
		t.Errorf("StrokeModePadding want 0, got %v", roundwidget.StrokeModePadding)
	}
	if roundwidget.StrokeModeOverlay != 1 {
		t.Errorf("StrokeModeOverlay want 1, got %v", roundwidget.StrokeModeOverlay)
	}
}

// ...rest unchanged