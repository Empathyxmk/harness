package original

import "testing"

type Attr struct{ wAttributes int }
type WinTerm struct {
	fore  int
	back  int
	style int
	attr  *Attr
}

// This test simulates the Python test for WinTerm initialization
func TestWinTermInit(t *testing.T) {
	attr := &Attr{wAttributes: 0xAB}
	term := winTermFromAttr(attr)
	if term.fore != 3 {
		t.Errorf("expected fore = 3, got %v", term.fore)
	}
	if term.back != 2 {
		t.Errorf("expected back = 2, got %v", term.back)
	}
	if term.style != 136 {
		t.Errorf("expected style = 136, got %v", term.style)
	}
}

// This test simulates the reset_all behavior for WinTerm
func TestWinTermResetAll(t *testing.T) {
	attr := &Attr{wAttributes: 250}
	term := winTermFromAttr(attr)
	term.fore = 1
	term.back = 3
	term.style = 0
	term.resetAll()
	if term.fore != 2 {
		t.Errorf("expected fore = 2, got %v", term.fore)
	}
	if term.back != 7 {
		t.Errorf("expected back = 7, got %v", term.back)
	}
	if term.style != 136 {
		t.Errorf("expected style = 136, got %v", term.style)
	}
}

func winTermFromAttr(attr *Attr) *WinTerm {
	w := &WinTerm{attr: attr}
	w.setFromAttr()
	return w
}

func (w *WinTerm) setFromAttr() {
	w.fore = w.attr.wAttributes & 7
	w.back = (w.attr.wAttributes >> 4) & 7
	w.style = w.attr.wAttributes &^ 0x77
}

func (w *WinTerm) resetAll() {
	w.setFromAttr()
}