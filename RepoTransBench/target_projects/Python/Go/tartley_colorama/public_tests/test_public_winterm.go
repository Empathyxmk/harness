package public_tests

import (
	"testing"
)

func TestInitPublic(t *testing.T) {
	mockAttr := &Attr{wAttributes: 171} // 0b10101011
	term := NewWinTermWithAttr(mockAttr)
	if term.fore != 3 {
		t.Errorf("expected _fore=3, got %v", term.fore)
	}
	if term.back != 2 {
		t.Errorf("expected _back=2, got %v", term.back)
	}
	if term.style != 136 {
		t.Errorf("expected _style=136, got %v", term.style)
	}
}

func TestResetAllPublic(t *testing.T) {
	mockAttr := &Attr{wAttributes: 250} // 0b11111010
	term := NewWinTermWithAttr(mockAttr)
	// mess up internal state
	term.fore = 1
	term.back = 3
	term.style = 0
	term.set_console = func() {}
	term.ResetAll()
	if term.fore != 2 {
		t.Errorf("expected _fore=2, got %v", term.fore)
	}
	if term.back != 7 {
		t.Errorf("expected _back=7, got %v", term.back)
	}
	if term.style != 136 {
		t.Errorf("expected _style=136, got %v", term.style)
	}
}

// Simulated WinTerm and dependencies for public test
type Attr struct {
	wAttributes int
}

type WinTerm struct {
	fore        int
	back        int
	style       int
	set_console func()
	attr        *Attr
}

func NewWinTermWithAttr(attr *Attr) *WinTerm {
	w := &WinTerm{attr: attr}
	w.initFromAttr()
	return w
}

func (w *WinTerm) initFromAttr() {
	w.fore = w.attr.wAttributes & 7
	w.back = (w.attr.wAttributes >> 4) & 7
	w.style = w.attr.wAttributes & ^0x77
}

func (w *WinTerm) ResetAll() {
	w.initFromAttr()
	if w.set_console != nil {
		w.set_console()
	}
}