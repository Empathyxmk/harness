package original

import (
	"testing"
	"spring5webapp/internal/samplebranching"
)

func TestCategorizeNegative(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	got := service.CategorizeNumber(-5)
	want := "negative"
	if got != want {
		t.Errorf("CategorizeNumber(-5) = %q; want %q", got, want)
	}
}

func TestCategorizeZero(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	got := service.CategorizeNumber(0)
	want := "zero"
	if got != want {
		t.Errorf("CategorizeNumber(0) = %q; want %q", got, want)
	}
}

func TestCategorizeSmall(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	got := service.CategorizeNumber(5)
	want := "small"
	if got != want {
		t.Errorf("CategorizeNumber(5) = %q; want %q", got, want)
	}
}

func TestCategorizeLarge(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	got := service.CategorizeNumber(100)
	want := "large"
	if got != want {
		t.Errorf("CategorizeNumber(100) = %q; want %q", got, want)
	}
}

func TestIsEvenTrue(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	if !service.IsEven(2) {
		t.Error("IsEven(2) = false; want true")
	}
}

func TestIsEvenFalse(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	if service.IsEven(3) {
		t.Error("IsEven(3) = true; want false")
	}
}