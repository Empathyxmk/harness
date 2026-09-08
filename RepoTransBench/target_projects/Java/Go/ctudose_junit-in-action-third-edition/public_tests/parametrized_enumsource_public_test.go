package public_tests

import "testing"

type Colors int

const (
	RED Colors = iota
	GREEN
	BLUE
	YELLOW
)
func isPrimary(color Colors) bool {
	return color == RED || color == GREEN || color == BLUE
}

func TestIsPrimaryTrue(t *testing.T) {
	for _, color := range []Colors{RED, BLUE} {
		if !isPrimary(color) {
			t.Errorf("Color %v should be primary", color)
		}
	}
}

func TestIsPrimaryFalse(t *testing.T) {
	for _, color := range []Colors{YELLOW} {
		if isPrimary(color) {
			t.Errorf("Color %v should not be primary", color)
		}
	}
}