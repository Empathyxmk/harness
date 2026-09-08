package original

import (
	"testing"
)

type Modifier int

const (
	Public Modifier = iota
	Private
	Protected
	Default
	Final
	Static
)

func compareModifierVisibility(a, b Modifier) int {
	// public > protected > default > private
	score := map[Modifier]int{
		Public:    3,
		Protected: 2,
		Default:   1,
		Private:   0,
	}

	av, bv := score[a], score[b]
	switch {
	case av > bv:
		return -1
	case av < bv:
		return 1
	default:
		return 0
	}
}

func TestAPublicBnot(t *testing.T) {
	if got := compareModifierVisibility(Public, Private); got != -1 {
		t.Errorf("Expected -1, got %d", got)
	}
}
func TestADefaultBnot(t *testing.T) {
	if got := compareModifierVisibility(Default, Private); got != -1 {
		t.Errorf("Expected -1, got %d", got)
	}
}
func TestAProtectedBnot(t *testing.T) {
	if got := compareModifierVisibility(Protected, Private); got != -1 {
		t.Errorf("Expected -1, got %d", got)
	}
}
func TestBPublicAnot(t *testing.T) {
	if got := compareModifierVisibility(Private, Public); got != 1 {
		t.Errorf("Expected 1, got %d", got)
	}
}
func TestBDefaultAnot(t *testing.T) {
	if got := compareModifierVisibility(Private, Default); got != 1 {
		t.Errorf("Expected 1, got %d", got)
	}
}
func TestBProtectedAnot(t *testing.T) {
	if got := compareModifierVisibility(Private, Protected); got != 1 {
		t.Errorf("Expected 1, got %d", got)
	}
}
func TestSamePrivate(t *testing.T) {
	if got := compareModifierVisibility(Private, Private); got != 0 {
		t.Errorf("Expected 0, got %d", got)
	}
}
func TestSameProtected(t *testing.T) {
	if got := compareModifierVisibility(Private, Private); got != 0 {
		t.Errorf("Expected 0, got %d", got)
	}
}
func TestSameDefault(t *testing.T) {
	if got := compareModifierVisibility(Default, Default); got != 0 {
		t.Errorf("Expected 0, got %d", got)
	}
}
func TestSamePublic(t *testing.T) {
	if got := compareModifierVisibility(Public, Public); got != 0 {
		t.Errorf("Expected 0, got %d", got)
	}
}