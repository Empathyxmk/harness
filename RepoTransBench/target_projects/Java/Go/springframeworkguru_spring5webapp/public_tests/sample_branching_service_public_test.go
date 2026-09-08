package public_tests

import (
	"testing"
	"spring5webapp/internal/samplebranching"
)

func TestCategorizeNegativePublic(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	got := service.CategorizeNumber(-15)
	want := "negative"
	if got != want {
		t.Errorf("CategorizeNumber(-15) = %q; want %q", got, want)
	}
}

func TestCategorizeZeroPublic(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	got := service.CategorizeNumber(0)
	want := "zero"
	if got != want {
		t.Errorf("CategorizeNumber(0) = %q; want %q", got, want)
	}
}

func TestCategorizeSmallPublic(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	got := service.CategorizeNumber(8)
	want := "small"
	if got != want {
		t.Errorf("CategorizeNumber(8) = %q; want %q", got, want)
	}
}

func TestCategorizeLargePublic(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	got := service.CategorizeNumber(50)
	want := "large"
	if got != want {
		t.Errorf("CategorizeNumber(50) = %q; want %q", got, want)
	}
}

func TestIsEvenTruePublic(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	if !service.IsEven(6) {
		t.Error("IsEven(6) = false; want true")
	}
}

func TestIsEvenFalsePublic(t *testing.T) {
	service := samplebranching.NewSampleBranchingService()
	if service.IsEven(9) {
		t.Error("IsEven(9) = true; want false")
	}
}