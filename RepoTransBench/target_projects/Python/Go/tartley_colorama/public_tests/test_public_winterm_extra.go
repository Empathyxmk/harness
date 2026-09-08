package public_tests

import "testing"

func TestWinTermPublicExtractAttributes(t *testing.T) {
	attr := &Attr{wAttributes: 0b11010101} // some pattern
	term := NewWinTermWithAttr(attr)
	if term.fore != 5 {
		t.Errorf("expected fore = 5, got %v", term.fore)
	}
	if term.back != 13 {
		t.Errorf("expected back = 13, got %v", term.back)
	}
	wantStyle := 0b11010101 &^ 0x77
	if term.style != wantStyle {
		t.Errorf("expected style = %d, got %v", wantStyle, term.style)
	}
}