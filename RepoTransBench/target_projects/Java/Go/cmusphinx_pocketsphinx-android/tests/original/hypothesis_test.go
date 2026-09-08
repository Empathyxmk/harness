package original

import (
	"testing"
)

// Minimal dummy Hypothesis struct for testability
type Hypothesis struct {
	Hypstr    string
	BestScore int
}

func NewHypothesis(hypstr string, bestScore int) *Hypothesis {
	return &Hypothesis{Hypstr: hypstr, BestScore: bestScore}
}

func (h *Hypothesis) GetHypstr() string {
	return h.Hypstr
}

func (h *Hypothesis) GetBestScore() int {
	return h.BestScore
}

func TestHypothesisGetters(t *testing.T) {
	h := NewHypothesis("hello world", 42)
	if h.GetHypstr() != "hello world" {
		t.Errorf("Expected 'hello world', got '%v'", h.GetHypstr())
	}
	if h.GetBestScore() != 42 {
		t.Errorf("Expected 42, got %d", h.GetBestScore())
	}
}

func TestHypothesisEmptyText(t *testing.T) {
	h := NewHypothesis("", 0)
	if h.GetHypstr() != "" {
		t.Errorf("Expected empty hypstr, got '%v'", h.GetHypstr())
	}
	if h.GetBestScore() != 0 {
		t.Errorf("Expected 0 score, got %d", h.GetBestScore())
	}
}

func TestHypothesisNegativeScore(t *testing.T) {
	h := NewHypothesis("neg", -1)
	if h.GetHypstr() != "neg" {
		t.Errorf("Expected 'neg', got '%v'", h.GetHypstr())
	}
	if h.GetBestScore() != -1 {
		t.Errorf("Expected -1 score, got %d", h.GetBestScore())
	}
}