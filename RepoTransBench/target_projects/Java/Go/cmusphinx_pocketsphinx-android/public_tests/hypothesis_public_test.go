package public_tests

import "testing"

type Hypothesis struct {
	Hypstr string
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

func TestHypothesisGettersWithDifferentValues(t *testing.T) {
	h := NewHypothesis("public test string", 123)
	if h.GetHypstr() != "public test string" {
		t.Errorf("Expected 'public test string', got '%v'", h.GetHypstr())
	}
	if h.GetBestScore() != 123 {
		t.Errorf("Expected 123, got %d", h.GetBestScore())
	}
}

func TestHypothesisWhitespaceText(t *testing.T) {
	h := NewHypothesis("    ", 1000)
	if h.GetHypstr() != "    " {
		t.Errorf("Expected four spaces, got '%v'", h.GetHypstr())
	}
	if h.GetBestScore() != 1000 {
		t.Errorf("Expected 1000, got %d", h.GetBestScore())
	}
}

func TestHypothesisLargeNegativeScore(t *testing.T) {
	h := NewHypothesis("edge", -999999)
	if h.GetHypstr() != "edge" {
		t.Errorf("Expected 'edge', got '%v'", h.GetHypstr())
	}
	if h.GetBestScore() != -999999 {
		t.Errorf("Expected -999999, got %d", h.GetBestScore())
	}
}